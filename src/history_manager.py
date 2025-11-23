import os
import json
from datetime import datetime

HISTORY_FILE = "data/history.json"

def load_history():
    """Loads the history from the JSON file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_to_history(filename, analysis_json, transcript_text):
    """Saves a new meeting entry."""
    history = load_history()
    
    # Estimate duration based on word count (avg 150 words/min)
    word_count = len(transcript_text.split())
    estimated_minutes = round(word_count / 150, 2)
    
    entry = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "filename": filename,
        "duration_minutes": estimated_minutes,
        "summary": analysis_json.get("executive_summary", "No summary"),
        "decisions": analysis_json.get("key_decisions", []),
        "actions": analysis_json.get("action_items", [])
    }
    
    # Prepend to list (newest first)
    history.insert(0, entry)
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)
    
    return entry

def get_stats():
    """Calculates dashboard stats."""
    history = load_history()
    total_meetings = len(history)
    total_minutes = sum(h.get("duration_minutes", 0) for h in history)
    
    return {
        "total_meetings": total_meetings,
        "total_minutes": round(total_minutes, 1),
        "hours_saved": round(total_minutes / 60, 1) # Rough estimate
    }