from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sentence_transformers import SentenceTransformer, util
from spellchecker import SpellChecker
import os
import logging

#intialising flask 
app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("Starting Flask app...")

try:
    retrieval_model = SentenceTransformer("all-MiniLM-L6-v2")
    logger.info("SentenceTransformer model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading SentenceTransformer model: {e}")

# Loading Knowledge Base
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

#intialising spelling checker
spell = SpellChecker()

def correct_spelling(user_message):
    corrected_words = []
    for word in user_message.split():
        if spell.unknown([word]):
            candidates = spell.candidates(word)
            if candidates:
                corrected_word = max(candidates, key=spell.word_probability) 
                corrected_words.append(corrected_word)
            else:
                corrected_words.append(word)  
        else:
            corrected_words.append(word)
    corrected_message = ' '.join(corrected_words)
    return corrected_message

#loading the knowledge base
def retrieve_knowledge(user_message):
    if not knowledge_base:
        logger.warning("Knowledge base is empty.")
        return "I don't have enough knowledge yet."

    try:
        user_embedding = retrieval_model.encode(user_message, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(user_embedding, knowledge_embeddings)[0]
        best_match_idx = scores.argmax().item()
        logger.debug(f"Best match index: {best_match_idx}, Score: {scores[best_match_idx]}")
        return knowledge_base[best_match_idx]  
    except Exception as e:
        logger.error(f"Error retrieving knowledge: {e}")
        return "Error processing request."
    
#generating chatbot response
def generate_response(user_message):

    corrected_message = correct_spelling(user_message)
    relevant_fact = retrieve_knowledge(corrected_message)
    return relevant_fact

#api end point
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "")
        if not user_message:  
            logger.warning("Received empty user message.")
            return jsonify({"reply": "Please provide a message."}), 400
        
        logger.info(f"Received user message: {user_message}")
        bot_reply = generate_response(user_message)
        logger.info(f"Bot reply: {bot_reply}")
        return jsonify({"reply": bot_reply})
    except Exception as e:
        logger.error(f"Error in /chat route: {e}")
        return jsonify({"reply": "i am not well confident for this query . Please contact the institution."}), 500

@app.route("/")
def home():
    logger.info("Home page accessed.")
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting app on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
try:
    retrieval_model = SentenceTransformer("all-MiniLM-L6-v2")
    logger.info("SentenceTransformer model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading SentenceTransformer model: {e}")

# Loading Knowledge Base
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

# Initialize the  spelling checker
spell = SpellChecker()

def correct_spelling(user_message):
    corrected_message = ' '.join([spell.candidates(word).pop() if spell.unknown([word]) else word for word in user_message.split()])
    return corrected_message

def retrieve_knowledge(user_message):
    if not knowledge_base:
        logger.warning("Knowledge base is empty.")
        return "I don't have enough knowledge yet."

    try:
        user_embedding = retrieval_model.encode(user_message, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(user_embedding, knowledge_embeddings)[0]
        best_match_idx = scores.argmax().item()
        logger.debug(f"Best match index: {best_match_idx}, Score: {scores[best_match_idx]}")
        return knowledge_base[best_match_idx]  
    except Exception as e:
        logger.error(f"Error retrieving knowledge: {e}")
        return "Error processing request."

def generate_response(user_message):
    corrected_message = correct_spelling(user_message)
    relevant_fact = retrieve_knowledge(corrected_message)
    return relevant_fact

#the end point
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
    port = int(os.environ.get("PORT", 5000))  
    logger.info(f"Starting app on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)