"""
Settings Page
User preferences, privacy controls, and account management
"""

import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Paramètres - CarIActérologie",
    page_icon="⚙️",
    layout="wide"
)

def main():
    """Main settings interface"""
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px; margin-bottom: 2rem; color: white; text-align: center;">
        <h1>⚙️ Paramètres et Préférences</h1>
        <p>Gérez votre compte, confidentialité et préférences d'application</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Settings tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["👤 Profil", "🔒 Confidentialité", "🎨 Interface", "🔔 Notifications", "💾 Données"])
    
    with tab1:
        st.markdown("### 👤 Profil Utilisateur")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Informations Personnelles**")
            
            name = st.text_input("Nom Complet", value="Dr. Sarah Johnson")
            email = st.text_input("Adresse Email", value="sarah.johnson@example.com")
            
            # Age range for psychological context
            age_range = st.selectbox(
                "Tranche d'Âge",
                ["18-25", "26-35", "36-45", "46-55", "56-65", "65+"],
                index=2
            )
            
            # Professional context
            profession = st.selectbox(
                "Profession",
                ["Santé", "Éducation", "Technologie", "Affaires", "Arts et Créatif", "Autre"],
                index=1
            )
            
            # Goals for using the platform
            st.markdown("**Objectifs de Découverte de Soi**")
            goals = st.multiselect(
                "Que espérez-vous accomplir ?",
                [
                    "Mieux comprendre ma personnalité",
                    "Améliorer les relations", 
                    "Guidance de carrière",
                    "Croissance personnelle",
                    "Intelligence émotionnelle",
                    "Gestion du stress",
                    "Prise de décision",
                    "Compétences de communication"
                ],
                default=["Mieux comprendre ma personnalité", "Croissance personnelle"]
            )
        
        with col2:
            st.markdown("**Résumé du Profil**")
            
            # Profile picture placeholder
            st.image("https://via.placeholder.com/150x150/667eea/white?text=SJ", width=150)
            
            if st.button("Changer la Photo", key="change_picture_btn"):
                st.info("Fonctionnalité de téléchargement de photo bientôt disponible !")
            
            st.markdown("**Informations du Compte**")
            st.info(f"**Membre depuis** : 1er janvier 2024")
            st.info(f"**Sessions totales** : 28")
            st.info(f"**Confiance de caractère** : 85%")
            st.info(f"**Type de caractère principal** : Sanguin")
            
            st.markdown("**Plan d'Abonnement**")
            st.success("✅ **Plan Premium** - Toutes les fonctionnalités débloquées")
            
            if st.button("Gérer l'Abonnement", key="manage_subscription_btn"):
                st.info("Redirection vers la gestion de l'abonnement...")
        
        # Save profile changes
        if st.button("💾 Sauvegarder les Modifications du Profil", use_container_width=True, key="save_profile_btn"):
            st.success("Profil mis à jour avec succès !")
    
    with tab2:
        st.markdown("### 🔒 Confidentialité et Sécurité")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Contrôles de Confidentialité des Données**")
            
            # Privacy settings
            data_retention = st.selectbox(
                "Période de Rétention des Données",
                ["1 an", "2 ans", "5 ans", "Indéfinie"],
                index=1
            )
            
            allow_analytics = st.checkbox("Autoriser les analyses d'utilisation anonymisées", value=True)
            allow_research = st.checkbox("Contribuer aux données de recherche psychologique", value=False)
            allow_sharing = st.checkbox("Autoriser le partage d'insights avec les prestataires de soins", value=False)
            
            st.markdown("**Gestion de la Mémoire**")
            auto_forget = st.checkbox("Oubli automatique des conversations sensibles", value=True)
            memory_encryption = st.checkbox("Chiffrer les mémoires stockées", value=True)
            
            # Memory categories to store
            st.markdown("**Quoi Retenir**")
            remember_categories = st.multiselect(
                "Catégories à stocker en mémoire à long terme",
                [
                    "Insights de personnalité",
                    "Analyse de caractère",
                    "Patterns émotionnels", 
                    "Tendances comportementales",
                    "Préférences personnelles",
                    "Objectifs et aspirations",
                    "Dynamiques relationnelles",
                    "Insights professionnels"
                ],
                default=["Insights de personnalité", "Analyse de caractère", "Patterns émotionnels"]
            )
        
        with col2:
            st.markdown("**Paramètres de Sécurité**")
            
            # Password change
            if st.button("🔐 Changer le Mot de Passe", key="change_password_btn"):
                st.info("Le formulaire de changement de mot de passe apparaîtrait ici")
            
            # Two-factor authentication
            two_factor = st.checkbox("Activer l'Authentification à Deux Facteurs", value=False)
            if two_factor:
                st.info("📱 La configuration de l'authentification à deux facteurs commencerait ici")
            
            # Session security
            st.markdown("**Sécurité de Session**")
            auto_logout = st.selectbox(
                "Déconnexion automatique après inactivité",
                ["15 minutes", "30 minutes", "1 heure", "2 heures", "Jamais"],
                index=2
            )
            
            # Privacy summary
            st.markdown("**Résumé de Confidentialité**")
            st.info("🔒 Vos conversations sont chiffrées")
            st.info("🛡️ Aucune donnée vendue à des tiers")
            st.info("🏥 Stockage conforme HIPAA")
            st.info("🌍 Conforme au RGPD")
            
            if st.button("📋 Télécharger le Rapport de Confidentialité", key="download_privacy_btn"):
                st.success("Rapport de confidentialité généré et téléchargé !")
        
        # Privacy actions
        col3, col4 = st.columns(2)
        with col3:
            if st.button("🗑️ Supprimer des Données Spécifiques", use_container_width=True, key="delete_specific_btn"):
                st.warning("L'interface de suppression de données apparaîtrait ici")
        
        with col4:
            if st.button("📤 Exporter Toutes les Données", use_container_width=True, key="export_data_privacy_btn"):
                st.success("Exportation des données initiée !")
    
    with tab3:
        st.markdown("### 🎨 Interface et Expérience")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Préférences Visuelles**")
            
            # Theme selection
            theme = st.selectbox(
                "Thème de l'Application",
                ["Clair", "Sombre", "Automatique (Système)", "Bleu Thérapeutique"],
                index=3
            )
            
            # Color scheme
            primary_color = st.color_picker("Couleur d'Accent Principal", "#667eea")
            
            # Font preferences
            font_size = st.selectbox(
                "Taille de Police",
                ["Petite", "Moyenne", "Grande", "Très Grande"],
                index=1
            )
            
            # Layout preferences
            sidebar_default = st.selectbox(
                "État par Défaut de la Barre Latérale",
                ["Étendue", "Réduite", "Automatique"],
                index=0
            )
            
            st.markdown("**Disposition du Tableau de Bord**")
            dashboard_cards = st.multiselect(
                "Afficher sur le tableau de bord",
                [
                    "Métriques de session",
                    "Confiance de caractère", 
                    "Insights récents",
                    "Suivi d'humeur",
                    "Chronologie des progrès",
                    "Actions rapides",
                    "Badges de réussite"
                ],
                default=["Métriques de session", "Confiance de caractère", "Insights récents"]
            )
        
        with col2:
            st.markdown("**Préférences d'Interaction**")
            
            # Chat settings
            typing_speed = st.slider("Vitesse de Réponse de l'IA", min_value=1, max_value=5, value=3)
            show_timestamps = st.checkbox("Afficher les horodatages des messages", value=True)
            markdown_rendering = st.checkbox("Activer le formatage de texte riche", value=True)
            
            # Analysis preferences
            st.markdown("**Affichage de l'Analyse**")
            show_confidence = st.checkbox("Afficher les scores de confiance", value=True)
            animated_charts = st.checkbox("Visualisations animées", value=True)
            detailed_explanations = st.checkbox("Afficher les explications détaillées des traits", value=True)
            
            # Accessibility
            st.markdown("**Accessibilité**")
            high_contrast = st.checkbox("Mode à contraste élevé", value=False)
            screen_reader = st.checkbox("Optimisations pour lecteur d'écran", value=False)
            keyboard_nav = st.checkbox("Navigation clavier améliorée", value=False)
            
            # Preview
            st.markdown("**Aperçu du Thème**")
            if theme == "Bleu Thérapeutique":
                st.markdown("""
                <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 8px; text-align: center;">
                    <h4>Thème Bleu Thérapeutique</h4>
                    <p>Couleurs apaisantes conçues pour le bien-être psychologique</p>
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("🎨 Appliquer les Changements d'Interface", use_container_width=True, key="apply_interface_btn"):
            st.success("Préférences d'interface mises à jour !")
    
    with tab4:
        st.markdown("### 🔔 Notifications et Rappels")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Rappels de Session**")
            
            session_reminders = st.checkbox("Activer les rappels de session", value=True)
            
            if session_reminders:
                reminder_frequency = st.selectbox(
                    "Fréquence des Rappels",
                    ["Quotidien", "Tous les 2 jours", "Hebdomadaire", "Personnalisé"],
                    index=2
                )
                
                reminder_time = st.time_input("Heure de rappel préférée", value=datetime.strptime("19:00", "%H:%M").time())
            
            st.markdown("**Notifications de Progrès**")
            milestone_notifications = st.checkbox("Notifications de jalons de caractère", value=True)
            insight_notifications = st.checkbox("Notifications de nouveaux insights", value=True)
            weekly_summary = st.checkbox("Résumé hebdomadaire des progrès", value=True)
            
            st.markdown("**Notifications Système**")
            maintenance_notifications = st.checkbox("Notifications de maintenance", value=True)
            feature_updates = st.checkbox("Annonces de nouvelles fonctionnalités", value=True)
            security_alerts = st.checkbox("Alertes de sécurité", value=True)
        
        with col2:
            st.markdown("**Préférences de Livraison**")
            
            # Notification channels
            notification_channels = st.multiselect(
                "Canaux de Notification",
                ["Email", "Dans l'application", "Notifications push", "SMS"],
                default=["Email", "Dans l'application"]
            )
            
            # Email preferences
            st.markdown("**Notifications Email**")
            email_frequency = st.selectbox(
                "Fréquence des Emails",
                ["Immédiat", "Résumé quotidien", "Résumé hebdomadaire", "Jamais"],
                index=1
            )
            
            # Content preferences
            st.markdown("**Préférences de Contenu**")
            include_tips = st.checkbox("Inclure des conseils psychologiques", value=True)
            include_quotes = st.checkbox("Inclure des citations inspirantes", value=True)
            include_articles = st.checkbox("Inclure des articles connexes", value=False)
            
            # Quiet hours
            st.markdown("**Heures de Silence**")
            enable_quiet_hours = st.checkbox("Activer les heures de silence", value=True)
            
            if enable_quiet_hours:
                col_quiet1, col_quiet2 = st.columns(2)
                with col_quiet1:
                    quiet_start = st.time_input("De", value=datetime.strptime("22:00", "%H:%M").time())
                with col_quiet2:
                    quiet_end = st.time_input("À", value=datetime.strptime("08:00", "%H:%M").time())
        
        if st.button("🔔 Sauvegarder les Paramètres de Notification", use_container_width=True, key="save_notifications_btn"):
            st.success("Préférences de notification mises à jour !")
    
    with tab5:
        st.markdown("### 💾 Gestion des Données")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Aperçu des Données**")
            
            # Storage usage
            st.metric("Stockage Utilisé", "2.4 GB", "sur 10 GB")
            
            # Data breakdown
            data_breakdown = {
                "Historique de Conversation": "1.2 GB",
                "Données d'Analyse": "800 MB", 
                "Rapports Générés": "350 MB",
                "Préférences Utilisateur": "50 MB"
            }
            
            for category, size in data_breakdown.items():
                st.markdown(f"**{category}**: {size}")
            
            st.markdown("**Santé des Données**")
            st.success("✅ Toutes les données sauvegardées")
            st.success("✅ Aucune corruption détectée")
            st.success("✅ Chiffrement actif")
            
            # Backup settings
            st.markdown("**Préférences de Sauvegarde**")
            auto_backup = st.checkbox("Sauvegarde quotidienne automatique", value=True)
            backup_frequency = st.selectbox(
                "Fréquence de Sauvegarde",
                ["Quotidienne", "Hebdomadaire", "Mensuelle"],
                index=0
            )
        
        with col2:
            st.markdown("**Actions sur les Données**")
            
            # Export options
            if st.button("📤 Exporter Toutes les Données", use_container_width=True, key="export_data_backup_btn"):
                with st.spinner("Préparation de l'exportation des données..."):
                    import time
                    time.sleep(2)
                    st.success("✅ Exportation des données prête pour le téléchargement !")
            
            # Backup actions
            if st.button("💾 Créer une Sauvegarde Manuelle", use_container_width=True, key="manual_backup_btn"):
                with st.spinner("Création de la sauvegarde..."):
                    import time
                    time.sleep(2)
                    st.success("✅ Sauvegarde créée avec succès !")
            
            # Data cleanup
            st.markdown("**Nettoyage des Données**")
            if st.button("🧹 Nettoyer les Fichiers Temporaires", use_container_width=True, key="clean_temp_btn"):
                st.success("✅ Fichiers temporaires nettoyés (150 MB libérés)")
            
            if st.button("🗑️ Supprimer les Anciennes Sessions", use_container_width=True, key="delete_old_sessions_btn"):
                st.warning("⚠️ Ceci supprimera les sessions plus anciennes que votre période de rétention")
            
            # Dangerous actions
            st.markdown("**⚠️ Actions Dangereuses**")
            
            with st.expander("🗑️ Supprimer Toutes les Données"):
                st.error("**Attention** : Cette action ne peut pas être annulée !")
                confirm_text = st.text_input("Tapez 'SUPPRIMER TOUTES LES DONNEES' pour confirmer :")
                
                if confirm_text == "SUPPRIMER TOUTES LES DONNEES":
                    if st.button("🗑️ Supprimer Définitivement Toutes les Données", key="delete_all_data_btn"):
                        st.error("La suppression des données serait exécutée ici")
            
            with st.expander("🔄 Réinitialiser l'Analyse de Caractère"):
                st.warning("Ceci réinitialisera votre analyse de caractère et repartira à zéro")
                if st.button("🔄 Réinitialiser l'Analyse", key="reset_analysis_btn"):
                    st.info("Analyse de caractère réinitialisée - les nouvelles sessions reconstruiront votre profil")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; padding: 1rem;">
        <p><strong>Paramètres CarIActérologie</strong></p>
        <p>Tous les paramètres sont automatiquement sauvegardés. Les changements prennent effet immédiatement.</p>
        <p>Pour le support, contactez : <a href="mailto:support@cariacterology.ai">support@cariacterology.ai</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()