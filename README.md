# 🕵️‍♂️ AI-Powered Fact Checker using LLM + RAG

This is a demo system that verifies news claims using a **RAG (Retrieval-Augmented Generation)** pipeline powered by **Google Gemini**, **FAISS**, and **SentenceTransformers**. It extracts claims, retrieves relevant facts, and uses an LLM to generate a verdict.

## 🚀 Features

- Claim extraction using spaCy
- Fact embedding with `all-MiniLM-L6-v2`
- FAISS vector search for relevant evidence
- Verdict generation via Google Gemini (Gemini Pro or Flash)
- Streamlit frontend for user interaction

---

## 📂 Project Structure

```
├── app.py # Streamlit UI
├── data/ # Contains facts CSV and index files
├── src/
│ ├── claim_extractor.py
│ ├── retriever.py
│ ├── fact_checker.py
│ └── embedder.py
├── utils.py
├── .env # Your Google API Key (not committed)
└── requirements.txt
```
---

## ⚙️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/DattatrayBodake25/ai-powered-fact-checker.git
   cd ai-powered-fact-checker
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Set up environment variables

Create a .env file:

ini

GOOGLE_API_KEY=your_gemini_api_key_here
Run the app


streamlit run app.py
📝 On first run, the app will automatically build a FAISS index from data/verified_facts.csv.

🌐 Streamlit Cloud Deployment Notes
Ensure data/verified_facts.csv is present in the repo.

The app rebuilds the index on deployment if missing.

📌 Tech Stack
LLM: Google Gemini Pro / Flash

Embeddings: SentenceTransformers (all-MiniLM-L6-v2)

Vector DB: FAISS

Frontend: Streamlit

📄 License
This project is for educational and demonstration purposes only.
---

Let me know if you'd like a version with demo screenshots or badges for GitHub Actions, Hugging Face, or Streamlit 
