"""
Settings Page
User preferences, privacy controls, and account management
"""

import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Settings - CarIActerology",
    page_icon="⚙️",
    layout="wide"
)

def main():
    """Main settings interface"""
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px; margin-bottom: 2rem; color: white; text-align: center;">
        <h1>⚙️ Settings & Preferences</h1>
        <p>Manage your account, privacy, and application preferences</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Settings tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["👤 Profile", "🔒 Privacy", "🎨 Interface", "🔔 Notifications", "💾 Data"])
    
    with tab1:
        st.markdown("### 👤 User Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Personal Information**")
            
            name = st.text_input("Full Name", value="Dr. Sarah Johnson")
            email = st.text_input("Email Address", value="sarah.johnson@example.com")
            
            # Age range for psychological context
            age_range = st.selectbox(
                "Age Range",
                ["18-25", "26-35", "36-45", "46-55", "56-65", "65+"],
                index=2
            )
            
            # Professional context
            profession = st.selectbox(
                "Profession",
                ["Healthcare", "Education", "Technology", "Business", "Arts & Creative", "Other"],
                index=1
            )
            
            # Goals for using the platform
            st.markdown("**Goals for Self-Discovery**")
            goals = st.multiselect(
                "What do you hope to achieve?",
                [
                    "Better understand my personality",
                    "Improve relationships", 
                    "Career guidance",
                    "Personal growth",
                    "Emotional intelligence",
                    "Stress management",
                    "Decision making",
                    "Communication skills"
                ],
                default=["Better understand my personality", "Personal growth"]
            )
        
        with col2:
            st.markdown("**Profile Summary**")
            
            # Profile picture placeholder
            st.image("https://via.placeholder.com/150x150/667eea/white?text=SJ", width=150)
            
            if st.button("Change Picture"):
                st.info("Picture upload feature coming soon!")
            
            st.markdown("**Account Information**")
            st.info(f"**Member since**: January 1, 2024")
            st.info(f"**Total sessions**: 28")
            st.info(f"**Character confidence**: 85%")
            st.info(f"**Primary character type**: Sanguine")
            
            st.markdown("**Subscription Plan**")
            st.success("✅ **Premium Plan** - All features unlocked")
            
            if st.button("Manage Subscription"):
                st.info("Redirecting to subscription management...")
        
        # Save profile changes
        if st.button("💾 Save Profile Changes", use_container_width=True):
            st.success("Profile updated successfully!")
    
    with tab2:
        st.markdown("### 🔒 Privacy & Security")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Data Privacy Controls**")
            
            # Privacy settings
            data_retention = st.selectbox(
                "Data Retention Period",
                ["1 year", "2 years", "5 years", "Indefinite"],
                index=1
            )
            
            allow_analytics = st.checkbox("Allow anonymized usage analytics", value=True)
            allow_research = st.checkbox("Contribute data to psychological research", value=False)
            allow_sharing = st.checkbox("Allow sharing insights with healthcare providers", value=False)
            
            st.markdown("**Memory Management**")
            auto_forget = st.checkbox("Auto-forget sensitive conversations", value=True)
            memory_encryption = st.checkbox("Encrypt stored memories", value=True)
            
            # Memory categories to store
            st.markdown("**What to Remember**")
            remember_categories = st.multiselect(
                "Categories to store in long-term memory",
                [
                    "Personality insights",
                    "Character analysis",
                    "Emotional patterns", 
                    "Behavioral tendencies",
                    "Personal preferences",
                    "Goals and aspirations",
                    "Relationship dynamics",
                    "Professional insights"
                ],
                default=["Personality insights", "Character analysis", "Emotional patterns"]
            )
        
        with col2:
            st.markdown("**Security Settings**")
            
            # Password change
            if st.button("🔐 Change Password"):
                st.info("Password change form would appear here")
            
            # Two-factor authentication
            two_factor = st.checkbox("Enable Two-Factor Authentication", value=False)
            if two_factor:
                st.info("📱 Two-factor authentication setup would begin here")
            
            # Session security
            st.markdown("**Session Security**")
            auto_logout = st.selectbox(
                "Auto-logout after inactivity",
                ["15 minutes", "30 minutes", "1 hour", "2 hours", "Never"],
                index=2
            )
            
            # Privacy summary
            st.markdown("**Privacy Summary**")
            st.info("🔒 Your conversations are encrypted")
            st.info("🛡️ No data sold to third parties")
            st.info("🏥 HIPAA-compliant storage")
            st.info("🌍 GDPR compliant")
            
            if st.button("📋 Download Privacy Report"):
                st.success("Privacy report generated and downloaded!")
        
        # Privacy actions
        col3, col4 = st.columns(2)
        with col3:
            if st.button("🗑️ Delete Specific Data", use_container_width=True):
                st.warning("Data deletion interface would appear here")
        
        with col4:
            if st.button("📤 Export All Data", use_container_width=True):
                st.success("Data export initiated!")
    
    with tab3:
        st.markdown("### 🎨 Interface & Experience")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Visual Preferences**")
            
            # Theme selection
            theme = st.selectbox(
                "Application Theme",
                ["Light", "Dark", "Auto (System)", "Therapeutic Blue"],
                index=3
            )
            
            # Color scheme
            primary_color = st.color_picker("Primary Accent Color", "#667eea")
            
            # Font preferences
            font_size = st.selectbox(
                "Font Size",
                ["Small", "Medium", "Large", "Extra Large"],
                index=1
            )
            
            # Layout preferences
            sidebar_default = st.selectbox(
                "Default Sidebar State",
                ["Expanded", "Collapsed", "Auto"],
                index=0
            )
            
            st.markdown("**Dashboard Layout**")
            dashboard_cards = st.multiselect(
                "Show on dashboard",
                [
                    "Session metrics",
                    "Character confidence", 
                    "Recent insights",
                    "Mood tracking",
                    "Progress timeline",
                    "Quick actions",
                    "Achievement badges"
                ],
                default=["Session metrics", "Character confidence", "Recent insights"]
            )
        
        with col2:
            st.markdown("**Interaction Preferences**")
            
            # Chat settings
            typing_speed = st.slider("AI Response Speed", min_value=1, max_value=5, value=3)
            show_timestamps = st.checkbox("Show message timestamps", value=True)
            markdown_rendering = st.checkbox("Enable rich text formatting", value=True)
            
            # Analysis preferences
            st.markdown("**Analysis Display**")
            show_confidence = st.checkbox("Show confidence scores", value=True)
            animated_charts = st.checkbox("Animated visualizations", value=True)
            detailed_explanations = st.checkbox("Show detailed trait explanations", value=True)
            
            # Accessibility
            st.markdown("**Accessibility**")
            high_contrast = st.checkbox("High contrast mode", value=False)
            screen_reader = st.checkbox("Screen reader optimizations", value=False)
            keyboard_nav = st.checkbox("Enhanced keyboard navigation", value=False)
            
            # Preview
            st.markdown("**Theme Preview**")
            if theme == "Therapeutic Blue":
                st.markdown("""
                <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <h4>Therapeutic Blue Theme</h4>
                    <p>Calming colors designed for psychological well-being</p>
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("🎨 Apply Interface Changes", use_container_width=True):
            st.success("Interface preferences updated!")
    
    with tab4:
        st.markdown("### 🔔 Notifications & Reminders")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Session Reminders**")
            
            session_reminders = st.checkbox("Enable session reminders", value=True)
            
            if session_reminders:
                reminder_frequency = st.selectbox(
                    "Reminder Frequency",
                    ["Daily", "Every 2 days", "Weekly", "Custom"],
                    index=2
                )
                
                reminder_time = st.time_input("Preferred reminder time", value=datetime.strptime("19:00", "%H:%M").time())
            
            st.markdown("**Progress Notifications**")
            milestone_notifications = st.checkbox("Character milestone notifications", value=True)
            insight_notifications = st.checkbox("New insight notifications", value=True)
            weekly_summary = st.checkbox("Weekly progress summary", value=True)
            
            st.markdown("**System Notifications**")
            maintenance_notifications = st.checkbox("Maintenance notifications", value=True)
            feature_updates = st.checkbox("New feature announcements", value=True)
            security_alerts = st.checkbox("Security alerts", value=True)
        
        with col2:
            st.markdown("**Delivery Preferences**")
            
            # Notification channels
            notification_channels = st.multiselect(
                "Notification Channels",
                ["Email", "In-app", "Push notifications", "SMS"],
                default=["Email", "In-app"]
            )
            
            # Email preferences
            st.markdown("**Email Notifications**")
            email_frequency = st.selectbox(
                "Email Frequency",
                ["Immediate", "Daily digest", "Weekly digest", "Never"],
                index=1
            )
            
            # Content preferences
            st.markdown("**Content Preferences**")
            include_tips = st.checkbox("Include psychological tips", value=True)
            include_quotes = st.checkbox("Include inspirational quotes", value=True)
            include_articles = st.checkbox("Include related articles", value=False)
            
            # Quiet hours
            st.markdown("**Quiet Hours**")
            enable_quiet_hours = st.checkbox("Enable quiet hours", value=True)
            
            if enable_quiet_hours:
                col_quiet1, col_quiet2 = st.columns(2)
                with col_quiet1:
                    quiet_start = st.time_input("From", value=datetime.strptime("22:00", "%H:%M").time())
                with col_quiet2:
                    quiet_end = st.time_input("To", value=datetime.strptime("08:00", "%H:%M").time())
        
        if st.button("🔔 Save Notification Settings", use_container_width=True):
            st.success("Notification preferences updated!")
    
    with tab5:
        st.markdown("### 💾 Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Data Overview**")
            
            # Storage usage
            st.metric("Storage Used", "2.4 GB", "of 10 GB")
            
            # Data breakdown
            data_breakdown = {
                "Conversation History": "1.2 GB",
                "Analysis Data": "800 MB", 
                "Generated Reports": "350 MB",
                "User Preferences": "50 MB"
            }
            
            for category, size in data_breakdown.items():
                st.markdown(f"**{category}**: {size}")
            
            st.markdown("**Data Health**")
            st.success("✅ All data backed up")
            st.success("✅ No corruption detected")
            st.success("✅ Encryption active")
            
            # Backup settings
            st.markdown("**Backup Preferences**")
            auto_backup = st.checkbox("Automatic daily backup", value=True)
            backup_frequency = st.selectbox(
                "Backup Frequency",
                ["Daily", "Weekly", "Monthly"],
                index=0
            )
        
        with col2:
            st.markdown("**Data Actions**")
            
            # Export options
            if st.button("📤 Export All Data", use_container_width=True):
                with st.spinner("Preparing data export..."):
                    import time
                    time.sleep(2)
                    st.success("✅ Data export ready for download!")
            
            # Backup actions
            if st.button("💾 Create Manual Backup", use_container_width=True):
                with st.spinner("Creating backup..."):
                    import time
                    time.sleep(2)
                    st.success("✅ Backup created successfully!")
            
            # Data cleanup
            st.markdown("**Data Cleanup**")
            if st.button("🧹 Clean Temporary Files", use_container_width=True):
                st.success("✅ Temporary files cleaned (150 MB freed)")
            
            if st.button("🗑️ Delete Old Sessions", use_container_width=True):
                st.warning("⚠️ This will delete sessions older than your retention period")
            
            # Dangerous actions
            st.markdown("**⚠️ Dangerous Actions**")
            
            with st.expander("🗑️ Delete All Data"):
                st.error("**Warning**: This action cannot be undone!")
                confirm_text = st.text_input("Type 'DELETE ALL DATA' to confirm:")
                
                if confirm_text == "DELETE ALL DATA":
                    if st.button("🗑️ Permanently Delete All Data"):
                        st.error("Data deletion would be executed here")
            
            with st.expander("🔄 Reset Character Analysis"):
                st.warning("This will reset your character analysis and start fresh")
                if st.button("🔄 Reset Analysis"):
                    st.info("Character analysis reset - new sessions will rebuild your profile")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; padding: 1rem;">
        <p><strong>CarIActerology Settings</strong></p>
        <p>All settings are automatically saved. Changes take effect immediately.</p>
        <p>For support, contact: <a href="mailto:support@cariacterology.ai">support@cariacterology.ai</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()