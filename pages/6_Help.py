"""
Help and Documentation Page
Comprehensive FAQ and user guide
"""

import streamlit as st

st.set_page_config(
    page_title="Help - CarIActerology",
    page_icon="❓",
    layout="wide"
)

def main():
    """Main help and documentation page"""
    
    # Custom CSS for help page
    st.markdown("""
    <style>
        .help-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
        .faq-section {
            background: #f8f9fc;
            border: 1px solid #e1e5e9;
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        .quick-nav {
            background: #e8f4fd;
            border-left: 4px solid #2196F3;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
        }
        .tip-box {
            background: #fff3cd;
            border: 1px solid #ffd700;
            border-radius: 6px;
            padding: 1rem;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="help-header">
        <h1>❓ Help & Documentation</h1>
        <p>Everything you need to know about CarIActerology</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick navigation
    st.markdown("""
    <div class="quick-nav">
        <h4>📍 Quick Navigation</h4>
        <ul>
            <li><strong>Getting Started:</strong> New user guide and first steps</li>
            <li><strong>Features:</strong> Detailed explanation of all platform features</li>
            <li><strong>Characterology:</strong> Understanding René Le Senne's framework</li>
            <li><strong>Privacy & Data:</strong> How your information is handled</li>
            <li><strong>Troubleshooting:</strong> Common issues and solutions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🚀 Getting Started", 
        "✨ Features", 
        "📚 Characterology", 
        "🔒 Privacy & Data", 
        "🔧 Troubleshooting"
    ])
    
    with tab1:
        st.markdown("## 🚀 Getting Started with CarIActerology")
        
        with st.expander("❓ What is CarIActerology?", expanded=True):
            st.markdown("""
            CarIActerology is an AI-powered psychological self-discovery platform based on René Le Senne's characterology. 
            It helps you understand your personality through meaningful conversations and provides detailed analysis 
            based on classical psychological frameworks.
            
            **Key Benefits:**
            - Discover your character type among Le Senne's 8 classifications
            - Track personality development over time
            - Get personalized insights and recommendations
            - Generate professional psychological reports
            """)
        
        with st.expander("🎯 First Steps - New User Guide"):
            st.markdown("""
            **1. Start with a Conversation**
            - Click "Start Chat" on the homepage
            - Share your thoughts, experiences, and feelings openly
            - Be specific about situations and your reactions
            
            **2. Review Your Analysis**
            - Visit the Analysis page to see your personality profile
            - Check your character type and confidence score
            - Explore the radar chart showing your traits
            
            **3. Track Your Progress**
            - Use the Dashboard to monitor your journey
            - Review session statistics and insights
            - Watch your personality profile evolve over time
            
            **4. Generate Reports**
            - Create PDF reports of your psychological insights
            - Share with professionals or keep for personal reflection
            - Export data for external analysis
            
            **5. Customize Your Experience**
            - Adjust preferences in Settings
            - Manage privacy controls
            - Set up notifications and themes
            """)
        
        with st.expander("💡 Tips for Better Results"):
            st.markdown("""
            **Conversation Quality:**
            - Be honest and authentic in your responses
            - Share specific examples, not general statements
            - Discuss various life areas (work, relationships, challenges)
            - Talk about your decision-making processes
            
            **Examples of Good vs. Poor Responses:**
            
            ✅ **Good:** "When I'm in a conflict, I usually try to understand the other person's perspective first, then find a compromise that works for everyone."
            
            ❌ **Poor:** "I don't like conflicts."
            
            ✅ **Good:** "Under pressure, I become very focused and organized. I make lists, prioritize tasks, and work methodically through problems."
            
            ❌ **Poor:** "Pressure is stressful."
            """)
    
    with tab2:
        st.markdown("## ✨ Platform Features")
        
        feature_sections = {
            "💬 Chat Interface": {
                "description": "Interactive conversation with AI psychologist",
                "features": [
                    "Real-time psychological analysis of responses",
                    "Contextual follow-up questions",
                    "Session saving and history",
                    "Conversation export options",
                    "Progress tracking during chat"
                ],
                "tips": "Share detailed, specific experiences for better analysis"
            },
            "📊 Analysis Dashboard": {
                "description": "Comprehensive personality profile visualization",
                "features": [
                    "Character type identification (Le Senne's 8 types)",
                    "Interactive radar charts showing 8 personality dimensions",
                    "Confidence scoring based on data quality",
                    "Strengths and growth areas identification",
                    "Character evolution timeline"
                ],
                "tips": "Visit regularly to see how your profile evolves with more conversations"
            },
            "📈 Progress Dashboard": {
                "description": "Track your self-discovery journey over time",
                "features": [
                    "Session statistics and metrics",
                    "Insights collection and categorization",
                    "Achievement milestones",
                    "Timeline visualization",
                    "Progress analytics"
                ],
                "tips": "Review weekly to understand your development patterns"
            },
            "📄 Reports System": {
                "description": "Generate professional psychological reports",
                "features": [
                    "Comprehensive PDF reports with analysis",
                    "Multiple report types (analysis, progress, character)",
                    "Professional formatting suitable for sharing",
                    "Historical report access",
                    "Custom report generation options"
                ],
                "tips": "Generate reports monthly to track long-term changes"
            },
            "⚙️ Settings & Privacy": {
                "description": "Customize your experience and manage data",
                "features": [
                    "Privacy controls and data management",
                    "Theme and appearance customization",
                    "Notification preferences",
                    "Account information management",
                    "Data export and deletion options"
                ],
                "tips": "Review privacy settings regularly and export data for backup"
            }
        }
        
        for feature_name, details in feature_sections.items():
            with st.expander(f"{feature_name}"):
                st.markdown(f"**{details['description']}**")
                st.markdown("**Key Features:**")
                for feature in details['features']:
                    st.markdown(f"- {feature}")
                
                st.markdown(f"**💡 Tip:** {details['tips']}")
    
    with tab3:
        st.markdown("## 📚 Understanding Characterology")
        
        with st.expander("🧠 René Le Senne's Framework", expanded=True):
            st.markdown("""
            **Historical Context:**
            René Le Senne (1882-1954) was a French philosopher and psychologist who developed a comprehensive 
            characterology system published in his "Treatise on Characterology" (1945). His framework 
            remains one of the most systematic approaches to personality classification.
            
            **The Three Primary Factors:**
            
            **1. Emotionality (E / nE)**
            - **Emotional (E):** Strong reactions to stimuli, deeply affected by experiences
            - **Non-Emotional (nE):** Calm, stable responses, less affected by external events
            
            **2. Activity (A / nA)**
            - **Active (A):** High initiative, tendency to act and engage
            - **Non-Active (nA):** Passive, contemplative, prefers reflection to action
            
            **3. Resonance (P / S)**
            - **Primary (P):** Immediate, present-focused, spontaneous responses
            - **Secondary (S):** Reflective, future-focused, considers long-term consequences
            """)
        
        with st.expander("🎭 The Eight Character Types"):
            st.markdown("""
            | Type | Formula | Description | Key Traits |
            |------|---------|-------------|------------|
            | **Nervous** | EnAP | Emotional, inactive, primary | Sensitive, anxious, immediate reactions |
            | **Sanguine** | EAP | Emotional, active, primary | Optimistic, social, spontaneous |
            | **Choleric** | EAS | Emotional, active, secondary | Passionate, driven, strategic |
            | **Melancholic** | EnAS | Emotional, inactive, secondary | Thoughtful, introspective, deep |
            | **Phlegmatic** | nEnAS | Non-emotional, inactive, secondary | Calm, systematic, thorough |
            | **Apathetic** | nEnAP | Non-emotional, inactive, primary | Indifferent, adaptable, present-focused |
            | **Amorphous** | nEAP | Non-emotional, active, primary | Flexible, practical, immediate |
            | **Passionate** | nEAS | Non-emotional, active, secondary | Determined, methodical, long-term |
            """)
        
        with st.expander("📊 How Analysis Works"):
            st.markdown("""
            **Data Collection:**
            - Conversational content analysis
            - Response pattern recognition
            - Emotional language detection
            - Decision-making style identification
            
            **AI Analysis Process:**
            1. **Text Processing:** Natural language understanding of your responses
            2. **Pattern Recognition:** Identification of behavioral patterns
            3. **Factor Scoring:** Assessment of Emotionality, Activity, and Resonance
            4. **Type Classification:** Mapping to one of the 8 character types
            5. **Confidence Calculation:** Based on data quality and consistency
            
            **Continuous Learning:**
            - Profile updates with each conversation
            - Increased accuracy over time
            - Evolution tracking and trend analysis
            """)
    
    with tab4:
        st.markdown("## 🔒 Privacy & Data Management")
        
        with st.expander("🛡️ Data Privacy Policy", expanded=True):
            st.markdown("""
            **What We Collect:**
            - Conversation content (for analysis purposes only)
            - Usage patterns and session data
            - Analysis results and generated insights
            - User preferences and settings
            
            **How We Use Your Data:**
            - Generate personality analysis and insights
            - Improve AI models and analysis accuracy
            - Provide personalized recommendations
            - Track your personal development over time
            
            **Data Storage & Security:**
            - All data encrypted in transit and at rest
            - Secure cloud storage with access controls
            - Regular security audits and updates
            - No data sharing with third parties without consent
            
            **Your Rights:**
            - Access all your stored data
            - Export data in standard formats
            - Delete specific conversations or all data
            - Opt-out of analysis or data collection
            """)
        
        with st.expander("⚙️ Managing Your Data"):
            st.markdown("""
            **In Settings > Data Management:**
            
            **Export Options:**
            - Download conversation history (JSON/CSV)
            - Export analysis results (PDF/JSON)
            - Get complete data package
            
            **Deletion Options:**
            - Delete individual conversations
            - Clear specific date ranges
            - Complete account data deletion
            - Selective insight removal
            
            **Privacy Controls:**
            - Pause data collection temporarily
            - Limit analysis sharing
            - Control report generation
            - Manage third-party integrations
            """)
        
        with st.expander("🔐 Security Best Practices"):
            st.markdown("""
            **For Your Security:**
            - Use strong, unique passwords
            - Enable two-factor authentication if available
            - Regularly review account activity
            - Keep browser and apps updated
            
            **What We Do:**
            - Regular security assessments
            - Encrypted data transmission
            - Access logging and monitoring
            - Incident response procedures
            
            **Reporting Security Issues:**
            Contact our security team immediately if you notice:
            - Unauthorized account access
            - Unusual activity patterns
            - Suspicious communications
            - Data integrity concerns
            """)
    
    with tab5:
        st.markdown("## 🔧 Troubleshooting & Support")
        
        with st.expander("❗ Common Issues & Solutions"):
            st.markdown("""
            **Chat Interface Issues:**
            
            **Problem:** Messages not sending
            - **Solution:** Check internet connection, refresh page, try shorter messages
            
            **Problem:** AI responses seem generic
            - **Solution:** Provide more specific, detailed information in your messages
            
            **Problem:** Session not saving
            - **Solution:** Click "Save Conversation" button, check browser settings for cookies
            
            **Analysis Page Issues:**
            
            **Problem:** Analysis not updating
            - **Solution:** Click "Refresh Analysis" or have more conversations for better data
            
            **Problem:** Low confidence scores
            - **Solution:** Engage in longer, more detailed conversations across different topics
            
            **Problem:** Charts not loading
            - **Solution:** Disable ad blockers, enable JavaScript, try different browser
            
            **Reports Generation Issues:**
            
            **Problem:** PDF not downloading
            - **Solution:** Check popup blockers, try different browser, clear cache
            
            **Problem:** Report appears empty
            - **Solution:** Ensure you have sufficient conversation data for report generation
            """)
        
        with st.expander("💻 Browser Compatibility"):
            st.markdown("""
            **Recommended Browsers:**
            - Chrome 90+ (Recommended)
            - Firefox 88+
            - Safari 14+
            - Edge 90+
            
            **Required Features:**
            - JavaScript enabled
            - Cookies enabled
            - Local storage available
            - Pop-up blockers configured
            
            **If you experience issues:**
            - Clear browser cache and cookies
            - Disable browser extensions temporarily
            - Try incognito/private browsing mode
            - Update to latest browser version
            """)
        
        with st.expander("📞 Getting Support"):
            st.markdown("""
            **Self-Help Resources:**
            - Review this help documentation
            - Check the FAQ sections above
            - Try the troubleshooting steps
            
            **Contact Support:**
            - Email: support@cariacterology.com
            - Response time: Within 24 hours
            - Include: Browser type, error messages, steps to reproduce
            
            **Feature Requests:**
            - Submit via Settings > Feedback
            - Join our user community forum
            - Follow development updates
            
            **Emergency Issues:**
            - Data loss or security concerns
            - Contact immediately: emergency@cariacterology.com
            - Include account details and issue description
            """)
    
    # Footer with additional resources
    st.markdown("---")
    st.markdown("""
    <div class="tip-box">
        <h4>📚 Additional Resources</h4>
        <ul>
            <li><strong>Academic Background:</strong> René Le Senne's "Treatise on Characterology" (1945)</li>
            <li><strong>Modern Applications:</strong> AI-powered personality analysis in therapeutic settings</li>
            <li><strong>Related Fields:</strong> Psychology, personality assessment, self-development</li>
            <li><strong>Community:</strong> Join discussions with other users exploring characterology</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()