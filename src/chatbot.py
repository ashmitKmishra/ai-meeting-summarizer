import os
import sys
import requests
import json  # Import json for cleaner error printing
from dotenv import load_dotenv

# Load .env file if it exists, then fall back to system environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY is not set in environment variables or .env file.")
    sys.exit(1)

# FIX 1: Corrected to the official Gemini API v1 endpoint and a current Gemini model
GEMINI_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-pro:generateContent"


def ask_gemini(question, transcript_text):
    full_prompt = (
        f"You are a meeting assistant. Use the transcription below to answer user questions.\n\n"
        f"TRANSCRIPT:\n{transcript_text}\n\n"
        f"USER QUESTION: {question}"
    )

    # FIX 2 & 3: Updated payload structure and increased maxOutputTokens
    # The token limit is increased from 512 to 2048 to prevent the MAX_TOKENS error
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": full_prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048,  # Increased output limit
            "candidateCount": 1
        }
    }

    headers = {
        "Content-Type": "application/json",
        # FIX 4: Changed authentication to use x-goog-api-key header
        "x-goog-api-key": GEMINI_API_KEY
    }

    try:
        response = requests.post(GEMINI_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
    
    except requests.exceptions.RequestException as e:
        return f"Error: An HTTP request error occurred: {e}"

    data = response.json()

    # FIX 5: Added robust error handling for MAX_TOKENS and missing text
    try:
        candidate = data["candidates"][0]
        finish_reason = candidate.get("finishReason")
        
        # Check for the MAX_TOKENS condition
        if finish_reason == "MAX_TOKENS":
            # Check if any partial text was generated
            parts = candidate.get("content", {}).get("parts", [])
            generated_text = parts[0].get("text") if parts and "text" in parts[0] else None
            
            # Print usage metadata for debugging
            usage = data.get("usageMetadata", {})
            
            if generated_text:
                return (
                    f"⚠️ Warning: Response was truncated (MAX_TOKENS). "
                    f"Usage: {usage.get('totalTokenCount')} tokens. Partial answer: {generated_text}"
                )
            else:
                return (
                    f"❌ Error: Model hit max token limit (2048) before generating output. "
                    f"Usage: {usage.get('totalTokenCount')} tokens. "
                    f"The model may have used tokens for internal reasoning (thoughtsTokenCount)."
                )

        # Extract and return the successfully generated text
        return candidate["content"]["parts"][0]["text"]

    except (KeyError, IndexError, TypeError):
        # Fallback for genuinely unexpected JSON format
        return f"Error: Unexpected response format: {json.dumps(data, indent=2)}"


def main():
    transcript_path = sys.argv[1] if len(sys.argv) > 1 else None

    if not transcript_path or not os.path.exists(transcript_path):
        print("Usage: python chatbot.py <transcription_file.txt>")
        sys.exit(1)

    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript_text = f.read()
    except Exception as e:
        print(f"Error reading transcript file: {e}")
        sys.exit(1)

    print("Meeting Transcript Chatbot (Gemini API)")
    print("Ask questions about the meeting. Type 'exit' to quit.\n")

    while True:
        try:
            user_q = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if user_q.lower().strip() in ["exit", "quit"]:
            print("Goodbye.")
            break

        answer = ask_gemini(user_q, transcript_text)
        print(f"\nAssistant: {answer}\n")


if __name__ == "__main__":
    main()