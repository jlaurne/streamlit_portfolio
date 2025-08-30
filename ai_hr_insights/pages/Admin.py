import streamlit as st
from utils import init_firebase
from datetime import datetime

db = init_firebase()

st.header("Add Article Manually")

title = st.text_input("Title")
url = st.text_input("URL")
source = st.text_input("Source", "Manual")
if st.button("Save"):
    db.collection("articles").add({
        "title": title,
        "url": url,
        "date": datetime.utcnow(),
        "source": source,
        "tags": [],
    })
    st.success("Article added")

st.header("Generate Summaries")
articles_ref = db.collection("articles").stream()

for doc in articles_ref:
    art = doc.to_dict()
    if "summary_leadership" not in art:
        if st.button(f"Summarize {art['title']}"):
            text = art["title"]  # later replace with full scraped text
            leadership = summarize_article(text, "Leadership (strategic)")
            dsp = summarize_article(text, "Data Strategy & Platforms (technical)")
            db.collection("articles").document(doc.id).update({
                "summary_leadership": leadership,
                "summary_dsp": dsp
            })
            st.success("Summaries added")
