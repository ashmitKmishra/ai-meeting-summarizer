# AI Meeting Summarizer

Transform your meeting recordings into actionable insights using AI-powered transcription and summarization.

## 🌟 Features

- 🎤 Automatic transcription with Whisper AI
- 📝 Smart summarization with Gemini AI  
- ✅ Action item extraction
- 👥 Speaker identification
- 😊 Sentiment analysis
- 📊 Export summaries (JSON, TXT)

## 🚀 Quick Start

```bash
# Install dependencies
pip install streamlit

# Run the app
streamlit run src/app_ui.py
```

Visit http://localhost:8501

## 📁 Project Structure

- `src/app_ui.py` - Main Streamlit application
- `src/components/` - UI components
- `src/pipeline.py` - AI processing pipeline
- `src/baseline.py` - Regex baseline for comparison
- `src/evaluation.py` - Evaluation metrics

## 👥 Team

- **Frontend Lead**: Streamlit dashboard & UI components
- **AI Engineer**: Whisper + Gemini integration  
- **Data Scientist**: Baseline & evaluation metrics

## 📖 Documentation

See [README.md](README.md) for full documentation and [QUICKSTART.md](QUICKSTART.md) for team-specific instructions.

---

Built with ❤️ for CSE-3683-01
