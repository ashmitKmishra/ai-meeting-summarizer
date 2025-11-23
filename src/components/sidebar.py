"""
Sidebar Component
Displays navigation and settings
Frontend Lead - Member 1
"""

import streamlit as st


def render_sidebar():
    """Render the application sidebar"""
    
    with st.sidebar:
        st.markdown("# Settings")
        
        st.markdown("---")
        
        # Summary Length
        st.markdown("### Summary Length")
        summary_length = st.radio(
            "Preferred length",
            ["Brief", "Standard", "Detailed"],
            index=1
        )
        
        # Additional Features
        st.markdown("### Features")
        speaker_identification = st.checkbox("Speaker Identification", value=True)
        sentiment_analysis = st.checkbox("Sentiment Analysis", value=True)
        action_items = st.checkbox("Extract Action Items", value=True)
        timestamps = st.checkbox("Include Timestamps", value=False)
        
        st.markdown("---")
        
        # History Section
        st.markdown("### Recent Meetings")
        with st.expander("View History"):
            st.markdown("*No meetings processed yet*")
        
        st.markdown("---")
        
        # About Section
        st.markdown("### About")
        st.markdown("""
        **AI Meeting Summarizer**
        Version 1.0.0
        
        Transform your meetings into actionable insights using AI-powered transcription and summarization.
        
        [Documentation](https://github.com/ashmitKmishra/ai-meeting-summarizer) | [Report Bug](https://github.com/ashmitKmishra/ai-meeting-summarizer) | [Suggest Feature](https://github.com/ashmitKmishra/ai-meeting-summarizer)
        """)
        
        # Credits
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.8rem;'>
            Built by Team 5PPL<br>
            Powered by Whisper & Gemini
        </div>
        """, unsafe_allow_html=True)
