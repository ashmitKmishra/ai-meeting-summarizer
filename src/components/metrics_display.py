"""
Metrics Display Component
Shows statistics and analytics
Frontend Lead - Member 1
"""

import streamlit as st


def render_metrics():
    """Render quick statistics and metrics"""
    
    # Session statistics (dummy data for now)
    total_meetings = st.session_state.get('total_meetings', 0)
    total_hours = st.session_state.get('total_hours', 0)
    action_items = st.session_state.get('action_items_count', 0)
    
    # Display metrics
    st.metric(
        label="Meetings Processed",
        value=total_meetings,
        delta="This session"
    )
    
    st.metric(
        label="Hours Analyzed",
        value=f"{total_hours:.1f}h",
        delta="Total"
    )
    
    # Progress indicators
    if st.session_state.get('processing', False):
        st.markdown("### Processing Status")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        import time
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
            if i < 30:
                status_text.text("Transcribing audio...")
            elif i < 70:
                status_text.text("Analyzing content...")
            else:
                status_text.text("Generating summary...")


def update_session_metrics(summary_data):
    """
    Update session metrics based on processed data
    
    Args:
        summary_data: Dictionary containing summary information
    """
    if 'total_meetings' not in st.session_state:
        st.session_state.total_meetings = 0
    
    st.session_state.total_meetings += 1
    
    # Extract duration and convert to hours
    duration_str = summary_data.get('duration', '0 minutes')
    try:
        minutes = int(duration_str.split()[0])
        hours = minutes / 60
        
        if 'total_hours' not in st.session_state:
            st.session_state.total_hours = 0
        st.session_state.total_hours += hours
    except:
        pass
    
    # Count action items
    action_items = summary_data.get('action_items', [])
    if 'action_items_count' not in st.session_state:
        st.session_state.action_items_count = 0
    st.session_state.action_items_count += len(action_items)
