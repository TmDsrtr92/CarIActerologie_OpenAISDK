"""
CarIActerology - AI-Powered Psychological Self-Discovery Platform
Main Streamlit Application

Based on René Le Senne's characterology and modern AI techniques.
"""

import streamlit as st
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="Accueil - CarIActérologie",
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
        <h1>🧠 CarIActérologie</h1>
        <p><em>"Connais-toi toi-même" - Socrate</em></p>
        <p>Plateforme de Découverte de Soi Psychologique propulsée par l'IA</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="welcome-text">
        Bienvenue sur CarIActérologie, une plateforme avancée de découverte de soi psychologique alimentée par l'intelligence artificielle.
        <br>
        Basée sur la caractérologie de René Le Senne, nous vous aidons à comprendre votre personnalité grâce à des conversations significatives.
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="navigation-card">
            <h3>💬 Discussion 
                <span class="help-tooltip">❓
                    <span class="tooltiptext">
                        Engagez des conversations significatives avec notre psychologue IA. Partagez vos pensées, expériences et questions pour découvrir des insights sur votre personnalité basés sur le cadre caractérologique de Le Senne.
                    </span>
                </span>
            </h3>
            <p>Commencez une conversation avec notre psychologue IA pour explorer votre personnalité et vos traits de caractère.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Commencer la Discussion", key="chat_btn", use_container_width=True):
            st.switch_page("pages/1_Chat.py")
    
    with col2:
        st.markdown("""
        <div class="navigation-card">
            <h3>📊 Analyse 
                <span class="help-tooltip">❓
                    <span class="tooltiptext">
                        Visualisez des représentations détaillées de votre profil de personnalité incluant l'évaluation du type de caractère, les analyses des traits, et les scores de confiance basés sur vos conversations et réponses.
                    </span>
                </span>
            </h3>
            <p>Visualisez votre profil psychologique et l'analyse de caractère basée sur la caractérologie de Le Senne.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Voir l'Analyse", key="analysis_btn", use_container_width=True):
            st.switch_page("pages/2_Analysis.py")
    
    with col3:
        st.markdown("""
        <div class="navigation-card">
            <h3>📈 Tableau de Bord 
                <span class="help-tooltip">❓
                    <span class="tooltiptext">
                        Surveillez votre parcours de découverte de soi avec le suivi des progrès, les statistiques de sessions, les visualisations de chronologie, et les insights personnels collectés au fil du temps.
                    </span>
                </span>
            </h3>
            <p>Suivez vos progrès de découverte de soi et visualisez les insights de vos sessions.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ouvrir le Tableau de Bord", key="dashboard_btn", use_container_width=True):
            st.switch_page("pages/3_Dashboard.py")
    
    # Second row
    col4, col5 = st.columns(2)
    
    with col4:
        st.markdown("""
        <div class="navigation-card">
            <h3>📄 Rapports 
                <span class="help-tooltip">❓
                    <span class="tooltiptext">
                        Créez des rapports PDF complets incluant l'analyse psychologique, les profils de caractère, les résumés de sessions, et les rapports de progrès pour un usage personnel ou à partager avec des professionnels.
                    </span>
                </span>
            </h3>
            <p>Générez et téléchargez des rapports psychologiques détaillés de vos sessions.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Générer des Rapports", key="reports_btn", use_container_width=True):
            st.switch_page("pages/4_Reports.py")
    
    with col5:
        st.markdown("""
        <div class="navigation-card">
            <h3>⚙️ Paramètres 
                <span class="help-tooltip">❓
                    <span class="tooltiptext">
                        Personnalisez votre expérience avec les préférences utilisateur, les contrôles de confidentialité, les options de gestion des données, les paramètres de thème, et la gestion des informations de compte.
                    </span>
                </span>
            </h3>
            <p>Gérez vos préférences, paramètres de confidentialité, et informations de compte.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ouvrir les Paramètres", key="settings_btn", use_container_width=True):
            st.switch_page("pages/5_Settings.py")
    
    # Help Section
    st.markdown("---")
    with st.expander("❓ Comment Commencer - Guide du Premier Utilisateur"):
        st.markdown("""
        <div class="help-section">
            <h4>🚀 Guide de Démarrage Rapide</h4>
            <ol>
                <li><strong>Commencez par la Discussion :</strong> Débutez votre parcours en cliquant sur "Commencer la Discussion" et ayez une conversation sur vous-même</li>
                <li><strong>Partagez Ouvertement :</strong> Plus vous partagez vos pensées, sentiments et expériences, meilleure sera l'analyse</li>
                <li><strong>Consultez l'Analyse :</strong> Après avoir discuté, visitez la page Analyse pour voir votre profil de personnalité</li>
                <li><strong>Suivez vos Progrès :</strong> Utilisez le Tableau de Bord pour surveiller votre parcours de découverte de soi au fil du temps</li>
                <li><strong>Générez des Rapports :</strong> Créez des rapports PDF détaillés de vos insights psychologiques</li>
            </ol>
            
            <h4>💡 Comprendre la Caractérologie</h4>
            <p>La caractérologie de René Le Senne identifie 8 types de personnalité basés sur trois facteurs clés :</p>
            <ul>
                <li><strong>Émotivité :</strong> L'intensité de vos réactions aux situations</li>
                <li><strong>Activité :</strong> Votre tendance à agir et prendre des initiatives</li>
                <li><strong>Résonance :</strong> Si vous vous concentrez sur les détails présents ou les possibilités futures</li>
            </ul>
            
            <h4>🔒 Confidentialité et Données</h4>
            <p>Vos conversations sont traitées pour fournir des insights mais stockées de manière sécurisée. Visitez les Paramètres pour gérer vos préférences de confidentialité et options de rétention des données.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer information
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; margin-top: 2rem;">
        <p>Basé sur le <em>Traité de Caractérologie</em> de René Le Senne (1945)</p>
        <p>Propulsé par OpenAI Agents SDK, Système de Mémoire Mem0, et Base de Données Vectorielle FAISS</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()