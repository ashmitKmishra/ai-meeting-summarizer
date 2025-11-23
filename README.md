# AI Meeting Summarizer 🎙️

An intelligent meeting assistant that transforms your meeting recordings into actionable insights using AI-powered transcription and summarization.

## 🌟 Features

- **Automatic Transcription**: Convert audio/video recordings to text using Whisper AI
- **Smart Summarization**: Generate concise meeting summaries with Gemini AI
- **Action Item Extraction**: Automatically identify and list action items
- **Speaker Identification**: Detect and label different speakers
- **Sentiment Analysis**: Understand the tone and mood of discussions
- **Multiple Export Formats**: Download summaries as JSON, TXT, or email them

## 📁 Project Structure

```
Final_project/
├── src/
│   ├── app_ui.py              # Main Streamlit application (FRONTEND LEAD)
│   ├── components/            # UI components (FRONTEND LEAD)
│   │   ├── __init__.py
│   │   ├── file_uploader.py   # File upload component
│   │   ├── summary_display.py # Summary display component
│   │   ├── sidebar.py         # Sidebar navigation
│   │   └── metrics_display.py # Metrics and stats
│   ├── pipeline.py            # Whisper & Gemini pipeline (AI ENGINEER)
│   ├── llm_utils.py           # LLM utilities (AI ENGINEER)
│   ├── baseline.py            # Regex baseline (DATA SCIENTIST)
│   └── evaluation.py          # Comparison metrics (DATA SCIENTIST)
├── static/                    # Static assets (CSS, images)
├── uploads/                   # Uploaded files storage
├── requirements.txt           # Python dependencies
├── .streamlit/                # Streamlit configuration
│   └── config.toml
└── README.md                  # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository** (or navigate to the project folder):
   ```bash
   cd "d:\MSU\Fall 2025\AI Fundamentals (CSE-3683-01)\Final_project"
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   .\venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Run the Streamlit app:
```bash
streamlit run src/app_ui.py
```

The application will open in your default web browser at `http://localhost:8501`

## 👥 Team Responsibilities

### 👤 Member 1: Frontend Lead
- **Files**: `src/app_ui.py`, `src/components/`
- **Goal**: Build the Streamlit dashboard with file upload and display functionality
- **Branch**: `ui` (work on this branch to avoid merge conflicts)

### 👤 Member 2: AI Engineer
- **Files**: `src/pipeline.py`, `src/llm_utils.py`
- **Goal**: Implement Whisper & Gemini pipeline with `process_audio(file)` function
- **Branch**: `ai-pipeline`

### 👤 Member 3: Data Scientist
- **Files**: `src/baseline.py`, `src/evaluation.py`
- **Goal**: Create regex baseline and comparison metrics
- **Branch**: `baseline-evaluation`

## 🔄 Git Workflow

To avoid merge conflicts:

1. **Create your feature branch**:
   ```bash
   git checkout -b <your-branch-name>
   ```

2. **Work only on your assigned files**

3. **Commit frequently**:
   ```bash
   git add <your-files>
   git commit -m "Descriptive message"
   ```

4. **Push to your branch**:
   ```bash
   git push origin <your-branch-name>
   ```

5. **Create a Pull Request** to merge into `main` when ready

## 📝 Usage

1. **Upload File**: Select an audio or video recording of your meeting
2. **Process**: Click the "Process Meeting" button
3. **Review**: View the generated summary, action items, and key topics
4. **Export**: Download the summary in your preferred format

## 🎨 Supported File Formats

### Audio
- MP3
- WAV
- M4A
- OGG

### Video
- MP4
- AVI
- MOV
- MKV

## 🔧 Configuration

Edit `.streamlit/config.toml` to customize:
- Theme colors
- Font sizes
- Server settings
- Maximum upload file size

## 📊 Future Enhancements

- [ ] Real-time transcription
- [ ] Integration with calendar apps
- [ ] Multi-language support
- [ ] Speaker diarization improvements
- [ ] Custom prompt templates
- [ ] Meeting comparison analytics
- [ ] Team collaboration features

## 🐛 Troubleshooting

### Streamlit not found
```bash
pip install streamlit --upgrade
```

### Port already in use
```bash
streamlit run src/app_ui.py --server.port 8502
```

### Import errors
Make sure you're in the project root directory and have installed all requirements.

## 📄 License

This project is created for educational purposes as part of CSE-3683-01.

## 🤝 Contributing

1. Follow the team's assigned file ownership
2. Use descriptive commit messages
3. Test your changes before pushing
4. Create pull requests for review

## 📧 Contact

For questions or issues, contact the team:
- Frontend: Member 1
- Backend: Member 2
- Evaluation: Member 3

---

**Built with ❤️ by Team 5PPL**
