from flask import Flask, render_template, request, jsonify
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains.question_answering import load_qa_chain
from dotenv import load_dotenv


app = Flask(__name__)

# 1. API keys 
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")


# 2. Load notes and build vector store 
notes_path = os.path.join(os.path.dirname(__file__), "data", "notes.txt")
with open(notes_path, "r", encoding="utf-8") as f:
    full_text = f.read()

splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
chunks = splitter.split_text(full_text)

embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=HF_TOKEN,
)

vector_store = FAISS.from_texts(chunks, embeddings)

# 3. Gemini LLM + QA chain 
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    temperature=0.7,
    google_api_key=GEMINI_API_KEY,
)

qa_chain = load_qa_chain(llm, chain_type="stuff")

# 4. Routes

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def get_bot_response():
    data = request.get_json()
    user_input = data.get("message", "")
    text = user_input.lower().strip()

    # For Simple fixed replies for common phrases (no Gemini call)
    simple_replies = {
        "thank you": "You're welcome! I'm glad I could support you 💙",
        "thanks": "You're welcome! 🌼",
        "bye": "Take care! I'm here whenever you want to talk again 💛",
        "goodbye": "Wishing you peace and comfort 💐",
        "ok": "Alright. If anything comes up later, feel free to share 🌸",
        "okay": "Okay. I'm here whenever you need to talk 🌼",
        "good": "I'm glad you're feeling good 😊 If anything ever bothers you, you can always share it here.",
        "fine": "Happy to hear you're feeling fine 💙",
        "happy": "That's lovely to hear! Keep enjoying your day 🌟",
        "great": "Awesome! I'm glad things feel great right now 😄",
        "love you": "Thank you for sharing that 💙 I'm just a chatbot, but I'm here to listen and support you."

    }
    for key, val in simple_replies.items():
        if key in text:
            return jsonify({"reply": val})

    # Retrieve relevant notes from vector store
    matching_chunks = vector_store.similarity_search(user_input, k=4)

    # Prompt: ONLY use docs, otherwise say you’re not sure
    question = f"""
You are a gentle, supportive mental wellness assistant.

You must answer ONLY using the information in the provided documents (context).
If the documents do NOT contain enough information to answer the user's question,
or if the question is unrelated to mental wellbeing (for example: programming, math,
arrays, data structures, etc.), reply exactly like this:

"I'm not sure about that topic, but I'm mainly here to support mental wellbeing."

User message: {user_input}

Using ONLY the given documents, do this:
- Respond in a short, kind, empathetic way.
- If they ask "what is ...", explain briefly.
-If the user sounds neutral or positive (for example: good, fine, okay, happy),just respond briefly and encouragingly
- Suggest 1–2 simple, practical coping ideas based on the documents.
- Do NOT give any medical diagnosis.
- If the message seems very dark or crisis-like, gently suggest talking to a trusted person,
  a professional, or a local helpline.
"""

    try:
         output = qa_chain.invoke({"question": question, "input_documents": matching_chunks})
         reply = output.strip()
    except Exception as e:
        print("Error:", e)
        reply = "I'm here for you, but something went wrong on my side. Please try again in a moment."

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
