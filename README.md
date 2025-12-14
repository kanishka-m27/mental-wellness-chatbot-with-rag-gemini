# 🧠 MindConnect AI – Mental Wellness Assistant

MindConnect AI is a web-based mental wellness chatbot designed to provide supportive, empathetic, and context-aware responses for everyday stress and anxiety.  
The system uses **Retrieval-Augmented Generation (RAG)** to ensure responses stay grounded in curated mental wellness knowledge.

---

## 🚀 Features

- Interactive mental wellness chatbot
- Custom knowledge base using curated mental wellness notes
- Retrieval-Augmented Generation (RAG) with FAISS
- AI-powered responses using Google Gemini API
- Safe, empathetic, and context-aware replies
- Clean and responsive chat interface
- Typing indicator for improved user experience

---

## 🛠️ Tech Stack

**Frontend**
- HTML
- CSS
- JavaScript

**Backend**
- Python
- Flask

**AI & NLP**
- Google Gemini API
- LangChain

**Vector Database**
- FAISS

**Embeddings**
- HuggingFace sentence-transformers

---

## 📁 Project Structure
```text
mental-wellness-chatbot-with-rag-gemini/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│ └── notes.txt
│
├── static/
│ ├── style.css
│ └── script.js
│
├── templates/
│ └── index.html
```

---

## ⚙️ Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/kanishka-m27/mental-wellness-chatbot-with-rag-gemini.git
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Create a .env file and add:
```bash
GEMINI_API_KEY=your_api_key_here
HF_TOKEN=your_huggingface_token
```
4. Run the application
```bash
python app.py
```
5.  Open in Browser
```bash
 http://127.0.0.1:5000
```

## 🔐 Safety Note

This chatbot is not a medical or diagnostic tool.
It is intended only for general emotional support and educational purposes.

## 📌 Future Improvements

- Conversation memory
- Mood tracking and visual insights
- Deployment to cloud (Render / Hugging Face Spaces)
- Enhanced performance and latency optimization

## Author

Kanishka M
BCA Student | Aspiring Software Developer



