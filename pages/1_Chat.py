"""
Chat Interface Page
Interactive conversation with AI psychologist
"""

import streamlit as st
import time
from datetime import datetime

st.set_page_config(
    page_title="Discussion - CarIActérologie",
    page_icon="💬",
    layout="wide"
)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "Bonjour ! Je suis votre psychologue IA, spécialisé dans la caractérologie de René Le Senne. Je suis ici pour vous aider à vous découvrir à travers des conversations significatives. Qu'aimeriez-vous explorer concernant votre personnalité aujourd'hui ?",
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
        "C'est une perspective fascinante. En caractérologie, nous voyons souvent que de telles pensées reflètent des patterns de personnalité plus profonds. Pouvez-vous me parler davantage du moment où vous avez remarqué cela pour la première fois chez vous ?",
        
        "Je remarque des traits de caractère intéressants qui émergent de ce que vous avez partagé. Selon le cadre de Le Senne, cela pourrait indiquer certains patterns émotionnels et d'activité. Comment réagissez-vous généralement dans des situations difficiles ?",
        
        "Votre réponse suggère des aspects intrigants de votre structure de caractère. En caractérologie, nous analysons trois facteurs principaux : l'Émotivité, l'Activité et la Résonance. Lequel de ces facteurs résonne le plus avec votre auto-perception ?",
        
        "C'est très perspicace. Je commence à voir des patterns qui pourraient s'aligner avec l'un des huit types de caractère du système de Le Senne. Vous sentez-vous plus attiré par les détails concrets ou les concepts abstraits ?",
        
        "Merci de partager cela. Votre ouverture suggère une volonté d'explorer votre monde intérieur. Dans mon analyse, je remarque des indicateurs potentiels de traits de caractère spécifiques. Comment décririez-vous vos niveaux d'énergie tout au long de la journée ?"
    ]
    
    import random
    return random.choice(mock_responses)

def main():
    """Main chat interface"""
    initialize_session_state()
    
    # Custom CSS for chat interface with help tooltips
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
        
        /* Help Tooltip Styles */
        .help-tooltip {
            position: relative;
            display: inline-block;
            cursor: help;
            color: #ffffff;
            margin-left: 5px;
            opacity: 0.8;
        }
        .help-tooltip:hover {
            opacity: 1;
        }
        .help-tooltip .tooltiptext {
            visibility: hidden;
            width: 260px;
            background-color: #333;
            color: #fff;
            text-align: left;
            border-radius: 6px;
            padding: 8px;
            position: absolute;
            z-index: 1000;
            bottom: 125%;
            left: 50%;
            margin-left: -130px;
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 0.85rem;
            line-height: 1.3;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
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
        .chat-help {
            background: rgba(255,255,255,0.1);
            padding: 0.5rem;
            border-radius: 4px;
            margin-bottom: 0.5rem;
            font-size: 0.85rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header - ultra compact design with help tooltip
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 0.6rem; border-radius: 8px; margin-bottom: 0.3rem; color: white; text-align: center;">
        <h2 style="margin: 0; padding: 0; font-size: 1.3rem;">💬 Session de Discussion Psychologique
            <span class="help-tooltip">❓
                <span class="tooltiptext">
                    Ceci est un espace sûr pour explorer votre personnalité. Partagez vos pensées, expériences, réactions et sentiments. L'IA posera des questions de suivi pour comprendre vos patterns de caractère.
                </span>
            </span>
        </h2>
        <p style="margin: 0.2rem 0 0 0; font-size: 0.85rem;">Explorez votre caractère à travers la conversation</p>
        <div class="chat-help">
            💡 Conseil : Soyez honnête et spécifique sur vos expériences pour de meilleurs insights
        </div>
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
                        L'IA réfléchit...
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Chat input - positioned directly below the messages
        user_input = st.chat_input("Partagez vos pensées, sentiments, ou posez des questions sur votre personnalité...")
        
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
        st.markdown("### 💭 Outils de Conversation")
        
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button("🔄 Nouvelle Session", use_container_width=True):
                st.session_state.messages = [
                    {
                        "role": "assistant", 
                        "content": "Bonjour ! Je suis votre psychologue IA. Qu'aimeriez-vous explorer concernant votre personnalité aujourd'hui ?",
                        "timestamp": datetime.now()
                    }
                ]
                st.rerun()
        with col2:
            st.markdown("❓", help="Commencer une nouvelle conversation - votre discussion précédente sera perdue")
        
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button("📥 Sauvegarder la Conversation", use_container_width=True):
                st.success("Conversation sauvegardée dans votre historique de session !")
        with col2:
            st.markdown("❓", help="Sauvegarder cette conversation pour la revoir plus tard dans votre tableau de bord")
        
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button("📊 Analyser la Session", use_container_width=True):
                st.info("L'analyse sera disponible après avoir collecté plus de données de conversation.")
        with col2:
            st.markdown("❓", help="Générer des insights psychologiques basés sur cette conversation")
        
        st.markdown("---")
        st.markdown("### 📈 Statistiques de Session")
        st.metric("Messages", len(st.session_state.messages), help="Total des messages échangés dans cette session")
        st.metric("Durée de Session", "15 mins", help="Durée de la conversation actuelle")
        st.metric("Insights Détectés", "3", help="Nombre d'insights de personnalité identifiés")
        
        # Add conversation tips
        st.markdown("---")
        with st.expander("💡 Conseils de Conversation"):
            st.markdown("""
            **Quoi partager :**
            - Expériences personnelles et réactions
            - Comment vous gérez le stress ou les défis
            - Vos préférences et style de prise de décision
            - Relations et interactions sociales
            - Approches de travail ou d'étude
            
            **Meilleures réponses :**
            - "Quand je suis stressé(e), j'ai tendance à..." ✅
            - "Je me sens stressé(e)" ❌
            - "Dans les conflits, j'ai tendance à..." ✅
            - "Je n'aime pas les conflits" ❌
            """)

if __name__ == "__main__":
    main()