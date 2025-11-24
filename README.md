# MeetingMind: Automated Meeting Intelligence System

**MeetingMind** is a Python-based application that converts unstructured meeting and lecture audio into **structured, actionable intelligence**. It automates note-taking by generating executive summaries, extracting key decisions, and producing action items with owners and due dates.


---

## 🚀 Key Features

### 🔊 Automated Transcription  
- Uses **OpenAI Whisper (local CPU)** to convert audio to text.  
- Ensures privacy and eliminates cloud transcription costs.

### 🧠 Structured Intelligence  
- Sends transcripts to **Google Gemini API**.  
- Outputs **strict JSON** containing:
  - Executive summary  
  - Key points/decisions  
  - Action items with inferred owners & due dates  

### ✔️ Action Item Extraction  
- Identifies tasks, ownership, deadlines using contextual reasoning.

### 🗂️ Historical Archive  
- Stores all meetings locally in a persistent JSON database.  
- Tracks:
  - Total meetings analyzed  
  - Total hours of audio processed  
  - Estimated hours saved  


---
## 🧩 Technical Architecture

### 1. **Ingestion**
User uploads audio (MP3/WAV/M4A) via a **Streamlit** interface.

### 2. **Transcription Layer**
Runs **Whisper Base** locally on CPU (optimizations for Intel & Apple Silicon).

### 3. **Intelligence Layer**
Transcript sent to **Google Gemini API** with a strict JSON schema prompt.  
The backend:
- Validates schema
- Automatically detects available Gemini models  
- Prevents invalid model errors

### 4. **Persistence**
Outputs stored in: **data/history.json**
- **Includes timestamps, summaries, key decisions, and action items.**

---
## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.10 / 3.11 |
| Frontend | Streamlit |
| Speech Recognition | OpenAI Whisper (local) |
| LLM | Google Gemini API |
| Storage | Local JSON DB |
| Validation | JSON Schema |
| Config | python-dotenv |

---

## 🖥️ Installation & Local Setup

### 1. **Prerequisites**
Make sure Python and FFmpeg are installed.

**Mac:**
```bash
brew install ffmpeg
```
```bash
git clone https://github.com/yourusername/ai-meeting-summarizer.git
```
```bash
cd ai-meeting-summarizer
```
### 2. **Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
# or
.venv\Scripts\activate         # Windows
```
### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

