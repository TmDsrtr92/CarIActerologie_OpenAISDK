"""
Analysis Dashboard Page
Character visualization and psychological analysis
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Analysis - CarIActerology",
    page_icon="📊",
    layout="wide"
)

def create_character_radar_chart():
    """Create a radar chart for character traits"""
    
    # Mock character traits data based on Le Senne's 8 character types
    traits = {
        'Emotionality': 75,
        'Activity': 60,
        'Resonance': 80,
        'Extraversion': 65,
        'Intuition': 70,
        'Rationality': 55,
        'Stability': 68,
        'Openness': 82
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
    
    st.markdown("### 🎭 Character Type Analysis")
    st.markdown("Based on René Le Senne's characterology framework")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        # Top character type
        top_type, top_data = sorted_types[0]
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 1rem;">
            <h2>Primary Type: {top_type}</h2>
            <p style="font-size: 1.2rem; margin: 0;">{top_data['description']}</p>
            <div style="font-size: 2rem; margin-top: 1rem;">
                Confidence: {top_data['score']}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📈 Confidence")
        for char_type, data in sorted_types[:3]:
            st.metric(
                label=char_type, 
                value=f"{data['score']}%",
                delta=f"{data['score'] - 50}% vs baseline"
            )
    
    with col3:
        # Character evolution chart
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        scores = np.random.normal(75, 5, 30).clip(0, 100)
        
        fig = px.line(
            x=dates, 
            y=scores,
            title="Character Profile Evolution",
            labels={'x': 'Date', 'y': 'Confidence Score'}
        )
        fig.update_traces(line_color='#667eea')
        st.plotly_chart(fig, use_container_width=True)

def create_traits_breakdown():
    """Create detailed traits breakdown"""
    
    st.markdown("### 🔍 Detailed Trait Analysis")
    
    traits_data = {
        'Trait': ['Emotionality', 'Activity', 'Resonance', 'Extraversion', 'Intuition', 'Rationality'],
        'Score': [75, 60, 80, 65, 70, 55],
        'Interpretation': [
            'High emotional responsiveness to stimuli',
            'Moderate tendency toward action and initiative',
            'Strong primary resonance - immediate reactions',
            'Balanced social orientation',
            'Strong intuitive thinking patterns',
            'Moderate logical reasoning preference'
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
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px; margin-bottom: 2rem; color: white; text-align: center;">
        <h1>📊 Character Analysis Dashboard</h1>
        <p>Based on René Le Senne's Characterology Framework</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Radar chart
        fig = create_character_radar_chart()
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Current analysis summary
        st.markdown("### 📋 Analysis Summary")
        
        st.metric("Sessions Analyzed", "12", "+3")
        st.metric("Character Confidence", "85%", "+5%")
        st.metric("Traits Identified", "8", "+2")
        
        st.markdown("### 🎯 Key Insights")
        st.info("🔍 Strong intuitive patterns detected")
        st.info("⚡ High emotional responsiveness")
        st.info("🤔 Secondary resonance tendencies")
        st.info("🌟 Balanced extraversion levels")
    
    # Character type display
    create_character_type_display()
    
    # Traits breakdown
    create_traits_breakdown()
    
    # Sidebar with analysis tools
    with st.sidebar:
        st.markdown("### 🛠️ Analysis Tools")
        
        if st.button("🔄 Refresh Analysis", use_container_width=True):
            st.success("Analysis refreshed with latest session data!")
        
        if st.button("📊 Detailed Report", use_container_width=True):
            st.info("Navigate to Reports page to generate detailed analysis.")
        
        if st.button("💾 Export Data", use_container_width=True):
            st.success("Analysis data exported successfully!")
        
        st.markdown("---")
        st.markdown("### ⏰ Analysis History")
        st.markdown("- **Today**: Character profile updated")
        st.markdown("- **Yesterday**: 3 new traits identified")
        st.markdown("- **Last Week**: Major personality shift detected")
        
        st.markdown("---")
        st.markdown("### 📚 Le Senne's Framework")
        st.markdown("**Three Primary Factors:**")
        st.markdown("- **E**motionality (E/nE)")
        st.markdown("- **A**ctivity (A/nA)")  
        st.markdown("- **R**esonance (P/S)")
        st.markdown("**8 Character Types:**")
        st.markdown("- Nervous (EnAP)")
        st.markdown("- Sanguine (EAP)")
        st.markdown("- Choleric (EAS)")
        st.markdown("- Melancholic (EnAS)")
        st.markdown("- And 4 more...")

if __name__ == "__main__":
    main()