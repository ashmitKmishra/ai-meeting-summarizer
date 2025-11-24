# CODE COPIED FROM BRANCH: "CHATBOT". Made some changes to integrate it with the project.

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load Environment
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

def ask_meeting_assistant(question, transcript_text):
    """
    Sends the transcript + user question to Gemini.
    Adapted from the standalone chatbot script.
    """
    if not transcript_text:
        return "Error: No transcript available to answer questions. Please process a file first."

    # We use the same model detection logic as your pipeline to avoid 404s
    # defaulting to a safe model if specific 2.5 detection isn't needed
    model = genai.GenerativeModel('gemini-1.5-flash') 

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
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"