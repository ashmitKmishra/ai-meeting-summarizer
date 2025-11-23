# Meeting-to-Action Summarizer (Audio → Key Points, Tasks, Next Steps)

Turn messy meeting or lecture audio into a clean, actionable brief:

- **Executive summary**
- **Key points / decisions**
- **Action items with owners and due dates**

This project combines **local speech recognition** with a **Gemini-based LLM pipeline** to extract, structure, and validate meeting intelligence in a reproducible way.

---

## 🚀 What this project does

Given an audio file (e.g., `.wav`, `.mp3`), the system:

1. **Transcribes audio locally** using `faster-whisper` (a fast Whisper implementation for CPU/GPU).
2. **Cleans & structures the transcript** into:
   - High-level **summary**
   - **Key points & decisions**
   - **Action items** with:
     - `description`
     - `owner`
     - `due_date`
3. **Validates the output** against a strict **JSON schema** to reduce hallucinations and enforce consistency.
4. Optionally **compares**:
   - A **deterministic baseline** (regex/heuristics only)
   - The **Gemini-enhanced pipeline**
5. Presents the results via:
   - A **CLI**
   - And a simple **frontend** (Streamlit or React, depending on implementation)

---

## 🧠 AI & Data

**ASR (Speech-to-Text):**

- [`faster-whisper`](https://github.com/guillaumekln/faster-whisper) for local transcription.

**LLM (Summarization & Extraction):**

- **Gemini API** (e.g., Gemini 1.5) for:
  - Summaries
  - Key points & decisions
  - Action items in **JSON**.

**Python libraries (planned/used):**

- `numpy`, `pandas`
- `regex`
- `dateparser` (for fuzzy due dates like “next Monday”)
- `tqdm`
- Optional: `pyannote` (speaker diarization), `matplotlib` (plots & evaluation charts)

**Frontend (one of):**

- **Streamlit app** (Python), or
- **React-based UI** (JavaScript)

**Data:**

- Short, consented recordings from team meetings/lectures
- Optional small public samples for testing and evaluation

---

## 📐 Project goals

- Build an **end-to-end meeting summarizer** that:
  - Works on realistic meeting/lecture audio.
  - Produces **structured JSON** that can be consumed by other tools (calendars, task managers, CRMs, etc.).
- **Quantify the value of LLMs** versus a non-LLM baseline by comparing:
  - Precision / recall / F1 of **action-item extraction**
  - Runtime / latency of each pipeline

---

## 🏗️ High-level architecture

```text
Audio File
   │
   ├──▶ ASR (faster-whisper)
   │        └── raw transcript + segments
   │
   ├──▶ Baseline Extractor (regex/heuristics)
   │        └── baseline JSON (summary, points, actions)
   │
   └──▶ Gemini Pipeline
            ├── prompt templates
            ├── JSON schema-constrained output
            └── validated JSON (summary, points, actions)
