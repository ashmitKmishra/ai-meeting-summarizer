import streamlit as st
import os
import time
import json
from pipeline import MeetingPipeline
import history_manager

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="MeetingMind AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS (For that clean Blue/White look) ---
st.markdown("""
    <style>
    .main {
        background-color: #FFFFFF;
    }
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #0F172A;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .highlight {
        color: #2563EB;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: HISTORY ---
with st.sidebar:
    st.title("🗄️ Meeting History")
    history = history_manager.load_history()
    
    if not history:
        st.info("No meetings processed yet.")
    else:
        for item in history:
            with st.expander(f"{item['date']} - {item['filename']}"):
                st.write(f"**Duration:** {item['duration_minutes']} mins")
                st.write(item['summary'])

# --- MAIN PAGE: HEADER & STATS ---
st.title("🎙️ MeetingMind")
st.markdown("### Turn Audio into Actionable Intelligence")

# Display Stats Dashboard
stats = history_manager.get_stats()
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Total Meetings</h3>
        <h2 class="highlight">{stats['total_meetings']}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Minutes Analyzed</h3>
        <h2 class="highlight">{stats['total_minutes']}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Est. Hours Saved</h3>
        <h2 class="highlight">{stats['hours_saved']}</h2>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- SECTION: UPLOAD & PROCESS ---
col_upload, col_info = st.columns([2, 1])

with col_info:
    st.info("""
    **How it works:**
    1. 📤 **Upload** an MP3/WAV file.
    2. 🎧 **Whisper** transcribes the audio locally.
    3. 🧠 **Gemini** extracts insights & tasks.
    4. 📊 **View** structured reports below.
    """)

with col_upload:
    uploaded_file = st.file_uploader("Upload Meeting Audio", type=["mp3", "wav", "m4a"])

    if uploaded_file is not None:
        if st.button("🚀 Process Meeting", use_container_width=True):
            
            # 1. Save file temporarily
            temp_dir = "data"
            os.makedirs(temp_dir, exist_ok=True)
            file_path = os.path.join(temp_dir, uploaded_file.name)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 2. Initialize Status Container (The "Log" view)
            status_container = st.status("Processing Audio...", expanded=True)
            
            try:
                # Initialize Pipeline
                status_container.write("🏗️ Initializing AI Pipeline...")
                pipeline = MeetingPipeline()
                status_container.write(f"✅ Model Selected: {pipeline.model_name}")
                
                # Transcribe
                status_container.write("🎧 Transcribing audio (Whisper)...")
                # We need to call the internal methods to get intermediate updates if we want granular logs, 
                # but calling the main process_meeting is safer.
                
                # To show a "fake" progress bar for UX since Whisper blocks the thread
                progress_bar = status_container.progress(0)
                for percent in range(0, 40, 10):
                    time.sleep(0.1)
                    progress_bar.progress(percent)
                
                # Actual Processing
                result = pipeline.process_meeting(file_path)
                
                progress_bar.progress(80)
                status_container.write("🧠 Analyzing content with Gemini...")
                
                if "error" in result:
                    status_container.update(label="Error Occurred", state="error")
                    st.error(result["error"])
                else:
                    progress_bar.progress(100)
                    status_container.update(label="Processing Complete!", state="complete", expanded=False)
                    
                    # 3. Save Output & History
                    # We need the transcript text to save history. 
                    # The pipeline saves it to file, let's read it back or modify pipeline to return it.
                    # For now, let's read the file based on logic in pipeline.py
                    base_name = os.path.splitext(uploaded_file.name)[0]
                    transcript_path = os.path.join("output", f"{base_name}_transcript.txt")
                    
                    with open(transcript_path, "r") as t:
                        transcript_text = t.read()
                    
                    history_manager.save_to_history(uploaded_file.name, result, transcript_text)
                    
                    # --- RESULTS DISPLAY ---
                    st.success("Analysis Ready!")
                    
                    # Tab Layout
                    tab1, tab2, tab3, tab4 = st.tabs(["📋 Executive Summary", "✅ Action Items", "💡 Key Decisions", "📝 Full Transcript"])
                    
                    with tab1:
                        st.markdown(f"### Executive Summary")
                        st.write(result["executive_summary"])
                        
                    with tab2:
                        st.markdown("### Action Items")
                        # Use a clean dataframe for action items
                        if result["action_items"]:
                            st.dataframe(result["action_items"], use_container_width=True)
                        else:
                            st.info("No action items detected.")
                            
                    with tab3:
                        st.markdown("### Key Decisions")
                        for decision in result["key_decisions"]:
                            st.markdown(f"- {decision}")
                            
                    with tab4:
                        st.markdown("### Transcript")
                        st.download_button(
                            label="📥 Download Transcript (.txt)",
                            data=transcript_text,
                            file_name=f"{base_name}_transcript.txt",
                            mime="text/plain"
                        )
                        st.text_area("Raw Text", transcript_text, height=300)
                        
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")