# vacancy_forecast_gemma.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import altair as alt

# Optional: Hugging Face / transformers for Gemma. If not present, code falls back.
try:
    from transformers import AutoTokenizer, AutoModel
    from transformers import AutoModelForCausalLM, pipeline
    HF_AVAILABLE = True
except Exception:
    HF_AVAILABLE = False

# For embeddings fallback (TF-IDF)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(layout="wide", page_title="Vacancy Forecast + Gemma Chatbot")

# ----------------------
# Helper: fake data generator
# ----------------------
def generate_fake_movements(seed=42, months=36, n_business_areas=5, seg2_per_ba=3, seg3_per_seg2=2, seg4_per_seg3=2):
    np.random.seed(seed)
    start = datetime.today() - pd.DateOffset(months=months)
    records = []
    business_areas = [f"BA_{i+1}" for i in range(n_business_areas)]
    for ba in business_areas:
        for s2 in range(1, seg2_per_ba+1):
            seg2 = f"{ba}_S2_{s2}"
            for s3 in range(1, seg3_per_seg2+1):
                seg3 = f"{seg2}_S3_{s3}"
                for s4 in range(1, seg4_per_seg3+1):
                    seg4 = f"{seg3}_S4_{s4}"
                    # create time series of headcount, hires, exits per month
                    base_head = np.random.randint(20, 200)
                    for m in range(months):
                        month = (start + pd.DateOffset(months=m)).strftime("%Y-%m")
                        hires = np.random.poisson(lam=max(1, base_head*0.02))
                        exits = np.random.poisson(lam=max(1, base_head*0.015 + 0.2*np.sin(m/6))))
                        # hires or exits may include transfers; we keep simple
                        records.append({
                            "business_area": ba,
                            "seg2": seg2,
                            "seg3": seg3,
                            "seg4": seg4,
                            "month": month,
                            "base_headcount": base_head,
                            "hires": int(hires),
                            "exits": int(exits)
                        })
    return pd.DataFrame.from_records(records)

# ----------------------
# Forecast logic (simple): use historical exits to estimate future vacancies,
# average time-to-fill (months) by segment level applied to compute open-months and savings
# ----------------------
def compute_aggregates(df):
    # compute net movement per month, vacancy proxy = exits - hires (positive => net openings)
    df["net_openings"] = df["exits"] - df["hires"]
    agg = df.groupby(["business_area", "month"]).agg({
        "hires":"sum", "exits":"sum", "net_openings":"sum"
    }).reset_index()
    # monthly vacancy count proxy = cumulative net_openings clipped at 0
    agg["vacancy_running"] = agg.groupby("business_area")["net_openings"].cumsum().clip(lower=0)
    return agg

def forecast_vacancies(agg, months_ahead=12, avg_time_to_fill_by_seg=None):
    # Simple forecast: take last 12-month average exits per business_area and project forward;
    # use avg_time_to_fill_by_seg (dict mapping seg level keys to months) to estimate vacancy-months.
    last_month = agg["month"].max()
    bas = agg["business_area"].unique()
    forecasts = []
    for ba in bas:
        sub = agg[agg["business_area"]==ba]
        # avg monthly exits last 12
        recent = sub.tail(12)
        avg_exits = recent["exits"].mean() if len(recent)>0 else 0
        # project future months
        for m in range(1, months_ahead+1):
            target_month = (pd.to_datetime(last_month + "-01") + pd.DateOffset(months=m)).strftime("%Y-%m")
            # naive projection: use avg_exits as new openings
            projected_new_openings = avg_exits * np.random.uniform(0.9,1.1)
            forecasts.append({
                "business_area": ba,
                "month": target_month,
                "projected_new_openings": projected_new_openings
            })
    fdf = pd.DataFrame(forecasts)
    return fdf

def estimate_savings(forecast_df, avg_salary, approved_fraction=1.0, months_vacant_assumption=3):
    # savings = projected_new_openings * approved_fraction * (avg_salary * months_vacant_assumption / 12)
    forecast_df["estimated_savings"] = forecast_df["projected_new_openings"] * approved_fraction * (avg_salary * months_vacant_assumption / 12.0)
    return forecast_df

# ----------------------
# Small RAG/chat utilities
# ----------------------
def dataframe_to_chunks(df, chunk_cols=None):
    """Convert a dataframe into a list of textual chunks for embedding/retrieval."""
    chunks = []
    if chunk_cols is None:
        chunk_cols = df.columns.tolist()
    for i, row in df.iterrows():
        text = " | ".join([f"{c}: {row[c]}" for c in chunk_cols if c in row.index])
        chunks.append(text)
    return chunks

# Embedding wrapper (tries to use Gemma via transformers if available)
class EmbeddingEngine:
    def __init__(self, model_name="google/embedding-gemma", hf_token=None):
        self.model_name = model_name
        self.hf_token = hf_token
        self.online = HF_AVAILABLE
        if self.online:
            try:
                # many embedding models expect a simple tokenizer + model
                from transformers import AutoTokenizer, AutoModel
                self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=hf_token)
                self.model = AutoModel.from_pretrained(model_name, use_auth_token=hf_token)
                self.model.eval()
                self.online = True
            except Exception as e:
                st.warning(f"Could not load HF embedding model {model_name}: {e}")
                self.online = False
        # fallback vectorizer
        self.vectorizer = TfidfVectorizer(max_features=2000)

    def embed_texts(self, texts):
        if self.online:
            # simple mean pooling of last hidden state
            import torch
            toks = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
            with torch.no_grad():
                out = self.model(**toks)
                # out.last_hidden_state shape: (batch, seq_len, dim)
                hs = out.last_hidden_state
                mask = toks["attention_mask"].unsqueeze(-1)
                summed = (hs * mask).sum(dim=1)
                counts = mask.sum(dim=1)
                embeddings = (summed / counts).cpu().numpy()
            return embeddings
        else:
            # fallback: tfidf
            emb = self.vectorizer.fit_transform(texts).toarray()
            return emb

# Simple LM wrapper for generation using Gemma (if available)
class LMEngine:
    def __init__(self, model_name="google/gemma-7b-instruct", hf_token=None):
        self.model_name = model_name
        self.hf_token = hf_token
        self.online = HF_AVAILABLE
        self.generator = None
        if self.online:
            try:
                self.generator = pipeline("text-generation", model=model_name, device_map="auto", use_auth_token=hf_token, max_length=512)
            except Exception as e:
                st.warning(f"Couldn't init Gemma LM pipeline: {e}")
                self.generator = None
                self.online = False

    def generate(self, prompt, max_length=256):
        if self.generator:
            out = self.generator(prompt, max_length=max_length, do_sample=True, top_p=0.95, temperature=0.2)
            return out[0]["generated_text"]
        else:
            # fallback: template-based reply using retrieved context
            return "I don't have the Gemma model loaded locally. Based on the retrieved data:\n\n" + prompt[:1000]

# Retrieval + generation: retrieve top-k chunks by embedding similarity, craft prompt
def answer_query(query, chunks, embeddings, emb_engine, lm_engine, top_k=3):
    q_emb = emb_engine.embed_texts([query])[0]
    sims = cosine_similarity([q_emb], embeddings)[0]
    top_idx = np.argsort(sims)[::-1][:top_k]
    context = "\n\n".join([chunks[i] for i in top_idx])
    prompt = f"""You are an assistant answering questions about an employee movement and vacancy dataset. Use the context below to answer the user's question.\n\nContext:\n{context}\n\nUser question: {query}\n\nAnswer concisely, citing relevant context rows where helpful."""
    answer = lm_engine.generate(prompt)
    return answer, context

# ----------------------
# Streamlit app layout & interactivity
# ----------------------
st.title("Vacancy Forecasting + Gemma RAG Chatbot (demo)")

with st.sidebar:
    st.header("Simulation controls")
    seed = st.number_input("Random seed", value=42, step=1)
    months_hist = st.slider("History months", min_value=12, max_value=60, value=36)
    n_ba = st.slider("Business areas", min_value=1, max_value=8, value=4)
    seg2_per_ba = st.slider("Seg2 per BA", 1, 6, 2)
    seg3_per_seg2 = st.slider("Seg3 per Seg2", 1, 4, 1)
    seg4_per_seg3 = st.slider("Seg4 per Seg3", 1, 3, 1)
    months_forecast = st.slider("Months forecast", 1, 24, 12)
    avg_salary = st.number_input("Avg annual salary (USD) used to compute savings", value=90000.0, step=1000.0, format="%.2f")
    months_vacant_assumption = st.number_input("Assumed months vacant counted as savings", min_value=1, max_value=12, value=3)
    approved_fraction = st.slider("Fraction of vacancies approved in AOP (0-1)", 0.0, 1.0, 1.0)

st.markdown("### 1) Generate fake employee movement data")
if st.button("Generate data"):
    df = generate_fake_movements(seed=seed, months=months_hist,
                                 n_business_areas=n_ba,
                                 seg2_per_ba=seg2_per_ba,
                                 seg3_per_seg2=seg3_per_seg2,
                                 seg4_per_seg3=seg4_per_seg3)
    st.session_state["df"] = df
    st.success("Generated fake movement data.")
else:
    df = st.session_state.get("df", None)
    if df is None:
        st.info("No dataset in session. Click 'Generate data' in the sidebar to create a sample dataset.")
        st.stop()

st.write("Sample of generated data (first 20 rows):")
st.dataframe(df.head(20))

# Aggregates and forecast
agg = compute_aggregates(df)
st.markdown("### 2) Aggregated trends by business area")
sel_ba = st.selectbox("Select business area to inspect", options=sorted(agg["business_area"].unique()))
plot_df = agg[agg["business_area"]==sel_ba]
chart = alt.Chart(plot_df).transform_fold(["hires","exits","vacancy_running"], as_=["metric","value"]).mark_line().encode(
    x="month:T",
    y="value:Q",
    color="metric:N"
).properties(height=300, width=700)
st.altair_chart(chart, use_container_width=True)

# Forecast
fdf = forecast_vacancies(agg, months_ahead=months_forecast)
savings_df = estimate_savings(fdf, avg_salary=avg_salary, approved_fraction=approved_fraction, months_vacant_assumption=months_vacant_assumption)
st.markdown("### 3) Forecasted projected openings and estimated savings (first rows)")
st.dataframe(savings_df.head(20))

# Aggregated savings per business area
agg_savings = savings_df.groupby("business_area")["estimated_savings"].sum().reset_index().sort_values("estimated_savings", ascending=False)
st.markdown("#### Total estimated savings over forecast horizon by business area")
st.table(agg_savings)

# ----------------------
# Build RAG index (embeddings) for chatbot
# ----------------------
st.markdown("### 4) Chatbot (RAG) powered by EmbeddingGemma + Gemma (if available)")
use_hf = st.checkbox("Attempt to use Hugging Face Gemma models (embedding + LM) if installed", value=False)
hf_token = st.text_input("Optional Hugging Face token (if required)", value="", type="password")

# Prepare textual chunks (we'll use aggregated monthly rows as chunks)
chunks = dataframe_to_chunks(df[["business_area","seg2","seg3","seg4","month","hires","exits"]].head(200))  # limit size for demo

# init engines
if use_hf:
    emb_engine = EmbeddingEngine(model_name="google/embedding-gemma", hf_token=hf_token or None)
    lm_engine = LMEngine(model_name="google/gemma-7b-instruct", hf_token=hf_token or None)
else:
    emb_engine = EmbeddingEngine(model_name=None)
    lm_engine = LMEngine(model_name=None)

with st.spinner("Embedding dataset for retrieval..."):
    embeddings = emb_engine.embed_texts(chunks)

st.success("Embeddings ready (or TF-IDF fallback prepared).")

query = st.text_input("Ask about the data (e.g., 'Which business area will save the most next 12 months?')", value="")
if st.button("Ask"):
    if not query:
        st.warning("Type a question first.")
    else:
        ans, ctx = answer_query(query, chunks, embeddings, emb_engine, lm_engine, top_k=3)
        st.markdown("**Answer**")
        st.write(ans)
        st.markdown("**Retrieved context (top rows)**")
        for c in ctx.split("\n\n"):
            st.write("-", c)

st.markdown("---")
st.write("Notes and next steps:")
st.write("""
- This demo uses a **very simple forecasting approach** (12-month average exits projected forward). Replace `forecast_vacancies` with a proper predictive model (ARIMA, Prophet, or ML model) that uses segment-level average time-to-fill as features.
- To use Gemma/EmbeddingGemma in production, either:
  1. Run Gemma models locally (via the gemma library / Hugging Face weights) or
  2. Use a hosted Gemma endpoint (Vertex/other) and call it to get embeddings and completions. See Gemma docs for examples and best practices. :contentReference[oaicite:2]{index=2}
- For accurate "savings" treatment, align with finance rules: which portion of salary, benefits, and overhead are counted, and whether vacancy attrition is permanent vs. backfilled mid-year.
""")
