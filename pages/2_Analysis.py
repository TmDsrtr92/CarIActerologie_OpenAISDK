"""
Analysis Dashboard Page
Character visualization and psychological analysis
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime, timedelta

# Add the project root to Python path for data imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.mock_data import (
    get_primary_character_type, get_mock_user_profile, 
    get_character_evolution_data, CHARACTER_TYPES
)

st.set_page_config(
    page_title="Analyse - CarIActérologie",
    page_icon="📊",
    layout="wide"
)

def create_character_radar_chart():
    """Create a radar chart for character traits using real mock data"""
    
    # Get current user's character type and profile
    character_type = get_primary_character_type()
    user_profile = get_mock_user_profile()
    
    # Convert Le Senne traits to 0-100 scale for visualization
    base_traits = character_type["traits"]
    traits = {
        'Émotivité': base_traits["emotionality"] * 10,
        'Activité': base_traits["activity"] * 10, 
        'Résonance': base_traits["resonance"] * 10,
        'Extraversion': (base_traits["activity"] + base_traits["emotionality"]) * 5,
        'Intuition': (10 - base_traits["resonance"]) * 10,
        'Rationalité': (10 - base_traits["emotionality"]) * 10,
        'Stabilité': base_traits["resonance"] * 10,
        'Ouverture': (base_traits["emotionality"] + (10 - base_traits["resonance"])) * 5
    }
    
    categories = list(traits.keys())
    values = list(traits.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Current Profile',
        line_color='#667eea'
    ))
    
    # Add ideal/target profile for comparison
    ideal_values = [85, 75, 70, 80, 65, 70, 75, 80]
    fig.add_trace(go.Scatterpolar(
        r=ideal_values,
        theta=categories,
        fill='toself',
        name='Ideal Profile',
        line_color='#764ba2',
        opacity=0.3
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Character Profile Analysis",
        title_x=0.5
    )
    
    return fig

def create_character_type_display():
    """Display the detected character type"""
    
    # Mock character type detection
    character_types = {
        "Nervous": {"score": 75, "description": "High emotionality, low activity, primary resonance"},
        "Sanguine": {"score": 85, "description": "High emotionality, high activity, primary resonance"},
        "Choleric": {"score": 65, "description": "High emotionality, high activity, secondary resonance"},
        "Melancholic": {"score": 45, "description": "High emotionality, low activity, secondary resonance"},
        "Phlegmatic": {"score": 30, "description": "Low emotionality, low activity, secondary resonance"},
        "Apathetic": {"score": 20, "description": "Low emotionality, low activity, primary resonance"},
        "Amorphous": {"score": 25, "description": "Low emotionality, high activity, primary resonance"},
        "Passionate": {"score": 55, "description": "Low emotionality, high activity, secondary resonance"}
    }
    
    # Sort by score
    sorted_types = sorted(character_types.items(), key=lambda x: x[1]["score"], reverse=True)
    
    st.markdown("### 🎭 Analyse du Type de Caractère")
    st.markdown("Basée sur le cadre caractérologique de René Le Senne")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        # Top character type
        top_type, top_data = sorted_types[0]
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 1rem;">
            <h2>Type Primaire : {top_type}</h2>
            <p style="font-size: 1.2rem; margin: 0;">{top_data['description']}</p>
            <div style="font-size: 2rem; margin-top: 1rem;">
                Confiance : {top_data['score']}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📈 Confiance")
        for char_type, data in sorted_types[:3]:
            st.metric(
                label=char_type, 
                value=f"{data['score']}%",
                delta=f"{data['score'] - 50}% vs référence"
            )
    
    with col3:
        # Character evolution chart
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        scores = np.random.normal(75, 5, 30).clip(0, 100)
        
        fig = px.line(
            x=dates, 
            y=scores,
            title="Évolution du Profil de Caractère",
            labels={'x': 'Date', 'y': 'Score de Confiance'}
        )
        fig.update_traces(line_color='#667eea')
        st.plotly_chart(fig, use_container_width=True)

def create_traits_breakdown():
    """Create detailed traits breakdown"""
    
    st.markdown("### 🔍 Analyse Détaillée des Traits")
    
    traits_data = {
        'Trait': ['Émotivité', 'Activité', 'Résonance', 'Extraversion', 'Intuition', 'Rationalité'],
        'Score': [75, 60, 80, 65, 70, 55],
        'Interpretation': [
            'Forte réactivité émotionnelle aux stimuli',
            'Tendance modérée vers l\'action et l\'initiative',
            'Résonance primaire forte - réactions immédiates',
            'Orientation sociale équilibrée',
            'Patterns de pensée intuitive forte',
            'Préférence modérée pour le raisonnement logique'
        ]
    }
    
    df = pd.DataFrame(traits_data)
    
    for _, row in df.iterrows():
        col1, col2, col3 = st.columns([2, 1, 3])
        
        with col1:
            st.markdown(f"**{row['Trait']}**")
        
        with col2:
            color = "#4CAF50" if row['Score'] >= 70 else "#FF9800" if row['Score'] >= 50 else "#F44336"
            st.markdown(f"<span style='color: {color}; font-weight: bold;'>{row['Score']}%</span>", unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"*{row['Interpretation']}*")
        
        # Progress bar
        progress = row['Score'] / 100
        st.progress(progress)
        st.markdown("")

def main():
    """Main analysis dashboard"""
    
    # Add help tooltip CSS
    st.markdown("""
    <style>
        .help-tooltip {
            position: relative;
            display: inline-block;
            cursor: help;
            color: #ffffff;
            margin-left: 5px;
            opacity: 0.9;
        }
        .help-tooltip:hover {
            opacity: 1;
        }
        .help-tooltip .tooltiptext {
            visibility: hidden;
            width: 300px;
            background-color: #333;
            color: #fff;
            text-align: left;
            border-radius: 6px;
            padding: 10px;
            position: absolute;
            z-index: 1000;
            bottom: 125%;
            left: 50%;
            margin-left: -150px;
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 0.9rem;
            line-height: 1.4;
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
        .analysis-help {
            background: #e8f4fd;
            border: 1px solid #2196F3;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Get user data
    character_type = get_primary_character_type()
    user_profile = get_mock_user_profile()
    
    # Header with help tooltip
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px; margin-bottom: 2rem; color: white; text-align: center;">
        <h1>📊 Tableau de Bord d'Analyse du Caractère 
            <span class="help-tooltip">❓
                <span class="tooltiptext">
                    Ce tableau de bord montre votre profil psychologique basé sur vos conversations. Les types de caractère sont déterminés par trois facteurs : Émotivité (intensité de vos réactions), Activité (votre niveau d'initiative), et Résonance (focus présent vs futur).
                </span>
            </span>
        </h1>
        <p>Basé sur le Cadre Caractérologique de René Le Senne</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User guidance for first-time users
    if "analysis_visited" not in st.session_state:
        st.session_state.analysis_visited = True
        with st.expander("🎯 Comprendre Votre Analyse - Cliquez pour En Savoir Plus", expanded=True):
            st.markdown("""
            <div class="analysis-help">
                <h4>📖 Comment Lire Votre Analyse</h4>
                <ul>
                    <li><strong>Type de Caractère :</strong> Votre classification de personnalité principale basée sur les 8 types de Le Senne</li>
                    <li><strong>Graphique Radar :</strong> Représentation visuelle de vos 8 dimensions clés de personnalité</li>
                    <li><strong>Score de Confiance :</strong> À quel point l'IA est certaine de votre profil (plus haut = plus de données)</li>
                    <li><strong>Forces et Zones de Croissance :</strong> Ce en quoi vous excellez vs les domaines à développer</li>
                    <li><strong>Chronologie d'Évolution :</strong> Comment votre profil a changé au fil du temps</li>
                </ul>
                
                <h4>💡 Conseils pour une Meilleure Analyse</h4>
                <ul>
                    <li>Ayez plus de conversations dans Discussion pour améliorer la précision</li>
                    <li>Partagez des expériences diverses (travail, relations, défis)</li>
                    <li>Soyez spécifique sur vos réactions et processus de prise de décision</li>
                    <li>Consultez cette page régulièrement pour suivre les changements</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Character Type Summary
    st.markdown(f"""
    <div style="background: {character_type['color']}20; border-left: 4px solid {character_type['color']}; padding: 1rem; border-radius: 5px; margin-bottom: 2rem;">
        <h2 style="color: {character_type['color']}; margin: 0;">🎭 Votre Type de Caractère : {character_type['name']}</h2>
        <p style="margin: 0.5rem 0;"><strong>Score de Confiance :</strong> {user_profile['confidence_score']*100:.1f}%</p>
        <p style="margin: 0;">{character_type['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Radar chart
        fig = create_character_radar_chart()
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Current analysis summary using real data
        st.markdown("### 📋 Résumé d'Analyse")
        
        st.metric("Sessions Analysées", f"{user_profile['analysis_sessions']}", "+3")
        st.metric("Confiance de Caractère", f"{user_profile['confidence_score']*100:.0f}%", "+5%")
        st.metric("Interactions Totales", f"{user_profile['total_interactions']}", "+12")
        
        st.markdown("### 💪 Forces Clés")
        for strength in character_type["strengths"][:3]:
            st.success(f"✓ {strength}")
        
        st.markdown("### ⚠️ Zones de Croissance") 
        for challenge in character_type["challenges"][:2]:
            st.warning(f"• {challenge}")
    
    # Character evolution timeline
    st.markdown("---")
    st.markdown("## 📈 Développement du Caractère au Fil du Temps")
    
    evolution_data = get_character_evolution_data(6)
    
    if evolution_data:
        dates = [entry['date'].strftime('%Y-%m') for entry in evolution_data]
        emotionality = [entry['traits']['emotionality'] * 10 for entry in evolution_data]
        activity = [entry['traits']['activity'] * 10 for entry in evolution_data]
        resonance = [entry['traits']['resonance'] * 10 for entry in evolution_data]
        
        evolution_fig = go.Figure()
        evolution_fig.add_trace(go.Scatter(x=dates, y=emotionality, name='Emotionality', line=dict(color='#FF6B6B', width=3)))
        evolution_fig.add_trace(go.Scatter(x=dates, y=activity, name='Activity', line=dict(color='#4ECDC4', width=3)))
        evolution_fig.add_trace(go.Scatter(x=dates, y=resonance, name='Resonance', line=dict(color='#45B7D1', width=3)))
        
        evolution_fig.update_layout(
            title="Évolution des Traits de Caractère - Cadre Le Senne",
            xaxis_title="Période de Temps", 
            yaxis_title="Force du Trait (0-100)",
            height=400,
            showlegend=True,
            hovermode='x unified'
        )
        
        st.plotly_chart(evolution_fig, use_container_width=True)
    
    # Character type display
    create_character_type_display()
    
    # Traits breakdown
    create_traits_breakdown()
    
    # Sidebar with analysis tools
    with st.sidebar:
        st.markdown("### 🛠️ Outils d'Analyse")
        
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button("🔄 Actualiser l'Analyse", use_container_width=True):
                st.success("Analyse actualisée avec les dernières données de session !")
        with col2:
            st.markdown("❓", help="Mettre à jour l'analyse avec les dernières conversations et réponses")
        
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button("📊 Rapport Détaillé", use_container_width=True):
                st.info("Naviguez vers la page Rapports pour générer une analyse détaillée.")
        with col2:
            st.markdown("❓", help="Generate comprehensive PDF report of your psychological analysis")
        
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button("💾 Export Data", use_container_width=True):
                st.success("Analysis data exported successfully!")
        with col2:
            st.markdown("❓", help="Download your analysis data in CSV format for personal use")
        
        st.markdown("---")
        st.markdown("### ⏰ Analysis History")
        st.markdown("- **Today**: Character profile updated")
        st.markdown("- **Yesterday**: 3 new traits identified")
        st.markdown("- **Last Week**: Major personality shift detected")
        
        st.markdown("---")
        with st.expander("📚 Le Senne's Framework Guide"):
            st.markdown("""
            **Three Primary Factors:**
            - **E**motionality (E/nE) - How strongly you react
            - **A**ctivity (A/nA) - Your tendency to act
            - **R**esonance (P/S) - Present vs future focus
            
            **8 Character Types:**
            - **Nervous** (EnAP) - Emotional, inactive, present-focused
            - **Sanguine** (EAP) - Emotional, active, present-focused  
            - **Choleric** (EAS) - Emotional, active, future-focused
            - **Melancholic** (EnAS) - Emotional, inactive, future-focused
            - **Phlegmatic** (nEnAS) - Calm, inactive, future-focused
            - **Apathetic** (nEnAP) - Calm, inactive, present-focused
            - **Amorphous** (nEAP) - Calm, active, present-focused
            - **Passionate** (nEAS) - Calm, active, future-focused
            """)
        
        with st.expander("💡 Interpretation Tips"):
            st.markdown("""
            **Understanding Your Scores:**
            - **70-100%**: Strong trait presence
            - **50-69%**: Moderate trait presence  
            - **30-49%**: Weak trait presence
            - **0-29%**: Trait largely absent
            
            **Radar Chart Reading:**
            - Larger area = more complex personality
            - Balanced shape = well-rounded character
            - Spikes = dominant traits
            - Valleys = areas for development
            """)

if __name__ == "__main__":
    main()