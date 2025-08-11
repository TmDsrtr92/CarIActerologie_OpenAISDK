"""
User Dashboard Page
Progress tracking and session metrics
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Tableau de Bord - CarIActérologie",
    page_icon="📈",
    layout="wide"
)

def create_progress_metrics():
    """Create progress metrics display"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Sessions Totales",
            value="28",
            delta="4 cette semaine",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="Score de Découverte de Soi",
            value="78%",
            delta="+12%",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="Insights Obtenus",
            value="45",
            delta="+8",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Confiance de Caractère",
            value="85%",
            delta="+3%",
            delta_color="normal"
        )

def create_session_timeline():
    """Create interactive session timeline"""
    
    # Generate mock session data
    dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')
    sessions_per_day = np.random.poisson(0.3, len(dates))  # Average 0.3 sessions per day
    
    # Create some sessions
    session_data = []
    session_id = 1
    
    for date, num_sessions in zip(dates, sessions_per_day):
        for _ in range(num_sessions):
            session_data.append({
                'date': date,
                'session_id': session_id,
                'duration': np.random.normal(25, 8),  # Average 25 minutes
                'insights': np.random.randint(1, 8),
                'mood_before': np.random.randint(1, 10),
                'mood_after': np.random.randint(5, 10),
                'character_confidence': min(50 + session_id * 0.5 + np.random.normal(0, 3), 100)
            })
            session_id += 1
    
    df = pd.DataFrame(session_data[-50:])  # Last 50 sessions
    
    # Create timeline chart
    fig = px.scatter(
        df, 
        x='date', 
        y='character_confidence',
        size='duration',
        color='insights',
        hover_data=['mood_before', 'mood_after', 'duration'],
        title="Chronologie des Sessions et Développement du Caractère",
        labels={
            'character_confidence': 'Confiance de Caractère %',
            'date': 'Date',
            'insights': 'Insights Obtenus'
        }
    )
    
    fig.update_traces(opacity=0.7)
    fig.update_layout(height=400)
    
    return fig

def create_insights_gallery():
    """Create insights gallery with categorization"""
    
    insights = [
        {
            'category': 'Personality Trait',
            'insight': 'You show strong intuitive thinking patterns, preferring to see the big picture',
            'confidence': 92,
            'date': '2024-01-08',
            'icon': '🧠'
        },
        {
            'category': 'Emotional Pattern',
            'insight': 'High emotional responsiveness to interpersonal situations',
            'confidence': 88,
            'date': '2024-01-07',
            'icon': '❤️'
        },
        {
            'category': 'Behavioral Tendency',
            'insight': 'Preference for reflection before action (secondary resonance)',
            'confidence': 85,
            'date': '2024-01-06',
            'icon': '⚡'
        },
        {
            'category': 'Social Style',
            'insight': 'Balanced extraversion with selective social engagement',
            'confidence': 78,
            'date': '2024-01-05',
            'icon': '👥'
        },
        {
            'category': 'Decision Making',
            'insight': 'Values-driven decisions with careful consideration',
            'confidence': 82,
            'date': '2024-01-04',
            'icon': '🎯'
        },
        {
            'category': 'Stress Response',
            'insight': 'Tends toward withdrawal and reflection under pressure',
            'confidence': 76,
            'date': '2024-01-03',
            'icon': '🌊'
        }
    ]
    
    st.markdown("### 💡 Recent Insights")
    
    for insight in insights:
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 6, 2, 2])
            
            with col1:
                st.markdown(f"<div style='font-size: 2rem; text-align: center;'>{insight['icon']}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**{insight['category']}**")
                st.markdown(f"*{insight['insight']}*")
            
            with col3:
                confidence_color = "#4CAF50" if insight['confidence'] >= 80 else "#FF9800" if insight['confidence'] >= 70 else "#F44336"
                st.markdown(f"<span style='color: {confidence_color}; font-weight: bold;'>{insight['confidence']}%</span>", unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"<small>{insight['date']}</small>", unsafe_allow_html=True)
            
            st.markdown("---")

def create_mood_tracking():
    """Create mood tracking visualization"""
    
    # Generate mock mood data
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    morning_mood = np.random.normal(6, 1.5, len(dates)).clip(1, 10)
    evening_mood = morning_mood + np.random.normal(1, 0.8, len(dates))
    evening_mood = evening_mood.clip(1, 10)
    
    df = pd.DataFrame({
        'date': dates,
        'morning_mood': morning_mood,
        'evening_mood': evening_mood
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['morning_mood'],
        mode='lines+markers',
        name='Morning Mood',
        line=dict(color='#667eea')
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['evening_mood'],
        mode='lines+markers',
        name='Evening Mood',
        line=dict(color='#764ba2')
    ))
    
    fig.update_layout(
        title="Suivi de l'Humeur (30 Jours)",
        yaxis_title="Score d'Humeur (1-10)",
        xaxis_title="Date",
        height=300
    )
    
    return fig

def main():
    """Main dashboard"""
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px; margin-bottom: 2rem; color: white; text-align: center;">
        <h1>📈 Tableau de Bord de Découverte Personnelle</h1>
        <p>Suivez votre parcours de compréhension de soi</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress metrics
    create_progress_metrics()
    
    st.markdown("---")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Session timeline
        timeline_fig = create_session_timeline()
        st.plotly_chart(timeline_fig, use_container_width=True)
        
        # Mood tracking
        mood_fig = create_mood_tracking()
        st.plotly_chart(mood_fig, use_container_width=True)
    
    with col2:
        # Weekly summary
        st.markdown("### 📊 Résumé de Cette Semaine")
        
        weekly_data = {
            'Day': ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
            'Sessions': [1, 0, 2, 1, 1, 0, 1],
            'Duration (min)': [25, 0, 45, 30, 20, 0, 35]
        }
        
        df_week = pd.DataFrame(weekly_data)
        
        fig_week = px.bar(
            df_week, 
            x='Day', 
            y='Sessions',
            title="Sessions de Cette Semaine"
        )
        fig_week.update_traces(marker_color='#667eea')
        st.plotly_chart(fig_week, use_container_width=True)
        
        # Achievement badges
        st.markdown("### 🏆 Réalisations Récentes")
        
        achievements = [
            {"name": "Penseur Profond", "desc": "5 sessions cette semaine", "icon": "🧠"},
            {"name": "Conscient de Soi", "desc": "85% de confiance de caractère", "icon": "🎯"},
            {"name": "Constant", "desc": "Série de 7 jours", "icon": "🔥"},
            {"name": "Perspicace", "desc": "45+ insights obtenus", "icon": "💡"}
        ]
        
        for achievement in achievements:
            st.markdown(f"""
            <div style="background: #f8f9fc; border-left: 4px solid #667eea; padding: 0.5rem; margin: 0.5rem 0; border-radius: 0 5px 5px 0;">
                {achievement['icon']} <strong>{achievement['name']}</strong><br>
                <small>{achievement['desc']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Insights gallery
    create_insights_gallery()
    
    # Sidebar with tools
    with st.sidebar:
        st.markdown("### 🛠️ Outils du Tableau de Bord")
        
        if st.button("📊 Mettre à Jour l'Analyse", use_container_width=True):
            st.success("Données du tableau de bord actualisées !")
        
        if st.button("📥 Exporter les Progrès", use_container_width=True):
            st.success("Données de progrès exportées !")
        
        if st.button("🎯 Définir des Objectifs", use_container_width=True):
            st.info("Fonctionnalité de définition d'objectifs bientôt disponible !")
        
        st.markdown("---")
        st.markdown("### 📅 Statistiques Rapides")
        st.markdown(f"**Aujourd'hui** : {datetime.now().strftime('%B %d, %Y')}")
        st.markdown("**Actif depuis** : 1er janvier 2024")
        st.markdown("**Temps total** : 12h 35m")
        st.markdown("**Session moyenne** : 23 minutes")
        
        st.markdown("---")
        st.markdown("### 🎨 Couleurs d'Humeur")
        st.color_picker("Couleur d'humeur actuelle", "#667eea")
        
        st.markdown("### 📝 Note Rapide")
        note = st.text_area("Ajoutez une réflexion rapide...", height=100)
        if st.button("Sauvegarder la Note"):
            st.success("Note sauvegardée dans votre journal !")

if __name__ == "__main__":
    main()