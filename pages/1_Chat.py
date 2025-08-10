"""
Chat Interface Page
Interactive conversation with AI psychologist
"""

import streamlit as st
import time
from datetime import datetime

st.set_page_config(
    page_title="Chat - CarIActerology",
    page_icon="💬",
    layout="wide"
)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "Hello! I'm your AI psychologist, specialized in René Le Senne's characterology. I'm here to help you discover yourself through meaningful conversation. What would you like to explore about your personality today?",
                "timestamp": datetime.now()
            }
        ]
    if "typing" not in st.session_state:
        st.session_state.typing = False

def display_message(message, is_user=False):
    """Display a chat message with appropriate styling"""
    with st.container():
        if is_user:
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin: 1rem 0;">
                <div style="background: #667eea; color: white; padding: 1rem; border-radius: 18px 18px 4px 18px; max-width: 70%; word-wrap: break-word;">
                    {message['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin: 1rem 0;">
                <div style="background: #f1f3f4; color: #333; padding: 1rem; border-radius: 18px 18px 18px 4px; max-width: 70%; word-wrap: break-word;">
                    {message['content']}
                    <br><small style="color: #888; font-size: 0.8rem;">{message.get('timestamp', datetime.now()).strftime('%H:%M')}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

def generate_mock_response(user_message):
    """Generate a mock psychological response"""
    mock_responses = [
        "That's a fascinating perspective. In characterology, we often see that such thoughts reflect deeper personality patterns. Can you tell me more about when you first noticed this about yourself?",
        
        "I notice some interesting character traits emerging from what you've shared. According to Le Senne's framework, this could indicate certain emotional and activity patterns. How do you typically react in challenging situations?",
        
        "Your response suggests some intriguing aspects of your character structure. In characterology, we analyze three main factors: Emotionality, Activity, and Resonance. Which of these resonates most with your self-perception?",
        
        "This is very insightful. I'm beginning to see patterns that might align with one of the eight character types in Le Senne's system. Do you find yourself more drawn to concrete details or abstract concepts?",
        
        "Thank you for sharing that. Your openness suggests a willingness to explore your inner world. In my analysis, I'm noticing potential indicators of specific character traits. How would you describe your energy levels throughout the day?"
    ]
    
    import random
    return random.choice(mock_responses)

def main():
    """Main chat interface"""
    initialize_session_state()
    
    # Custom CSS for chat interface
    st.markdown("""
    <style>
        /* Fix viewport to prevent any scrolling */
        .main .block-container {
            height: 100vh;
            max-height: 100vh;
            overflow: hidden;
            padding: 0.5rem;
            display: flex;
            flex-direction: column;
        }
        
        /* Ensure sidebar doesn't cause overflow */
        .css-1d391kg {
            padding-bottom: 1rem;
        }
        
        /* Reduce all gaps to minimum */
        div[data-testid="stVerticalBlock"] {
            gap: 0.25rem;
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        
        /* Minimize all margins */
        .element-container {
            margin: 0;
        }
        
        /* Remove extra padding */
        div[data-testid="stContainer"] {
            padding: 0;
            margin: 0;
        }
        
        /* Fix chat input positioning */
        div[data-testid="stChatInput"] {
            margin-top: 0.5rem;
            margin-bottom: 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header - ultra compact design
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 0.6rem; border-radius: 8px; margin-bottom: 0.3rem; color: white; text-align: center;">
        <h2 style="margin: 0; padding: 0; font-size: 1.3rem;">💬 Psychological Chat Session</h2>
        <p style="margin: 0.2rem 0 0 0; font-size: 0.85rem;">Explore your character through conversation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main chat area - use columns to better handle sidebar layout
    col1, col2 = st.columns([4, 0.1])  # Small right margin for better spacing
    
    with col1:
        # Chat messages container - calculated to fit viewport exactly
        # Viewport (100vh) - Header (65px) - Input (90px) - Padding (30px) = ~515px
        chat_container = st.container(height=515)
        with chat_container:
            # Display all messages
            for message in st.session_state.messages:
                is_user = message["role"] == "user"
                display_message(message, is_user)
            
            # Show typing indicator if needed
            if st.session_state.typing:
                st.markdown("""
                <div style="display: flex; justify-content: flex-start; margin: 1rem 0;">
                    <div style="background: #f1f3f4; color: #888; padding: 1rem; border-radius: 18px; font-style: italic;">
                        AI is thinking...
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Chat input - positioned directly below the messages
        user_input = st.chat_input("Share your thoughts, feelings, or ask about your personality...")
        
        if user_input:
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now()
            })
            
            # Show typing indicator
            st.session_state.typing = True
            st.rerun()
    
    # Process response (simulated delay)
    if st.session_state.typing:
        time.sleep(1)  # Simulate processing time
        
        # Generate and add AI response
        ai_response = generate_mock_response(st.session_state.messages[-1]["content"])
        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now()
        })
        
        st.session_state.typing = False
        st.rerun()
    
    # Sidebar with conversation tools
    with st.sidebar:
        st.markdown("### 💭 Conversation Tools")
        
        if st.button("🔄 New Session", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant", 
                    "content": "Hello! I'm your AI psychologist. What would you like to explore about your personality today?",
                    "timestamp": datetime.now()
                }
            ]
            st.rerun()
        
        if st.button("📥 Save Conversation", use_container_width=True):
            st.success("Conversation saved to your session history!")
        
        if st.button("📊 Analyze Session", use_container_width=True):
            st.info("Analysis will be available after more conversation data is collected.")
        
        st.markdown("---")
        st.markdown("### 📈 Session Stats")
        st.metric("Messages", len(st.session_state.messages))
        st.metric("Session Time", "15 mins")
        st.metric("Insights Detected", "3")

if __name__ == "__main__":
    main()