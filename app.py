from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sentence_transformers import SentenceTransformer, util
import os
import logging

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Allow frontend requests

# Setup logging
logging.basicConfig(level=logging.DEBUG)  # Log everything (DEBUG level)
logger = logging.getLogger(__name__)

logger.info("Starting Flask app...")

# Load SentenceTransformer for Semantic Search
try:
    retrieval_model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight & Fast
    logger.info("SentenceTransformer model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading SentenceTransformer model: {e}")

# Load Knowledge Base
def load_knowledge_base():
    try:
        if os.path.exists("knowledge_base.txt"):
            with open("knowledge_base.txt", "r", encoding="utf-8") as file:
                data = [line.strip() for line in file.readlines()]
                logger.info(f"Knowledge base loaded with {len(data)} entries.")
                return data
        logger.warning("Knowledge base file not found.")
        return []
    except Exception as e:
        logger.error(f"Error loading knowledge base: {e}")
        return []

knowledge_base = load_knowledge_base()
knowledge_embeddings = retrieval_model.encode(knowledge_base, convert_to_tensor=True) if knowledge_base else None

# Function to Retrieve the Best Knowledge Match
def retrieve_knowledge(user_message):
    if not knowledge_base:
        logger.warning("Knowledge base is empty.")
        return "I don't have enough knowledge yet."

    try:
        user_embedding = retrieval_model.encode(user_message, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(user_embedding, knowledge_embeddings)[0]
        best_match_idx = scores.argmax().item()
        logger.debug(f"Best match index: {best_match_idx}, Score: {scores[best_match_idx]}")
        return knowledge_base[best_match_idx]  # Return the closest factual answer
    except Exception as e:
        logger.error(f"Error retrieving knowledge: {e}")
        return "Error processing request."

# Function to Generate a Response (Directly from Knowledge Base)
def generate_response(user_message):
    relevant_fact = retrieve_knowledge(user_message)
    return relevant_fact

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "")
        logger.info(f"Received user message: {user_message}")
        bot_reply = generate_response(user_message)
        logger.info(f"Bot reply: {bot_reply}")
        return jsonify({"reply": bot_reply})
    except Exception as e:
        logger.error(f"Error in /chat route: {e}")
        return jsonify({"reply": f"An error occurred: {e}"}), 500

@app.route("/")
def home():
    logger.info("Home page accessed.")
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Change to match Render's port
    logger.info(f"Starting app on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
