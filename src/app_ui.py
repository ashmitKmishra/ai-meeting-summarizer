import streamlit as st
import os
import time
from pipeline import MeetingPipeline
import history_manager
import chat_engine  # Import the chatbot module

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="MeetingMind AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE SETUP ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_transcript" not in st.session_state:
    st.session_state.current_transcript = ""

# --- SVG ICONS ---
def get_icon(name):
    icons = {
        "mic": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>""",
        "history": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 8v13H3V8"/><path d="M1 3h22v5H1z"/><path d="M10 12h4"/></svg>""",
        "delete": "🗑️", 
        "upload": """<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>""",
        "whisper": """<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 10v3"/><path d="M6 6v11"/><path d="M10 3v18"/><path d="M14 8v7"/><path d="M18 5v13"/><path d="M22 10v4"/></svg>""",
        "brain": """<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/></svg>""",
        "file": """<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>""",
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

# --- HELPER: RENDER CHAT INTERFACE ---
# We extract this so we can reuse it in both the main dialog and history dialog
def render_chat_interface():
    st.caption("Ask questions about this meeting.")
    
    if not st.session_state.current_transcript:
        st.warning("No transcript loaded.")
        return

    # Display Chat History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Ask a question..."):
        # 1. User message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # 2. AI Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.ask_meeting_assistant(prompt, st.session_state.current_transcript)
                st.write(response)
        
        # 3. Save to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun() # Force refresh to show new message

# --- DIALOG: MAIN CHATBOT BUTTON ---
@st.dialog("💬 Chat with Transcript", width="large")
def show_chatbot_dialog():
    if not st.session_state.current_transcript:
        st.warning("Please upload and process a meeting first!")
        if st.button("Close"):
            st.rerun()
        return
    render_chat_interface()

# --- DIALOG: MEETING DETAILS (FIXED: Integrated Chat Tab) ---
@st.dialog("Meeting Details", width="large")
def show_meeting_details(item):
    st.write(f"**Date:** {item['date']}")
    st.write(f"**File:** {item['filename']}")
    
    # Switch context to THIS meeting immediately when viewing details
    # This ensures if they click "Chat", they chat with THIS meeting, not the old one.
    if st.session_state.current_transcript != item.get('transcript', ''):
        st.session_state.current_transcript = item.get('transcript', '')
        st.session_state.chat_history = [] # Reset chat for new context

    st.write("---")
    
    # Added "💬 Chat" as the 5th tab here
    t1, t2, t3, t4, t5 = st.tabs(["📝 Summary", "💡 Decisions", "✅ Actions", "📜 Transcript", "💬 Chat"])
    
    with t1: st.info(item.get('summary', 'No summary available'))
    with t2:
        for d in item.get('decisions', []): st.markdown(f"- {d}")
    with t3: 
        if item.get('actions'): st.dataframe(item.get('actions'), use_container_width=True)
    with t4: st.text_area("Full Transcript", item.get('transcript', ''), height=300)
    
    # Render the chat interface directly inside this tab!
    with t5:
        render_chat_interface()

# --- HELPER: RENDER METRICS ---
def render_metrics():
    stats = history_manager.get_stats()
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"""<div class="metric-card"><h3>Total Meetings</h3><h2 class="highlight">{stats['total_meetings']}</h2></div>""", unsafe_allow_html=True)
    with c2: st.markdown(f"""<div class="metric-card"><h3>Minutes Analyzed</h3><h2 class="highlight">{stats['total_minutes']}</h2></div>""", unsafe_allow_html=True)
    with c3: st.markdown(f"""<div class="metric-card"><h3>Est. Hours Saved</h3><h2 class="highlight">{stats['hours_saved']}</h2></div>""", unsafe_allow_html=True)

# --- SIDEBAR: HISTORY ---
with st.sidebar:
    st.markdown(f"### {get_icon('history')} Meeting History", unsafe_allow_html=True)
    st.write("---")
    history = history_manager.load_history()
    
    if not history:
        st.info("No meetings processed yet.")
    else:
        for item in history:
            col_text, col_del = st.columns([0.8, 0.2])
            if col_text.button(f"{item['date']} \n {item['filename'][:15]}...", key=f"btn_{item['id']}"):
                show_meeting_details(item)
            if col_del.button("🗑️", key=f"del_{item['id']}"):
                history_manager.delete_history_item(item['id'])
                st.rerun()

# --- MAIN PAGE ---

# 1. HEADER
col_title, col_spacer, col_bot = st.columns([0.6, 0.3, 0.1])
with col_title:
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 10px;">
            {get_icon('mic')}
            <h1 style="margin: 0; padding: 0;">MeetingMind</h1>
        </div>
    """, unsafe_allow_html=True)

with col_bot:
    if st.button("💬", help="Chat with current meeting"):
        show_chatbot_dialog()

st.markdown("### Turn Audio into Actionable Intelligence")

# 2. METRICS
metrics_placeholder = st.empty()
with metrics_placeholder.container():
    render_metrics()

st.write("---")

# 3. UPLOAD
uploaded_file = st.file_uploader("Upload Meeting Audio", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    if st.button("🚀 Process Meeting", use_container_width=True):
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
            
            # Fake progress
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
                
                base_name = os.path.splitext(uploaded_file.name)[0]
                transcript_path = os.path.join("output", f"{base_name}_transcript.txt")
                with open(transcript_path, "r") as t:
                    transcript_text = t.read()
                
                # Update Session State
                st.session_state.current_transcript = transcript_text
                st.session_state.chat_history = [] 

                history_manager.save_to_history(uploaded_file.name, result, transcript_text)
                
                with metrics_placeholder.container():
                    render_metrics()
                
                status.update(label="Complete!", state="complete", expanded=False)
                
                # TABS
                t1, t2, t3, t4 = st.tabs(["📝 Summary", "💡 Decisions", "✅ Actions", "📜 Transcript"])
                with t1: st.info(result["executive_summary"])
                with t2: 
                    for d in result["key_decisions"]: st.markdown(f"- {d}")
                with t3: st.dataframe(result["action_items"], use_container_width=True)
                with t4: st.text_area("Raw Text", transcript_text, height=200)

        except Exception as e:
            st.error(f"Error: {e}")

st.write("---")

# 4. HOW IT WORKS
st.markdown("### How it works")
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"""<div class="step-card"><div class="step-icon">{get_icon('upload')}</div><h4>1. Upload</h4><p>Upload your MP3/WAV file safely.</p></div>""", unsafe_allow_html=True)
with c2: st.markdown(f"""<div class="step-card"><div class="step-icon">{get_icon('whisper')}</div><h4>2. Transcribe</h4><p>Whisper converts speech to text locally.</p></div>""", unsafe_allow_html=True)
with c3: st.markdown(f"""<div class="step-card"><div class="step-icon">{get_icon('brain')}</div><h4>3. Analyze</h4><p>Gemini extracts tasks & summaries.</p></div>""", unsafe_allow_html=True)
with c4: st.markdown(f"""<div class="step-card"><div class="step-icon">{get_icon('file')}</div><h4>4. Report</h4><p>View structured insights instantly.</p></div>""", unsafe_allow_html=True)