import streamlit as st
import os
import time
from pipeline import MeetingPipeline
import history_manager

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="MeetingMind AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SVG ICONS (Professional Look) ---
def get_icon(name):
    icons = {
        "mic": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>""",
        "history": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 8v13H3V8"/><path d="M1 3h22v5H1z"/><path d="M10 12h4"/></svg>""",
        "delete": "🗑️", 
        "upload": """<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>""",
        "whisper": """<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 10v3"/><path d="M6 6v11"/><path d="M10 3v18"/><path d="M14 8v7"/><path d="M18 5v13"/><path d="M22 10v4"/></svg>""",
        "brain": """<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/></svg>""",
        "file": """<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>"""
    }
    return icons.get(name, "")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .stButton>button {
        background-color: #b0c3ee;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.2s;
    }
    .stButton>button:hover { background-color: #1D4ED8; transform: scale(1.02); }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        text-align: center;
    }
    .step-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        height: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .step-icon { margin-bottom: 10px; }
    h1, h2, h3, h4, p { color: #0F172A; font-family: 'Helvetica Neue', sans-serif; }
    .highlight { color: #2563EB; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- DIALOG: MEETING DETAILS POP-UP ---
@st.dialog("Meeting Details", width="large")
def show_meeting_details(item):
    st.write(f"**Date:** {item['date']}")
    st.write(f"**File:** {item['filename']}")
    st.write("---")
    
    # ADDED "Key Decisions" tab here
    t1, t2, t3, t4 = st.tabs(["📝 Summary", "💡 Decisions", "✅ Actions", "📜 Transcript"])
    
    with t1:
        st.info(item.get('summary', 'No summary available'))
            
    with t2:
        decisions = item.get('decisions', [])
        if decisions:
            for d in decisions:
                st.markdown(f"- {d}")
        else:
            st.warning("No key decisions found.")

    with t3:
        actions = item.get('actions', [])
        if actions:
            st.dataframe(actions, use_container_width=True)
        else:
            st.warning("No action items found.")
            
    with t4:
        st.text_area("Full Transcript", item.get('transcript', 'No transcript saved'), height=300)

# --- HELPER: RENDER METRICS ---
def render_metrics():
    stats = history_manager.get_stats()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="metric-card"><h3>Total Meetings</h3><h2 class="highlight">{stats['total_meetings']}</h2></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card"><h3>Minutes Analyzed</h3><h2 class="highlight">{stats['total_minutes']}</h2></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card"><h3>Est. Hours Saved</h3><h2 class="highlight">{stats['hours_saved']}</h2></div>""", unsafe_allow_html=True)

# --- SIDEBAR: HISTORY ---
with st.sidebar:
    # Use Markdown for Title with Icon
    st.markdown(f"### {get_icon('history')} Meeting History", unsafe_allow_html=True)
    st.write("---")
    
    history = history_manager.load_history()
    
    if not history:
        st.info("No meetings processed yet.")
    else:
        for item in history:
            col_text, col_del = st.columns([0.8, 0.2])
            
            # Button to open details
            if col_text.button(f"{item['date']} \n {item['filename'][:15]}...", key=f"btn_{item['id']}"):
                show_meeting_details(item)
            
            # Delete button
            if col_del.button("🗑️", key=f"del_{item['id']}", help="Delete this record"):
                history_manager.delete_history_item(item['id'])
                st.rerun()

# --- MAIN PAGE ---

# 1. Header with SVG Icon
st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        {get_icon('mic')}
        <h1 style="margin: 0; padding: 0;">MeetingMind</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("### Turn Audio into Actionable Intelligence")

# 2. Live Metrics Container (This will allow us to refresh it later)
metrics_placeholder = st.empty()
with metrics_placeholder.container():
    render_metrics()

st.write("---")

# 3. Upload Section
uploaded_file = st.file_uploader("Upload Meeting Audio", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    if st.button("🚀 Process Meeting", use_container_width=True):
        
        # Save temp
        temp_dir = "data"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        status = st.status("Processing...", expanded=True)
        
        try:
            status.write("🏗️ Initializing AI Pipeline...")
            pipeline = MeetingPipeline()
            
            status.write("🎧 Transcribing (Whisper)...")
            prog = status.progress(10)
            
            # Fake progress for UX
            for i in range(10, 50, 10):
                time.sleep(0.2)
                prog.progress(i)
                
            result = pipeline.process_meeting(file_path)
            
            if "error" in result:
                status.update(label="Error!", state="error")
                st.error(result["error"])
            else:
                prog.progress(100)
                status.write("💾 Saving results...")
                
                # Retrieve transcript
                base_name = os.path.splitext(uploaded_file.name)[0]
                transcript_path = os.path.join("output", f"{base_name}_transcript.txt")
                with open(transcript_path, "r") as t:
                    transcript_text = t.read()
                
                # Save to History
                history_manager.save_to_history(uploaded_file.name, result, transcript_text)
                
                # LIVE UPDATE: Refresh metrics immediately
                with metrics_placeholder.container():
                    render_metrics()
                
                status.update(label="Complete!", state="complete", expanded=False)
                
                # RESTORED 4 TABS HERE
                t1, t2, t3, t4 = st.tabs(["📝 Summary", "💡 Decisions", "✅ Actions", "📜 Transcript"])
                
                with t1: st.info(result["executive_summary"])
                
                with t2:
                    if result["key_decisions"]:
                        for d in result["key_decisions"]:
                            st.markdown(f"- {d}")
                    else:
                        st.info("No key decisions detected.")
                        
                with t3: st.dataframe(result["action_items"], use_container_width=True)
                with t4: st.text_area("Raw Text", transcript_text, height=200)

        except Exception as e:
            st.error(f"Error: {e}")

st.write("---")

# 4. "How it Works" - Beautiful Grid Layout
st.markdown("### How it works")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""<div class="step-card"><div class="step-icon">{get_icon('upload')}</div><h4>1. Upload</h4><p>Upload your MP3/WAV file safely.</p></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="step-card"><div class="step-icon">{get_icon('whisper')}</div><h4>2. Transcribe</h4><p>Whisper converts speech to text locally.</p></div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="step-card"><div class="step-icon">{get_icon('brain')}</div><h4>3. Analyze</h4><p>Gemini extracts tasks & summaries.</p></div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="step-card"><div class="step-icon">{get_icon('file')}</div><h4>4. Report</h4><p>View structured insights instantly.</p></div>""", unsafe_allow_html=True)