"""
CarIActerology - AI-Powered Psychological Self-Discovery Platform
Main Streamlit Application

Based on René Le Senne's characterology and modern AI techniques.
"""

import streamlit as st
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="CarIActerology - Know Thyself",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application entry point"""
    
    # Custom CSS for therapeutic aesthetic
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
        .welcome-text {
            font-size: 1.2rem;
            color: #555;
            text-align: center;
            margin-bottom: 2rem;
        }
        .navigation-card {
            background: #f8f9fc;
            border: 1px solid #e1e5e9;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            text-align: center;
            transition: all 0.3s ease;
        }
        .navigation-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🧠 CarIActerology</h1>
        <p><em>"Know Thyself" - Socrates</em></p>
        <p>AI-Powered Psychological Self-Discovery Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="welcome-text">
        Welcome to CarIActerology, an advanced psychological self-discovery platform powered by artificial intelligence.
        <br>
        Based on René Le Senne's characterology, we help you understand your personality through meaningful conversations.
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="navigation-card">
            <h3>💬 Chat</h3>
            <p>Start a conversation with our AI psychologist to explore your personality and character traits.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Chat", key="chat_btn", use_container_width=True):
            st.switch_page("pages/1_Chat.py")
    
    with col2:
        st.markdown("""
        <div class="navigation-card">
            <h3>📊 Analysis</h3>
            <p>View your psychological profile and character analysis based on Le Senne's characterology.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Analysis", key="analysis_btn", use_container_width=True):
            st.switch_page("pages/2_Analysis.py")
    
    with col3:
        st.markdown("""
        <div class="navigation-card">
            <h3>📈 Dashboard</h3>
            <p>Track your self-discovery progress and view insights from your sessions.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Dashboard", key="dashboard_btn", use_container_width=True):
            st.switch_page("pages/3_Dashboard.py")
    
    # Second row
    col4, col5 = st.columns(2)
    
    with col4:
        st.markdown("""
        <div class="navigation-card">
            <h3>📄 Reports</h3>
            <p>Generate and download detailed psychological reports of your sessions.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Generate Reports", key="reports_btn", use_container_width=True):
            st.switch_page("pages/4_Reports.py")
    
    with col5:
        st.markdown("""
        <div class="navigation-card">
            <h3>⚙️ Settings</h3>
            <p>Manage your preferences, privacy settings, and account information.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Settings", key="settings_btn", use_container_width=True):
            st.switch_page("pages/5_Settings.py")
    
    # Footer information
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; margin-top: 2rem;">
        <p>Based on René Le Senne's <em>Treatise on Characterology</em> (1945)</p>
        <p>Powered by OpenAI Agents SDK, Mem0 Memory System, and FAISS Vector Database</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()