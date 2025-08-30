import streamlit as st
from utils import init_firebase

db = init_firebase()
st.title("AI in HR Insights")

articles = db.collection("articles").order_by("date", direction="DESCENDING").limit(5).stream()

for doc in articles:
    art = doc.to_dict()
    st.subheader(art["title"])
    st.write(f"[Read]({art['url']}) | {art['source']}")
    st.markdown("**Leadership View:** " + art.get("summary_leadership","-"))
    st.markdown("**DSP View:** " + art.get("summary_dsp","-"))
