# Poly AI Chatbot

## Overview

Poly AI Chatbot is a virtual assistant designed to provide instant support and information about Government Polytechnic Dehradun. It is built using Flask, Natural Language Processing (NLP), and AI-based retrieval models to answer user queries accurately and efficiently.

## Features

- **Instant Responses:** Provides immediate answers to user queries.
- **Knowledge Base Integration:** Uses a predefined knowledge base for accurate information retrieval.
- **Spell Checker:** Corrects spelling errors in user queries.
- **AI-Powered Search:** Uses SentenceTransformer and cosine similarity for retrieving the best-matched responses.
- **User-Friendly Interface:** Simple and easy-to-use chatbot for students, faculty, and visitors.

## Technologies Used

- **Backend:** Python (Flask)
- **AI/NLP:** SentenceTransformer, SpellChecker
- **Frontend:** HTML, CSS, JavaScript
- **Database:** Knowledge base stored in a text file
- **Deployment:** Render, Vercel

## Project Structure

- `app.py`: Main Flask application handling chatbot interactions.
- `knowledge_base.txt`: Contains predefined responses for chatbot queries.
- `package-lock.json`: Package dependencies for frontend components.
- `render.yaml`: Configuration for deploying the chatbot on Render.
- `vercel.json`: Configuration for frontend deployment using Vercel.
- `README.md`: Documentation for the project.

## Setup & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/krishnagupta98/poly_ai_chatbot.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

## Deployment

- The backend is deployed using **Render**.
- The frontend is hosted on **Vercel**.

## Team Members

- **Krishna Gupta** - Backend & Deployment
- **Anshul Nautiyal** - Frontend (Structure) & Documentation
- **Satyendra Dangwal** - Designing & Presentation
- **Jaydeep Shah** - Frontend (Functionality)
- **Mohit Jha** - Literature Survey

## Future Improvements

- Voice Integration
- Advanced Analytics & Reporting
- Smarter Language Understanding
- Proactive Assistance

## Contact

For further inquiries, contact: [**nautiyalji25@gmail.com**](mailto\:nautiyalji25@gmail.com)

