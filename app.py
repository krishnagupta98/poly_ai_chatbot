from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer, util
import os

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Allow frontend requests

# Load MiniLM Model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Load Knowledge Base
def load_knowledge_base():
    if os.path.exists("knowledge_base.txt"):
        with open("knowledge_base.txt", "r", encoding="utf-8") as file:
            return file.readlines()  # Read lines to compare similarity
    return []

knowledge_base = load_knowledge_base()

# Function to find the best response
def find_best_response(user_message):
    if not knowledge_base:
        return "I don't have enough knowledge yet."

    # Encode user message and knowledge base
    user_embedding = model.encode(user_message, convert_to_tensor=True)
    knowledge_embeddings = model.encode(knowledge_base, convert_to_tensor=True)

    # Find the most similar response
    similarity_scores = util.pytorch_cos_sim(user_embedding, knowledge_embeddings)[0]
    best_match_index = similarity_scores.argmax().item()

    return knowledge_base[best_match_index].strip()  # Return the best-matching response

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get user message
        user_message = request.json.get("message", "")

        # Find the best response from MiniLM
        bot_reply = find_best_response(user_message)

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"reply": f"An error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
