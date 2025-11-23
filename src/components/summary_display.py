"""
Summary Display Component
Displays meeting summary and extracted information
Frontend Lead - Member 1
"""

import streamlit as st
import json
from datetime import datetime


def render_summary_display(summary_data):
    """
    Render the meeting summary and analysis
    
    Args:
        summary_data: Dictionary containing summary information
    """
    
    st.markdown("## Meeting Summary")
    
    # Header information
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Date", summary_data.get('date', 'N/A'))
    with col2:
        st.metric("Duration", summary_data.get('duration', 'N/A'))
    with col3:
        sentiment = summary_data.get('sentiment', 'Neutral')
        st.metric("Sentiment", sentiment)
    
    # Meeting Title
    st.markdown(f"### {summary_data.get('title', 'Meeting Summary')}")
    
    # Participants
    if 'participants' in summary_data:
        st.markdown("#### Participants")
        participants_str = ", ".join(summary_data['participants'])
        st.info(participants_str)
    
    # Main Summary
    st.markdown("#### Summary")
    st.markdown(f"""
    <div class="summary-box">
        {summary_data.get('summary', 'No summary available')}
    </div>
    """, unsafe_allow_html=True)
    
    # Key Topics
    if 'key_topics' in summary_data and summary_data['key_topics']:
        st.markdown("#### Key Topics")
        topics_cols = st.columns(len(summary_data['key_topics']))
        for idx, topic in enumerate(summary_data['key_topics']):
            with topics_cols[idx]:
                st.button(f"{topic}", key=f"topic_{idx}", disabled=True)
    
    # Action Items
    if 'action_items' in summary_data and summary_data['action_items']:
        st.markdown("#### Action Items")
        for idx, action in enumerate(summary_data['action_items']):
            render_action_item(action, idx)
    
    # Export Options
    st.markdown("---")
    st.markdown("### Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Download as JSON"):
            json_str = json.dumps(summary_data, indent=2)
            st.download_button(
                label="Save JSON",
                data=json_str,
                file_name=f"meeting_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("Download as Text"):
            text_summary = generate_text_summary(summary_data)
            st.download_button(
                label="Save TXT",
                data=text_summary,
                file_name=f"meeting_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    with col3:
        if st.button("Email Summary"):
            st.info("Email functionality coming soon!")


def render_action_item(action, index):
    """
    Render a single action item
    
    Args:
        action: Dictionary with action item details
        index: Item index for unique keys
    """
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="action-item">
                <strong>{action.get('task', 'No task description')}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.write(f"**{action.get('owner', 'Unassigned')}**")
        
        with col3:
            st.write(f"**{action.get('deadline', 'No deadline')}**")


def generate_text_summary(summary_data):
    """
    Generate plain text version of summary
    
    Args:
        summary_data: Dictionary containing summary information
    
    Returns:
        text_summary: Formatted text summary
    """
    lines = []
    lines.append(f"MEETING SUMMARY: {summary_data.get('title', 'Untitled Meeting')}")
    lines.append("=" * 60)
    lines.append(f"\nDate: {summary_data.get('date', 'N/A')}")
    lines.append(f"Duration: {summary_data.get('duration', 'N/A')}")
    lines.append(f"Sentiment: {summary_data.get('sentiment', 'N/A')}")
    
    if 'participants' in summary_data:
        lines.append(f"\nParticipants: {', '.join(summary_data['participants'])}")
    
    lines.append("\n" + "-" * 60)
    lines.append("SUMMARY")
    lines.append("-" * 60)
    lines.append(summary_data.get('summary', 'No summary available'))
    
    if 'key_topics' in summary_data and summary_data['key_topics']:
        lines.append("\n" + "-" * 60)
        lines.append("KEY TOPICS")
        lines.append("-" * 60)
        for topic in summary_data['key_topics']:
            lines.append(f"- {topic}")
    
    if 'action_items' in summary_data and summary_data['action_items']:
        lines.append("\n" + "-" * 60)
        lines.append("ACTION ITEMS")
        lines.append("-" * 60)
        for idx, action in enumerate(summary_data['action_items'], 1):
            lines.append(f"\n{idx}. {action.get('task', 'No description')}")
            lines.append(f"   Owner: {action.get('owner', 'Unassigned')}")
            lines.append(f"   Deadline: {action.get('deadline', 'No deadline')}")
    
    return "\n".join(lines)
