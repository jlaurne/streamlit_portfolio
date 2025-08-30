# app.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

def init_firestore():
    if not firebase_admin._apps:
        # Pass the entire 'firebase' section from secrets
        creds = credentials.Certificate(st.secrets["firebase"])
        firebase_admin.initialize_app(creds)
    return firestore.client()

db = init_firestore()

st.title("Firebase Connection Successful!")
st.write("Your app is now correctly configured to connect to Firestore using Streamlit secrets.")