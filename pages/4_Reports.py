"""
Reports Page
Generate and manage psychological analysis reports
"""

import streamlit as st
from datetime import datetime, timedelta
import io
import base64
import sys
import os

# Add the project root to Python path for module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.report_generator import generate_report, get_available_report_types

st.set_page_config(
    page_title="Reports - CarIActerology",
    page_icon="📄",
    layout="wide"
)

def generate_mock_report_content():
    """Generate mock report content"""
    
    report_content = f"""
# Psychological Analysis Report
**CarIActerology Platform - Based on René Le Senne's Characterology**

---

## Personal Information
- **Report Date**: {datetime.now().strftime('%B %d, %Y')}
- **Analysis Period**: {(datetime.now() - timedelta(days=30)).strftime('%B %d')} - {datetime.now().strftime('%B %d, %Y')}
- **Total Sessions**: 28
- **Total Analysis Time**: 12 hours 35 minutes

---

## Executive Summary

Based on extensive analysis of your conversations and responses over the past month, your psychological profile indicates a **Sanguine character type** with secondary **Nervous** tendencies according to Le Senne's characterology framework.

### Key Findings:
- **Primary Character Type**: Sanguine (EAP) - 85% confidence
- **Secondary Tendencies**: Nervous (EnAP) - 68% confidence
- **Emotional Responsiveness**: High (8.2/10)
- **Activity Level**: High (7.8/10)
- **Resonance Type**: Primary (immediate reactions)

---

## Character Analysis

### Emotionality (E) - Score: 82/100
You demonstrate high emotional responsiveness to both internal thoughts and external stimuli. This manifests in:
- Quick emotional reactions to interpersonal situations
- Rich inner emotional life
- Strong empathy and emotional intelligence
- Tendency to be moved by beauty, art, and meaningful experiences

### Activity (A) - Score: 78/100
Your activity level indicates a strong drive toward action and engagement:
- Preference for dynamic, engaging activities
- Initiative in social and professional situations
- Goal-oriented behavior with sustained effort
- Discomfort with prolonged periods of inactivity

### Primary Resonance (P) - Score: 85/100
Your responses suggest primary resonance characteristics:
- Immediate, spontaneous reactions to situations
- Present-focused attention and decision-making
- Adaptability and flexibility in changing circumstances
- Strong intuitive responses to people and situations

---

## Personality Insights

### Strengths Identified:
1. **Emotional Intelligence**: Exceptional ability to read and respond to others' emotions
2. **Adaptability**: Quick adjustment to new situations and changing circumstances
3. **Social Engagement**: Natural ability to connect with others and build relationships
4. **Initiative**: Strong drive to take action and pursue goals
5. **Intuitive Thinking**: Excellent pattern recognition and holistic understanding

### Areas for Development:
1. **Emotional Regulation**: Occasional overwhelm from high emotional responsiveness
2. **Deep Reflection**: Tendency toward quick decisions may benefit from more deliberation
3. **Consistency**: Primary resonance can lead to inconsistent long-term planning
4. **Stress Management**: High activity and emotionality can create stress under pressure

---

## Therapeutic Recommendations

### For Personal Growth:
- **Mindfulness Practice**: 10-15 minutes daily to balance emotional responsiveness
- **Structured Reflection**: Weekly journaling to capture insights and patterns
- **Goal Setting**: Monthly review of long-term objectives to maintain direction
- **Energy Management**: Balance high-activity periods with adequate rest

### For Relationships:
- **Communication**: Leverage natural empathy while practicing active listening
- **Boundaries**: Learn to recognize and communicate emotional limits
- **Conflict Resolution**: Use emotional intelligence constructively in disagreements

### For Professional Development:
- **Leadership Roles**: Your character type excels in motivating and inspiring others
- **Creative Fields**: High emotionality and intuition suit creative endeavors
- **People-Centered Work**: Natural fit for counseling, teaching, or team leadership
- **Dynamic Environments**: Thrive in roles requiring adaptability and quick thinking

---

## Session Analysis

### Most Productive Sessions:
1. **Session #15** (Jan 15): Breakthrough insight about emotional patterns - 95% confidence
2. **Session #22** (Jan 22): Deep exploration of social dynamics - 92% confidence  
3. **Session #27** (Jan 27): Career values alignment discussion - 90% confidence

### Key Themes Explored:
- Personal relationships and social dynamics (42% of discussion time)
- Professional growth and career alignment (28% of discussion time)
- Emotional regulation and self-awareness (18% of discussion time)
- Creative expression and personal interests (12% of discussion time)

---

## Progress Tracking

### Character Confidence Evolution:
- **Week 1**: 65% - Initial profile establishment
- **Week 2**: 74% - Pattern recognition and validation
- **Week 3**: 81% - Deep insight integration
- **Week 4**: 85% - Stable profile with high confidence

### Insights Generated: 45 total
- **Personality Traits**: 18 insights
- **Emotional Patterns**: 12 insights
- **Behavioral Tendencies**: 8 insights
- **Social Dynamics**: 7 insights

---

## Comparison with Character Types

### Sanguine Type Match (85%):
- ✅ High emotionality and activity
- ✅ Primary resonance tendencies
- ✅ Social engagement and adaptability
- ✅ Spontaneous and expressive nature

### Secondary Considerations:
- **Nervous Type (68%)**: Shares high emotionality and primary resonance
- **Choleric Type (45%)**: Similar activity levels but different resonance pattern

---

## Future Development Plan

### Short-term Goals (1-3 months):
1. Implement daily mindfulness practice
2. Establish weekly reflection routine
3. Develop stress management techniques
4. Enhance emotional regulation skills

### Medium-term Goals (3-6 months):
1. Apply insights to professional development
2. Strengthen relationship communication patterns
3. Explore creative expression opportunities
4. Build consistent long-term planning habits

### Long-term Goals (6+ months):
1. Integrate characterological insights into life decisions
2. Mentor others in self-discovery processes
3. Develop expertise in areas aligned with character strengths
4. Maintain balanced emotional and activity levels

---

## Methodology Notes

This analysis is based on René Le Senne's *Treatise on Characterology* (1945) and modern psychological assessment techniques. The AI system analyzed:
- 28 conversation sessions
- 156 psychological indicators
- 8 character type correlations
- Multiple validation approaches

**Confidence Level**: 85% - High reliability based on consistent patterns across multiple sessions and validation methods.

---

*This report is generated by the CarIActerology AI system and should be used as a tool for self-reflection and personal development. For clinical or therapeutic needs, please consult with a qualified mental health professional.*

**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Version**: CarIActerology v1.0
**Analysis Engine**: OpenAI Agents SDK with Mem0 Memory System
"""
    
    return report_content

def create_report_preview(report_type):
    """Create a preview of the selected report"""
    
    if report_type == "Complete Psychological Profile":
        st.markdown("### 📋 Complete Psychological Profile Preview")
        st.markdown("**Duration**: Comprehensive analysis of all sessions")
        st.markdown("**Content**: Character type, traits, insights, recommendations")
        
        with st.expander("Preview Content"):
            st.markdown("""
            - Executive Summary
            - Character Type Analysis (Sanguine - 85% confidence)
            - Personality Traits Breakdown
            - 45 Key Insights from 28 sessions
            - Therapeutic Recommendations
            - Future Development Plan
            """)
    
    elif report_type == "Session Summary":
        st.markdown("### 📝 Session Summary Preview")
        st.markdown("**Duration**: Last 7 sessions")
        st.markdown("**Content**: Recent insights, progress, key themes")
        
        with st.expander("Preview Content"):
            st.markdown("""
            - Recent session highlights
            - 8 new insights identified
            - Progress toward character understanding
            - Emerging patterns and themes
            """)
    
    elif report_type == "Character Evolution":
        st.markdown("### 📈 Character Evolution Preview")
        st.markdown("**Duration**: Full historical analysis")
        st.markdown("**Content**: Character development over time")
        
        with st.expander("Preview Content"):
            st.markdown("""
            - Character confidence progression (65% → 85%)
            - Trait stability analysis
            - Insight accumulation patterns
            - Development milestones
            """)

def create_download_button(report_content, filename):
    """Create a download button for the report"""
    
    # Convert to bytes
    report_bytes = report_content.encode('utf-8')
    b64_report = base64.b64encode(report_bytes).decode()
    
    # Create download link
    href = f'<a href="data:text/markdown;base64,{b64_report}" download="{filename}.md">📥 Download Report</a>'
    st.markdown(href, unsafe_allow_html=True)

def main():
    """Main reports interface with professional PDF generation"""
    
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
        .reports-help {
            background: #e8f4fd;
            border: 1px solid #2196F3;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with help tooltip
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px; margin-bottom: 2rem; color: white; text-align: center;">
        <h1>📄 Professional Analysis Reports 
            <span class="help-tooltip">❓
                <span class="tooltiptext">
                    Generate professional PDF reports of your psychological analysis, perfect for personal reflection or sharing with mental health professionals. Reports include character analysis, progress tracking, and insights.
                </span>
            </span>
        </h1>
        <p>Generate comprehensive PDF reports using advanced psychological analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # First-time user guidance
    if "reports_visited" not in st.session_state:
        st.session_state.reports_visited = True
        with st.expander("📋 Report Generation Guide - Click to Learn More", expanded=True):
            st.markdown("""
            <div class="reports-help">
                <h4>📖 Types of Reports Available</h4>
                <ul>
                    <li><strong>Character Analysis Report:</strong> Detailed breakdown of your personality type and traits</li>
                    <li><strong>Progress Report:</strong> Track your personal development over time</li>
                    <li><strong>Session Summary:</strong> Summary of insights from recent conversations</li>
                </ul>
                
                <h4>💡 Best Practices for Reports</h4>
                <ul>
                    <li>Generate reports monthly to track long-term changes</li>
                    <li>Share with therapists or counselors for professional insight</li>
                    <li>Keep personal copies for reflection and goal-setting</li>
                    <li>Compare reports over time to see growth patterns</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Report generation section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Generate Professional Report")
        
        # Get available report types
        available_reports = get_available_report_types()
        
        # Report type selection with descriptions
        st.markdown("**Select Report Type:**")
        
        selected_report = None
        for report_key, report_info in available_reports.items():
            if st.button(
                f"📋 {report_info['name']}", 
                key=f"select_{report_key}",
                use_container_width=True
            ):
                selected_report = report_key
        
        # Display report details if selected
        if selected_report or 'selected_report_type' in st.session_state:
            if selected_report:
                st.session_state.selected_report_type = selected_report
            
            report_info = available_reports[st.session_state.selected_report_type]
            
            # Report details
            st.markdown(f"### 📄 {report_info['name']}")
            st.markdown(f"**Description:** {report_info['description']}")
            st.markdown(f"**Length:** {report_info['pages']}")
            
            st.markdown("**Includes:**")
            for item in report_info['includes']:
                st.markdown(f"• {item}")
            
            st.markdown("---")
            
            # Generation options
            st.markdown("**Report Options:**")
            
            col_opt1, col_opt2 = st.columns(2)
            with col_opt1:
                include_charts = st.checkbox("Include visualizations", value=True, key="include_charts")
                confidential_header = st.checkbox("Confidential header", value=True, key="confidential")
            
            with col_opt2:
                professional_format = st.checkbox("Professional formatting", value=True, key="professional")
                detailed_analysis = st.checkbox("Detailed analysis", value=True, key="detailed")
            
            # Generate button
            if st.button("🔄 Generate Professional PDF Report", use_container_width=True, key="generate_pdf"):
                with st.spinner("Generating your professional psychological analysis report..."):
                    try:
                        # Generate the PDF report
                        pdf_buffer = generate_report(st.session_state.selected_report_type)
                        
                        st.success("✅ Professional PDF report generated successfully!")
                        
                        # Create download button
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"{report_info['name'].replace(' ', '_')}_{timestamp}.pdf"
                        
                        st.download_button(
                            label="📥 Download PDF Report",
                            data=pdf_buffer,
                            file_name=filename,
                            mime="application/pdf",
                            use_container_width=True
                        )
                        
                        # Display preview message
                        st.info("📋 Your professional PDF report is ready for download. The report includes comprehensive analysis, visualizations, and personalized recommendations based on René Le Senne's characterology framework.")
                        
                    except Exception as e:
                        st.error(f"Error generating report: {str(e)}")
                        st.info("Please try again or contact support if the issue persists.")
        else:
            st.info("👆 Please select a report type above to continue.")
    
    with col2:
        # Report types info
        st.markdown("### 🎯 Report Types")
        
        available_reports = get_available_report_types()
        
        for report_key, report_info in available_reports.items():
            with st.expander(f"📋 {report_info['name']}"):
                st.markdown(f"**Pages:** {report_info['pages']}")
                st.markdown(f"**Description:** {report_info['description']}")
                st.markdown("**Content:**")
                for item in report_info['includes']:
                    st.markdown(f"• {item}")
        
        # Quick stats
        st.markdown("---")
        st.markdown("### 📊 Report Features")
        st.success("✅ Professional PDF formatting")
        st.success("✅ René Le Senne framework")
        st.success("✅ Comprehensive analysis")
        st.success("✅ Personalized insights")
        st.success("✅ Visual charts included")
        st.success("✅ Therapeutic recommendations")
        
        # Export info
        st.markdown("---")
        st.markdown("### 💡 Report Benefits")
        
        st.info("""
        **Professional Quality**
        • Hospital-grade formatting
        • Suitable for healthcare sharing
        • Evidence-based analysis
        """)
        
        st.info("""
        **Comprehensive Content**
        • Character type analysis
        • Progress tracking
        • Actionable recommendations
        """)
        
        st.info("""
        **Privacy & Security**
        • Confidential formatting
        • Secure generation
        • Personal use focused
        """)
        
        # Additional features
        st.markdown("### 🔧 Advanced Features")
        
        if st.button("📧 Email Report", use_container_width=True, key="email_report"):
            st.info("Feature coming soon: Direct email delivery")
        
        if st.button("👨‍⚕️ Share with Provider", use_container_width=True, key="share_provider"):
            st.info("Feature coming soon: Secure healthcare sharing")
    
    # Footer with information
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; padding: 1rem;">
        <p><strong>About Your Reports</strong></p>
        <p>All reports are generated using René Le Senne's characterology framework combined with modern AI analysis. 
        Reports are based on your conversation data and should be used for personal development and self-reflection.</p>
        <p><em>For clinical or therapeutic needs, please consult with a qualified mental health professional.</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()