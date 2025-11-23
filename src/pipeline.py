import os
import json
import whisper
import google.generativeai as genai
from dotenv import load_dotenv

# --- CONFIGURATION ---
# 1. Load the secret key from the .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file.")
    print("👉 Please create a file named .env and add: GEMINI_API_KEY=your_actual_key")
else:
    genai.configure(api_key=API_KEY)

class MeetingPipeline:
    def __init__(self):
        """
        Initializes the pipeline with Model Auto-Detection.
        """
        print("🏗️  Initializing MeetingPipeline...")
        
        # 1. Setup Whisper (Local Ear)
        print("   -> Loading Whisper model (base size)...")
        # fp16=False prevents warnings on Mac CPUs
        self.transcriber = whisper.load_model("base")
        
        # 2. Setup Gemini (Cloud Brain) with Auto-Detect
        print("   -> Detecting available Gemini models...")
        self.model_name = self._get_working_model()
        print(f"   -> Selected Model: {self.model_name}")
        
        self.gemini_model = genai.GenerativeModel(self.model_name)
        print("✅ Models loaded successfully.")

    def _get_working_model(self):
        """
        Asks Google: 'Which models does my API key have access to?'
        Returns the best available one.
        """
        try:
            # List all models your key can see
            available_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
            
            # Preference list: Try these in order (Cheapest/Fastest first)
            preferences = [
                'models/gemini-1.5-flash',
                'models/gemini-1.5-flash-latest',
                'models/gemini-1.5-flash-001',
                'models/gemini-1.5-pro',
                'models/gemini-pro',
                'models/gemini-1.0-pro'
            ]

            # 1. Check if any of our preferred models exist
            for pref in preferences:
                if pref in available_models:
                    return pref
            
            # 2. If none match, just grab the first valid text model we found
            if available_models:
                print(f"⚠️ Preferred models not found. Falling back to: {available_models[0]}")
                return available_models[0]
                
            raise ValueError("No text generation models found for this API key.")
            
        except Exception as e:
            print(f"❌ Error listing models: {e}")
            # Absolute fallback
            return "models/gemini-pro"

    def process_meeting(self, audio_path: str):
        """
        Main function: Audio File -> Structured JSON
        """
        if not os.path.exists(audio_path):
            return {"error": f"Audio file not found at: {audio_path}"}

        # --- STEP 1: TRANSCRIPTION ---
        print(f"🎧 Transcribing {audio_path}...")
        try:
            # fp16=False is required for Mac/CPU
            result = self.transcriber.transcribe(audio_path, fp16=False)
            transcript_text = result["text"]
            print("   -> Transcription complete.")
        except Exception as e:
            return {"error": f"Whisper Transcription Failed: {str(e)}"}

        # --- STEP 2: GEMINI ANALYSIS ---
        print(f"🧠 Sending transcript to {self.model_name}...")
        
        prompt = f"""
        You are an expert Project Manager AI. Analyze the following meeting transcript.
        
        TRANSCRIPT:
        {transcript_text}
        
        OUTPUT FORMAT (Strict JSON only):
        {{
            "executive_summary": "String...",
            "key_decisions": ["Decision 1", "Decision 2"],
            "action_items": [
                {{
                    "task": "Task description",
                    "owner": "Name or Unassigned",
                    "due_date": "Date or TBD"
                }}
            ]
        }}
        """

        try:
            # Generate content requesting JSON mime type
            response = self.gemini_model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(response_mime_type="application/json")
            )
            
            # Parse response text into a Python Dictionary
            parsed_json = json.loads(response.text)
            return parsed_json
            
        except Exception as e:
            print(f"❌ Raw Gemini Error: {e}")
            return {"error": f"Gemini Analysis Failed. Check your API key quota."}

# --- TESTING BLOCK ---
if __name__ == "__main__":
    test_file = "data/test_audio.mp3"
    
    if not os.path.exists(test_file):
        print(f"\n⚠️  Test file missing: {test_file}")
        print("Please put a file named 'test_audio.mp3' in the 'data' folder.")
    else:
        pipeline = MeetingPipeline()
        result = pipeline.process_meeting(test_file)
        
        print("\n" + "="*40)
        print("🤖 AI PIPELINE RESULTS")
        print("="*40)
        print(json.dumps(result, indent=2))