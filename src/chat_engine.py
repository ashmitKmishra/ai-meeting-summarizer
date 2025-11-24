# CODE COPIED FROM BRANCH: "CHATBOT". Made some changes to integrate it with the project.

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load Environment
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

def get_working_model():
    """
    Copied from pipeline.py: Auto-detects the best available model
    to prevent 404 errors with the API Key.
    """
    try:
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        # Preference list
        preferences = [
            'models/gemini-1.5-flash',
            'models/gemini-1.5-flash-latest',
            'models/gemini-1.5-flash-001',
            'models/gemini-1.5-pro',
            'models/gemini-pro',
            'models/gemini-1.0-pro'
        ]

        # Check preferences against available
        for pref in preferences:
            if pref in available_models:
                return pref
        
        # Fallback
        if available_models:
            return available_models[0]
            
        return "models/gemini-pro"
        
    except Exception as e:
        # If listing fails, guess the safest one
        return "models/gemini-pro"

def ask_meeting_assistant(question, transcript_text):
    """
    Sends the transcript + user question to Gemini.
    """
    if not transcript_text:
        return "Error: No transcript available. Please process a meeting first."

    try:
        # 1. Auto-detect the correct model (Fixes the 404)
        model_name = get_working_model()
        model = genai.GenerativeModel(model_name) 

        prompt = f"""
        You are a helpful Meeting Assistant. Use the transcription below to answer the user's question accurately.
        
        TRANSCRIPT:
        {transcript_text}
        
        USER QUESTION: {question}
        
        INSTRUCTIONS:
        - Answer based ONLY on the transcript.
        - If the answer is not in the text, say "I couldn't find that information in the meeting."
        - Keep answers concise and professional.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"