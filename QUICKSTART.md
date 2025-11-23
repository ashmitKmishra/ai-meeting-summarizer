# Quick Start Guide - AI Meeting Summarizer

## 🚀 For Frontend Lead (Member 1)

You're responsible for the user interface. Your files are already set up!

### Your Files (DO NOT EDIT OTHER FILES):
- `src/app_ui.py` - Main application
- `src/components/` - All component files
  - `file_uploader.py`
  - `summary_display.py`
  - `sidebar.py`
  - `metrics_display.py`

### How to Run:

1. **Install Streamlit**:
   ```bash
   pip install streamlit
   ```

2. **Run the app**:
   ```bash
   cd "d:\MSU\Fall 2025\AI Fundamentals (CSE-3683-01)\Final_project"
   streamlit run src/app_ui.py
   ```

3. **Your app will open at**: http://localhost:8501

### What You Can Do Now:
✅ Upload files (audio/video)
✅ Display dummy data
✅ Test all UI components
✅ Customize styling in `app_ui.py`

### Next Steps:
- Test the file upload feature
- Adjust the UI layout if needed
- Add more visualization components
- **Later**: Connect to backend when Member 2 finishes `pipeline.py`

---

## 🤖 For AI Engineer (Member 2)

### Your Files:
- `src/pipeline.py` - Main AI pipeline
- `src/llm_utils.py` - Helper functions

### Your Goal:
Create a function `process_audio(file_path)` that:
1. Takes an audio/video file path
2. Transcribes it with Whisper
3. Summarizes with Gemini
4. Returns a JSON object

### Expected Return Format:
```python
{
    'title': 'Meeting Title',
    'date': '2025-11-23',
    'duration': '45 minutes',
    'participants': ['Speaker 1', 'Speaker 2'],
    'summary': 'Meeting summary text...',
    'action_items': [
        {'task': 'Task description', 'owner': 'Person', 'deadline': 'Date'}
    ],
    'key_topics': ['Topic 1', 'Topic 2'],
    'sentiment': 'Positive'
}
```

### Workflow:
```bash
# Work on your branch
git checkout -b ai-pipeline

# Install additional dependencies
pip install openai-whisper google-generativeai

# Edit your files
# src/pipeline.py
# src/llm_utils.py

# Test your function
python -c "from src.pipeline import process_audio; print(process_audio('test.mp3'))"

# Commit and push
git add src/pipeline.py src/llm_utils.py
git commit -m "Implement Whisper + Gemini pipeline"
git push origin ai-pipeline
```

---

## 📊 For Data Scientist (Member 3)

### Your Files:
- `src/baseline.py` - Regex baseline
- `src/evaluation.py` - Comparison metrics

### Your Goal:
1. **In `baseline.py`**: Create `get_regex_summary(text)` function
   - Use regex to extract action items, decisions, questions
   
2. **In `evaluation.py`**: Create `compare_results(ai_json, regex_list)` function
   - Compare AI results vs regex results
   - Calculate precision, recall, F1 score

### Workflow:
```bash
# Work on your branch
git checkout -b baseline-evaluation

# Edit your files
# src/baseline.py
# src/evaluation.py

# Test your functions
python -c "from src.baseline import get_regex_summary; print(get_regex_summary('TODO: Test task'))"

# Commit and push
git add src/baseline.py src/evaluation.py
git commit -m "Implement regex baseline and evaluation metrics"
git push origin baseline-evaluation
```

---

## 🔄 Integration Process

Once all members complete their parts:

1. **Member 2** completes `pipeline.py` with `process_audio()` function
2. **Member 1** updates `app_ui.py` to call the real pipeline:
   ```python
   from pipeline import process_audio
   
   # In the process button handler:
   result = process_audio(file_path)
   st.session_state.summary_data = result
   ```
3. **Member 3** adds evaluation comparison view to UI
4. Test integration on a shared branch
5. Merge all to `main`

---

## 📦 Dependencies by Member

### Member 1 (Frontend):
```bash
pip install streamlit pillow
```

### Member 2 (AI):
```bash
pip install openai-whisper google-generativeai python-dotenv
```

### Member 3 (Baseline):
```bash
pip install pandas numpy scikit-learn
```

---

## ⚠️ Avoiding Merge Conflicts

### The Golden Rule:
**Each person works ONLY on their assigned files!**

### File Ownership:
- ✅ Member 1: `app_ui.py`, `components/*.py`
- ✅ Member 2: `pipeline.py`, `llm_utils.py`
- ✅ Member 3: `baseline.py`, `evaluation.py`

### Git Best Practices:
```bash
# Always work on your own branch
git checkout -b your-branch-name

# Pull latest changes before starting
git pull origin main

# Commit often with clear messages
git commit -m "Add file upload validation"

# Push to your branch (not main!)
git push origin your-branch-name

# Create PR when ready to merge
```

---

## 🎯 Testing Checklist

### Frontend (Member 1):
- [ ] File upload works for all formats
- [ ] UI displays correctly
- [ ] Buttons are functional
- [ ] Export features work
- [ ] Responsive design on different screen sizes

### AI Pipeline (Member 2):
- [ ] Whisper transcribes audio correctly
- [ ] Gemini generates meaningful summaries
- [ ] Action items are extracted
- [ ] JSON format matches expected structure
- [ ] Error handling for invalid files

### Evaluation (Member 3):
- [ ] Regex extracts action items
- [ ] Metrics calculate correctly
- [ ] Comparison report is readable
- [ ] Handles edge cases (empty text, etc.)

---

## 🆘 Common Issues

### "Streamlit not found"
```bash
pip install streamlit --upgrade
```

### "Port 8501 is already in use"
```bash
# Use a different port
streamlit run src/app_ui.py --server.port 8502
```

### "Import errors"
Make sure you're in the project root:
```bash
cd "d:\MSU\Fall 2025\AI Fundamentals (CSE-3683-01)\Final_project"
```

### "Merge conflicts"
You edited someone else's file! Revert and stick to your assigned files.

---

## 📞 Quick Help

**Frontend issues?** → Ask Member 1
**AI/Pipeline issues?** → Ask Member 2
**Evaluation issues?** → Ask Member 3
**Git issues?** → Team meeting!

---

**Good luck! 🚀**
