"""
CarIActerology - AI-Powered Psychological Self-Discovery Platform
Main Streamlit Application

Based on René Le Senne's characterology and modern AI techniques.
"""

import streamlit as st
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="Home - CarIActerology",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application entry point"""
    
    # Custom CSS for therapeutic aesthetic with help tooltips
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
            cursor: pointer;
            position: relative;
        }
        .navigation-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        /* Help Tooltip Styles */
        .help-tooltip {
            position: relative;
            display: inline-block;
            cursor: help;
            color: #667eea;
            margin-left: 5px;
        }
        .help-tooltip .tooltiptext {
            visibility: hidden;
            width: 280px;
            background-color: #333;
            color: #fff;
            text-align: left;
            border-radius: 6px;
            padding: 10px;
            position: absolute;
            z-index: 1000;
            bottom: 125%;
            left: 50%;
            margin-left: -140px;
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 0.9rem;
            line-height: 1.4;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .help-tooltip .tooltiptext::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #333 transparent transparent transparent;
        }
        .help-tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        .help-section {
            background: #f0f2f6;
            border-left: 4px solid #667eea;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
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
            <h3>💬 Chat 
                <span class="help-tooltip">❓
                    <span class="tooltiptext">
                        Engage in meaningful conversations with our AI psychologist. Share your thoughts, experiences, and questions to uncover insights about your personality based on Le Senne's characterology framework.
                    </span>
                </span>
            </h3>
            <p>Start a conversation with our AI psychologist to explore your personality and character traits.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Chat", key="chat_btn", use_container_width=True):
            st.switch_page("pages/1_Chat.py")
    
    with col2:
        st.markdown("""
        <div class="navigation-card">
            <h3>📊 Analysis 
                <span class="help-tooltip">❓
                    <span class="tooltiptext">
                        View detailed visualizations of your personality profile including character type assessment, trait breakdowns, and confidence scores based on your conversations and responses.
                    </span>
                </span>
            </h3>
            <p>View your psychological profile and character analysis based on Le Senne's characterology.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Analysis", key="analysis_btn", use_container_width=True):
            st.switch_page("pages/2_Analysis.py")
    
    with col3:
        st.markdown("""
        <div class="navigation-card">
            <h3>📈 Dashboard 
                <span class="help-tooltip">❓
                    <span class="tooltiptext">
                        Monitor your self-discovery journey with progress tracking, session statistics, timeline visualizations, and personal insights collected over time.
                    </span>
                </span>
            </h3>
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
            <h3>📄 Reports 
                <span class="help-tooltip">❓
                    <span class="tooltiptext">
                        Create comprehensive PDF reports including psychological analysis, character profiles, session summaries, and progress reports for personal use or sharing with professionals.
                    </span>
                </span>
            </h3>
            <p>Generate and download detailed psychological reports of your sessions.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Generate Reports", key="reports_btn", use_container_width=True):
            st.switch_page("pages/4_Reports.py")
    
    with col5:
        st.markdown("""
        <div class="navigation-card">
            <h3>⚙️ Settings 
                <span class="help-tooltip">❓
                    <span class="tooltiptext">
                        Customize your experience with user preferences, privacy controls, data management options, theme settings, and account information management.
                    </span>
                </span>
            </h3>
            <p>Manage your preferences, privacy settings, and account information.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Settings", key="settings_btn", use_container_width=True):
            st.switch_page("pages/5_Settings.py")
    
    # Help Section
    st.markdown("---")
    with st.expander("❓ How to Get Started - First-Time User Guide"):
        st.markdown("""
        <div class="help-section">
            <h4>🚀 Quick Start Guide</h4>
            <ol>
                <li><strong>Start with Chat:</strong> Begin your journey by clicking "Start Chat" and having a conversation about yourself</li>
                <li><strong>Share Openly:</strong> The more you share about your thoughts, feelings, and experiences, the better the analysis</li>
                <li><strong>Review Analysis:</strong> After chatting, visit the Analysis page to see your personality profile</li>
                <li><strong>Track Progress:</strong> Use the Dashboard to monitor your self-discovery journey over time</li>
                <li><strong>Generate Reports:</strong> Create detailed PDF reports of your psychological insights</li>
            </ol>
            
            <h4>💡 Understanding Characterology</h4>
            <p>René Le Senne's characterology identifies 8 personality types based on three key factors:</p>
            <ul>
                <li><strong>Emotionality:</strong> How strongly you react to situations</li>
                <li><strong>Activity:</strong> Your tendency to act and take initiative</li>
                <li><strong>Resonance:</strong> Whether you focus on present details or future possibilities</li>
            </ul>
            
            <h4>🔒 Privacy & Data</h4>
            <p>Your conversations are processed to provide insights but stored securely. Visit Settings to manage your privacy preferences and data retention options.</p>
        </div>
        """, unsafe_allow_html=True)
    
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