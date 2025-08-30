# app.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta


def init_firestore():
    if not firebase_admin._apps:
        # Pass the entire 'firebase' section from secrets
        creds = credentials.Certificate(st.secrets["firebase"])
        firebase_admin.initialize_app(creds)
    return firestore.client()

db = init_firestore()

st.set_page_config(page_title="HR & AI Insights", layout="wide")
st.title("🚀 HR & AI Daily Insights")

# --- Fetch Today's Articles ---
today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
query = db.collection('articles').where('summarized_at', '>=', today_start).order_by('summarized_at', direction=firestore.Query.DESCENDING)
docs = query.stream()

# --- Display Digest ---
st.header(f"Digest for {datetime.now().strftime('%A, %B %d, %Y')}")

# Toggle for audience view
audience = st.radio("Select Your Audience View:", ('Leadership', 'Product / Engineering'), horizontal=True)
summary_key = 'summary_leadership' if audience == 'Leadership' else 'summary_pe'

for doc in docs:
    article = doc.to_dict()
    st.subheader(article['title'])
    st.write(f"Source: {article['source']} | [Read Full Article]({article['link']})")
    
    with st.expander("View Summary"):
        st.markdown(article.get(summary_key, "Summary not available."))
    st.divider()