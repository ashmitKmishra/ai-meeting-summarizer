"""
File Uploader Component
Handles audio/video file uploads for meeting recordings
Frontend Lead - Member 1
"""

import streamlit as st
from pathlib import Path


def render_file_uploader():
    """
    Render file upload component for meeting recordings
    
    Returns:
        uploaded_file: Streamlit UploadedFile object or None
    """
    
    st.markdown("""
    <div class="upload-section">
        <h3>Supported Formats</h3>
        <p>Audio: MP3, WAV, M4A, OGG | Video: MP4, AVI, MOV, MKV</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a meeting recording file",
        type=['mp3', 'wav', 'm4a', 'ogg', 'mp4', 'avi', 'mov', 'mkv'],
        help="Upload your meeting recording in audio or video format",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        # Display file preview
        file_extension = Path(uploaded_file.name).suffix.lower()
        
        if file_extension in ['.mp3', '.wav', '.m4a', '.ogg']:
            st.audio(uploaded_file, format=f'audio/{file_extension[1:]}')
        elif file_extension in ['.mp4', '.avi', '.mov', '.mkv']:
            st.video(uploaded_file, format=f'video/{file_extension[1:]}')
        
        # File details
        with st.expander("File Details"):
            st.write(f"**Filename:** {uploaded_file.name}")
            st.write(f"**Size:** {uploaded_file.size / (1024*1024):.2f} MB")
            st.write(f"**Type:** {uploaded_file.type}")
    
    return uploaded_file


def save_uploaded_file(uploaded_file, save_path="uploads"):
    """
    Save uploaded file to disk
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        save_path: Directory to save the file
    
    Returns:
        file_path: Path to saved file
    """
    save_dir = Path(save_path)
    save_dir.mkdir(exist_ok=True)
    
    file_path = save_dir / uploaded_file.name
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    return str(file_path)
