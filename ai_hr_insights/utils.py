import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json
import openai

def init_firebase():
    if not firebase_admin._apps:  # prevent double init
        firebase_config = st.secrets["firebase"]
        cred = credentials.Certificate(dict(firebase_config))
        firebase_admin.initialize_app(cred)
    return firestore.client()   


def summarize_article(text, audience):
    prompt = f"""
    Summarize the following article for {audience}.
    Provide 2-3 concise bullet points.
    Article: {text}
    """
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content": prompt}],
        temperature=0.3
    )
    return resp["choices"][0]["message"]["content"]
