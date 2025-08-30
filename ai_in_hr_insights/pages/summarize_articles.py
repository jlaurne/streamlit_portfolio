# summarize_articles.py
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# --- Firebase Initialization (same as fetch_articles.py) ---
# ...

# --- Gemini API Configuration ---
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY') # Get key from environment/secrets
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_summary(text, audience):
    if audience == "Leadership":
        prompt = f"""
        Summarize the following article for a leadership audience. Focus on the strategic implications, potential business impact, and key takeaways for decision-makers. Ignore technical jargon. Be concise and outcome-oriented.

        Article:
        {text}

        Summary:
        """
    elif audience == "Product/Engineering":
        prompt = f"""
        Summarize the following article for a technical product and engineering audience. Focus on the underlying technology, methodologies, potential tools, and practical implementation details. Highlight any new frameworks, APIs, or architectural patterns mentioned.

        Article:
        {text}

        Summary:
        """
    else:
        return ""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Could not generate summary."


def process_pending_articles():
    articles_to_summarize = db.collection('articles').where('summarized', '==', False).stream()

    for article in articles_to_summarize:
        article_data = article.to_dict()
        article_text = article_data.get('summary_raw') # Use full text when available

        print(f"Summarizing: {article_data['title']}")

        summary_leadership = generate_summary(article_text, "Leadership")
        summary_pe = generate_summary(article_text, "Product/Engineering")

        article.reference.update({
            'summary_leadership': summary_leadership,
            'summary_pe': summary_pe,
            'summarized': True,
            'summarized_at': firestore.SERVER_TIMESTAMP
        })

if __name__ == "__main__":
    process_pending_articles()