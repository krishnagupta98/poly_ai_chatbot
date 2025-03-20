from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sentence_transformers import SentenceTransformer, util
import os

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Allow frontend requests

# Load SentenceTransformer for Semantic Search
retrieval_model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight & Fast

# Load Knowledge Base
def load_knowledge_base():
    if os.path.exists("knowledge_base.txt"):
        with open("knowledge_base.txt", "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]
    return []

knowledge_base = load_knowledge_base()
knowledge_embeddings = retrieval_model.encode(knowledge_base, convert_to_tensor=True)

# Function to Retrieve the Best Knowledge Match
def retrieve_knowledge(user_message):
    if not knowledge_base:
        return "I don't have enough knowledge yet."
    
    user_embedding = retrieval_model.encode(user_message, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(user_embedding, knowledge_embeddings)[0]
    best_match_idx = scores.argmax().item()
    
    return knowledge_base[best_match_idx]  # Return the closest factual answer

# Function to Generate a Response (Directly from Knowledge Base)
def generate_response(user_message):
    relevant_fact = retrieve_knowledge(user_message)
    
    # Return the retrieved fact directly
    return relevant_fact

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "")
        bot_reply = generate_response(user_message)
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"reply": f"An error occurred: {e}"}), 500

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)