"""
AI Meeting Summarizer - Frontend Dashboard
Member 1: Frontend Lead
File Ownership: src/app_ui.py, src/components/
"""

import streamlit as st
import sys
from pathlib import Path

# Add components to path
sys.path.append(str(Path(__file__).parent))

from components.file_uploader import render_file_uploader
from components.summary_display import render_summary_display
from components.sidebar import render_sidebar
from components.metrics_display import render_metrics


def main():
    """Main application entry point"""
    
    # Page configuration
    st.set_page_config(
        page_title="AI Meeting Summarizer",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS with Font Awesome
    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
        .main {
            padding-top: 0rem;
        }
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: #1E88E5;
            text-align: center;
            padding: 0;
            margin-top: 0.5rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #666;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .upload-section {
            background-color: #f0f2f6;
            padding: 2rem;
            border-radius: 10px;
            margin: 2rem 0;
        }
        .summary-box {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #1E88E5;
            margin: 1rem 0;
        }
        .action-item {
            background-color: #fff3cd;
            padding: 1rem;
            border-radius: 5px;
            margin: 0.5rem 0;
            border-left: 3px solid #ffc107;
        }
        .stButton>button {
            background-color: #1E88E5;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            padding: 0.5rem 2rem;
        }
        h2 a, h3 a, h4 a {
            display: none !important;
        }
        [data-testid="stAppDeployButton"] {
            display: none;
        }
        button[kind="header"] {
            display: none;
        }
        [data-testid="stHeader"] button[aria-label="more_vert"] {
            display: none !important;
        }
        header[data-testid="stHeader"] > div:nth-child(2) > div > button {
            display: none !important;
        }
        </style>
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            const hideMenu = setInterval(function() {
                const menuButton = document.querySelector('[data-testid="stHeader"] button');
                if (menuButton) {
                    menuButton.style.display = 'none';
                }
                const toolbar = document.querySelector('[data-testid="stToolbar"]');
                if (toolbar) {
                    toolbar.style.display = 'none';
                }
            }, 100);
        });
        </script>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header"><i class="fas fa-microphone"></i> AI Meeting Summarizer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Transform your meeting recordings into actionable insights</div>',
        unsafe_allow_html=True
    )
    
    # Initialize session state
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'summary_data' not in st.session_state:
        st.session_state.summary_data = None
    
    # Sidebar
    render_sidebar()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h2>Upload Meeting Recording</h2>", unsafe_allow_html=True)
        
        # File upload component
        uploaded_file = render_file_uploader()
        
        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            
            # Display file info
            st.success(f"File uploaded: {uploaded_file.name}")
            st.info(f"File size: {uploaded_file.size / 1024:.2f} KB")
            
            # Process button
            if st.button("Process Meeting", key="process_btn"):
                st.session_state.processing = True
                
                with st.spinner("Processing your meeting recording..."):
                    # TODO: Connect to backend pipeline
                    # For now, show dummy data
                    import time
                    time.sleep(2)
                    
                    # Dummy summary data
                    st.session_state.summary_data = {
                        'title': 'Team Standup Meeting',
                        'date': '2025-11-23',
                        'duration': '45 minutes',
                        'participants': ['Alice', 'Bob', 'Charlie', 'David'],
                        'summary': """
                        The team discussed the progress on the current sprint. 
                        Key points included backend API development, frontend UI improvements, 
                        and upcoming deadlines. Several action items were identified for 
                        immediate attention.
                        """,
                        'action_items': [
                            {'task': 'Complete API documentation', 'owner': 'Alice', 'deadline': '2025-11-25'},
                            {'task': 'Review UI mockups', 'owner': 'Bob', 'deadline': '2025-11-24'},
                            {'task': 'Fix bug in authentication', 'owner': 'Charlie', 'deadline': '2025-11-26'},
                            {'task': 'Prepare deployment scripts', 'owner': 'David', 'deadline': '2025-11-27'}
                        ],
                        'key_topics': ['Sprint Progress', 'API Development', 'UI/UX', 'Deployment'],
                        'sentiment': 'Positive',
                        'next_meeting': '2025-11-30'
                    }
                
                st.session_state.processing = False
                st.rerun()
    
    with col2:
        st.markdown("<h2>Quick Stats</h2>", unsafe_allow_html=True)
        render_metrics()
        
        st.markdown("<h3>How it works</h3>", unsafe_allow_html=True)
        st.markdown("""
        1. **Upload** your meeting recording (audio/video)
        2. **Process** with AI to extract insights
        3. **Review** the automated summary
        4. **Export** action items and notes
        """)
        
        st.markdown("<h3>Features</h3>", unsafe_allow_html=True)
        st.markdown("""
        - <i class='fas fa-microphone-alt'></i> Automatic transcription
        - <i class='fas fa-file-alt'></i> Smart summarization
        - <i class='fas fa-tasks'></i> Action item extraction
        """, unsafe_allow_html=True)
    
    # Display summary if available
    if st.session_state.summary_data:
        st.markdown("---")
        render_summary_display(st.session_state.summary_data)


if __name__ == "__main__":
    main()
