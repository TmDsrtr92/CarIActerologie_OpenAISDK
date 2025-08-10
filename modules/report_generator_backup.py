"""
PDF Report Generation Module for CarIActerology
Professional psychological reports using ReportLab
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image, Flowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import io
import base64
import sys
import os

# Add the project root to Python path for data imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.mock_data import (
    get_mock_user_profile, get_primary_character_type,
    get_mock_session_history, get_mock_insights_gallery,
    get_mock_progress_metrics, get_mock_recommendations,
    get_mock_therapeutic_themes
)

class CharacterRadarChart(Flowable):
    """Custom flowable for character radar chart in PDF"""
    
    def __init__(self, traits_data, width=400, height=300):
        Flowable.__init__(self)
        self.traits_data = traits_data
        self.width = width
        self.height = height
    
    def draw(self):
        # Simple representation - in production, would use reportlab graphics
        # For now, create a placeholder
        self.canv.setFont("Helvetica-Bold", 12)
        self.canv.drawString(50, 150, "Character Trait Visualization")
        self.canv.setFont("Helvetica", 10)
        
        y_pos = 120
        for trait, value in self.traits_data.items():
            self.canv.drawString(50, y_pos, f"{trait}: {value:.1f}/10")
            y_pos -= 20

class ReportGenerator:
    """Professional PDF report generator for psychological analysis"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Define custom paragraph styles for professional reports"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#667eea'),
            alignment=TA_CENTER
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#4a5568'),
            leftIndent=0
        ))
        
        # Subsection style
        self.styles.add(ParagraphStyle(
            name='SubsectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=15,
            textColor=colors.HexColor('#2d3748')
        ))
        
        # Insight style
        self.styles.add(ParagraphStyle(
            name='InsightText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            leftIndent=20,
            textColor=colors.HexColor('#2d3748'),
            alignment=TA_JUSTIFY
        ))
        
        # Recommendation style
        self.styles.add(ParagraphStyle(
            name='RecommendationText',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            leftIndent=15,
            textColor=colors.HexColor('#4a5568')
        ))
    
    def create_header_footer(self, canvas, doc):
        """Add header and footer to each page"""
        canvas.saveState()
        
        # Header
        canvas.setFont('Helvetica-Bold', 10)
        canvas.setFillColor(colors.HexColor('#667eea'))
        canvas.drawString(50, letter[1] - 50, "CarIActerology - Psychological Analysis Report")
        canvas.drawString(letter[0] - 200, letter[1] - 50, f"Generated: {datetime.now().strftime('%B %d, %Y')}")
        
        # Footer
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        canvas.drawString(50, 50, "Confidential - For Personal Development Use Only")
        canvas.drawString(letter[0] - 100, 50, f"Page {canvas.getPageNumber()}")
        
        canvas.restoreState()
    
    def generate_complete_analysis_report(self) -> io.BytesIO:
        """Generate a comprehensive psychological analysis report"""
        
        # Get data
        user_profile = get_mock_user_profile()
        character_type = get_primary_character_type()
        sessions = get_mock_session_history(30)
        insights = get_mock_insights_gallery()
        progress = get_mock_progress_metrics()
        recommendations = get_mock_recommendations()
        themes = get_mock_therapeutic_themes()
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=letter,
            rightMargin=72, leftMargin=72,
            topMargin=100, bottomMargin=72
        )
        
        # Build story (content)
        story = []
        
        # Title Page
        story.append(Paragraph("Psychological Character Analysis", self.styles['ReportTitle']))
        story.append(Spacer(1, 30))
        story.append(Paragraph("Based on René Le Senne's Characterology Framework", self.styles['Normal']))
        story.append(Spacer(1, 40))
        
        # User information table
        user_info_data = [
            ['Report Date:', datetime.now().strftime('%B %d, %Y')],
            ['Analysis Period:', f"{user_profile['member_since'].strftime('%B %Y')} - Present"],
            ['Total Sessions:', str(user_profile['analysis_sessions'])],
            ['Character Type:', character_type['name']],
            ['Confidence Score:', f"{user_profile['confidence_score']*100:.1f}%"],
            ['Growth Status:', user_profile['growth_trajectory'].title()]
        ]
        
        user_table = Table(user_info_data, colWidths=[2*inch, 3*inch])
        user_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f7fafc')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))\n        \n        story.append(user_table)\n        story.append(PageBreak())\n        \n        # Executive Summary\n        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))\n        story.append(Paragraph(\n            f"This comprehensive psychological analysis reveals a {character_type['name']} character profile "\n            f"with a confidence level of {user_profile['confidence_score']*100:.1f}%. Through {user_profile['analysis_sessions']} "\n            f"analytical sessions and {user_profile['total_interactions']} interactions, we have identified key "\n            f"personality traits, behavioral patterns, and areas for personal development.",\n            self.styles['Normal']\n        ))\n        story.append(Spacer(1, 20))\n        \n        # Character Type Analysis\n        story.append(Paragraph("Character Type Analysis", self.styles['SectionHeader']))\n        story.append(Paragraph(f"Primary Type: {character_type['name']}", self.styles['SubsectionHeader']))\n        story.append(Paragraph(character_type['description'], self.styles['Normal']))\n        story.append(Spacer(1, 15))\n        \n        # Traits visualization (placeholder)\n        traits_chart = CharacterRadarChart(character_type['traits'])\n        story.append(traits_chart)\n        story.append(Spacer(1, 20))\n        \n        # Strengths and Challenges\n        story.append(Paragraph("Strengths and Growth Areas", self.styles['SectionHeader']))\n        \n        # Strengths table\n        strengths_data = [['Key Strengths', 'Description']]\n        for i, strength in enumerate(character_type['strengths']):\n            strengths_data.append([strength, f"Natural ability that supports personal and professional growth."])\n        \n        strengths_table = Table(strengths_data, colWidths=[2*inch, 4*inch])\n        strengths_table.setStyle(TableStyle([\n            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#48bb78')),\n            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),\n            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),\n            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),\n            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),\n            ('FONTSIZE', (0, 0), (-1, -1), 10),\n            ('GRID', (0, 0), (-1, -1), 1, colors.grey),\n            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')])\n        ]))\n        \n        story.append(strengths_table)\n        story.append(Spacer(1, 15))\n        \n        # Challenges table\n        challenges_data = [['Growth Areas', 'Development Opportunity']]\n        for challenge in character_type['challenges']:\n            challenges_data.append([challenge, f"Area for conscious development and skill building."])\n        \n        challenges_table = Table(challenges_data, colWidths=[2*inch, 4*inch])\n        challenges_table.setStyle(TableStyle([\n            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ed8936')),\n            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),\n            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),\n            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),\n            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),\n            ('FONTSIZE', (0, 0), (-1, -1), 10),\n            ('GRID', (0, 0), (-1, -1), 1, colors.grey),\n            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fffaf0')])\n        ]))\n        \n        story.append(challenges_table)\n        story.append(PageBreak())\n        \n        # Key Insights Section\n        story.append(Paragraph("Key Psychological Insights", self.styles['SectionHeader']))\n        \n        # Group insights by category\n        insight_categories = {}\n        for insight in insights[:12]:  # Limit to top 12 insights\n            category = insight['category']\n            if category not in insight_categories:\n                insight_categories[category] = []\n            insight_categories[category].append(insight)\n        \n        for category, category_insights in insight_categories.items():\n            story.append(Paragraph(category, self.styles['SubsectionHeader']))\n            for insight in category_insights:\n                story.append(Paragraph(\n                    f"• {insight['text']}\", self.styles['InsightText']\n                ))\n                story.append(Paragraph(\n                    f\"<i>Confidence: {insight['confidence']*100:.0f}% | Discovered: {insight['discovered_date'].strftime('%B %Y')}</i>\",\n                    self.styles['RecommendationText']\n                ))\n                story.append(Spacer(1, 8))\n        \n        story.append(PageBreak())\n        \n        # Progress Analysis\n        story.append(Paragraph("Progress and Development Analysis", self.styles['SectionHeader']))\n        \n        overall_progress = progress['overall_progress']\n        progress_data = [['Development Area', 'Current Level', 'Progress Indicator']]\n        \n        for area, score in overall_progress.items():\n            area_name = area.replace('_', ' ').title()\n            level_desc = \"Excellent\" if score >= 8.5 else \"Good\" if score >= 7.0 else \"Developing\" if score >= 5.5 else \"Needs Focus\"\n            progress_data.append([area_name, f\"{score:.1f}/10\", level_desc])\n        \n        progress_table = Table(progress_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])\n        progress_table.setStyle(TableStyle([\n            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4299e1')),\n            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),\n            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),\n            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),\n            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),\n            ('FONTSIZE', (0, 0), (-1, -1), 10),\n            ('GRID', (0, 0), (-1, -1), 1, colors.grey),\n            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ebf8ff')])\n        ]))\n        \n        story.append(progress_table)\n        story.append(Spacer(1, 20))\n        \n        # Therapeutic Recommendations\n        story.append(Paragraph("Personalized Recommendations", self.styles['SectionHeader']))\n        \n        for i, rec in enumerate(recommendations[:4], 1):  # Top 4 recommendations\n            story.append(Paragraph(f\"{i}. {rec['title']}\", self.styles['SubsectionHeader']))\n            story.append(Paragraph(rec['description'], self.styles['Normal']))\n            story.append(Paragraph(f\"<b>Category:</b> {rec['category']}\", self.styles['RecommendationText']))\n            story.append(Paragraph(f\"<b>Time Commitment:</b> {rec['time_commitment']}\", self.styles['RecommendationText']))\n            story.append(Paragraph(f\"<b>Priority:</b> {rec['priority'].title()}\", self.styles['RecommendationText']))\n            story.append(Paragraph(f\"<b>Personalized Note:</b> {rec['personalised_note']}\", self.styles['InsightText']))\n            story.append(Spacer(1, 15))\n        \n        story.append(PageBreak())\n        \n        # Session Summary\n        story.append(Paragraph(\"Recent Session Analysis\", self.styles['SectionHeader']))\n        \n        recent_sessions = sessions[:5]  # Last 5 sessions\n        session_data = [['Date', 'Duration', 'Focus Areas', 'Insights', 'Satisfaction']]\n        \n        for session in recent_sessions:\n            focus_areas = ', '.join(session['key_topics'][:2])  # First 2 topics\n            session_data.append([\n                session['date'].strftime('%m/%d/%Y'),\n                f\"{session['duration_minutes']} min\",\n                focus_areas,\n                str(session['insights_discovered']),\n                f\"{session['satisfaction_score']}/10\"\n            ])\n        \n        session_table = Table(session_data, colWidths=[1*inch, 0.8*inch, 2.2*inch, 0.8*inch, 1*inch])\n        session_table.setStyle(TableStyle([\n            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9f7aea')),\n            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),\n            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),\n            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),\n            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),\n            ('FONTSIZE', (0, 0), (-1, -1), 9),\n            ('GRID', (0, 0), (-1, -1), 1, colors.grey),\n            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#faf5ff')])\n        ]))\n        \n        story.append(session_table)\n        story.append(Spacer(1, 20))\n        \n        # Conclusion\n        story.append(Paragraph(\"Conclusion and Next Steps\", self.styles['SectionHeader']))\n        story.append(Paragraph(\n            f\"This analysis represents {user_profile['analysis_sessions']} sessions of deep psychological exploration \"\n            f\"using René Le Senne's proven characterology framework. Your {character_type['name']} profile shows \"\n            f\"significant potential for continued growth, particularly in the areas identified above. \"\n            f\"Regular engagement with the recommended practices will support your ongoing personal development journey.\",\n            self.styles['Normal']\n        ))\n        story.append(Spacer(1, 15))\n        \n        story.append(Paragraph(\n            \"<b>Recommended Follow-up:</b> Continue regular analysis sessions, implement personalized recommendations, \"\n            \"and monitor progress through periodic assessments. The insights gained through this process will deepen \"\n            \"with consistent application and self-reflection.\",\n            self.styles['InsightText']\n        ))\n        \n        # Build PDF\n        doc.build(story, onFirstPage=self.create_header_footer, onLaterPages=self.create_header_footer)\n        \n        # Return buffer\n        buffer.seek(0)\n        return buffer\n    \n    def generate_session_summary_report(self, session_count: int = 5) -> io.BytesIO:\n        \"\"\"Generate a focused session summary report\"\"\"\n        \n        sessions = get_mock_session_history(30)[:session_count]\n        insights = get_mock_insights_gallery()[:8]\n        \n        buffer = io.BytesIO()\n        doc = SimpleDocTemplate(buffer, pagesize=letter)\n        story = []\n        \n        # Title\n        story.append(Paragraph(\"Session Summary Report\", self.styles['ReportTitle']))\n        story.append(Spacer(1, 30))\n        \n        # Session overview\n        story.append(Paragraph(\"Recent Session Overview\", self.styles['SectionHeader']))\n        \n        total_duration = sum(s['duration_minutes'] for s in sessions)\n        total_insights = sum(s['insights_discovered'] for s in sessions)\n        avg_satisfaction = sum(s['satisfaction_score'] for s in sessions) / len(sessions)\n        \n        overview_data = [\n            ['Sessions Analyzed:', str(len(sessions))],\n            ['Total Time:', f\"{total_duration} minutes ({total_duration/60:.1f} hours)\"],\n            ['Insights Discovered:', str(total_insights)],\n            ['Average Satisfaction:', f\"{avg_satisfaction:.1f}/10\"]\n        ]\n        \n        overview_table = Table(overview_data, colWidths=[2*inch, 2*inch])\n        overview_table.setStyle(TableStyle([\n            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e2e8f0')),\n            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),\n            ('GRID', (0, 0), (-1, -1), 1, colors.grey)\n        ]))\n        \n        story.append(overview_table)\n        story.append(Spacer(1, 20))\n        \n        # Key insights\n        story.append(Paragraph(\"Key Insights from Recent Sessions\", self.styles['SectionHeader']))\n        \n        for insight in insights:\n            story.append(Paragraph(f\"• {insight['text']}\", self.styles['InsightText']))\n        \n        doc.build(story, onFirstPage=self.create_header_footer, onLaterPages=self.create_header_footer)\n        buffer.seek(0)\n        return buffer\n    \n    def generate_progress_report(self) -> io.BytesIO:\n        \"\"\"Generate a progress-focused report\"\"\"\n        \n        progress = get_mock_progress_metrics()\n        user_profile = get_mock_user_profile()\n        \n        buffer = io.BytesIO()\n        doc = SimpleDocTemplate(buffer, pagesize=letter)\n        story = []\n        \n        # Title\n        story.append(Paragraph(\"Personal Development Progress Report\", self.styles['ReportTitle']))\n        story.append(Spacer(1, 30))\n        \n        # Progress overview\n        story.append(Paragraph(\"Development Progress Overview\", self.styles['SectionHeader']))\n        \n        # Milestones achieved\n        story.append(Paragraph(\"Recent Milestones\", self.styles['SubsectionHeader']))\n        for milestone in progress['milestone_achievements']:\n            story.append(Paragraph(\n                f\"<b>{milestone['milestone']}</b> - {milestone['achieved_date'].strftime('%B %Y')}\",\n                self.styles['Normal']\n            ))\n            story.append(Paragraph(milestone['description'], self.styles['RecommendationText']))\n            story.append(Spacer(1, 8))\n        \n        doc.build(story, onFirstPage=self.create_header_footer, onLaterPages=self.create_header_footer)\n        buffer.seek(0)\n        return buffer

# Utility functions
def generate_report(report_type: str) -> io.BytesIO:\n    \"\"\"Generate specified report type\"\"\"\n    generator = ReportGenerator()\n    \n    if report_type == \"complete_analysis\":\n        return generator.generate_complete_analysis_report()\n    elif report_type == \"session_summary\":\n        return generator.generate_session_summary_report()\n    elif report_type == \"progress_report\":\n        return generator.generate_progress_report()\n    else:\n        raise ValueError(f\"Unknown report type: {report_type}\")\n\ndef get_available_report_types() -> dict:\n    \"\"\"Get list of available report types with descriptions\"\"\"\n    return {\n        \"complete_analysis\": {\n            \"name\": \"Complete Psychological Analysis\",\n            \"description\": \"Comprehensive character analysis with traits, insights, and recommendations\",\n            \"pages\": \"8-12 pages\",\n            \"includes\": [\"Character type analysis\", \"Trait visualization\", \"Key insights\", \"Personalized recommendations\", \"Progress metrics\"]\n        },\n        \"session_summary\": {\n            \"name\": \"Session Summary Report\",\n            \"description\": \"Focused summary of recent therapy sessions and discoveries\",\n            \"pages\": \"3-5 pages\",\n            \"includes\": [\"Session overview\", \"Key insights\", \"Progress highlights\", \"Next steps\"]\n        },\n        \"progress_report\": {\n            \"name\": \"Personal Development Progress\",\n            \"description\": \"Progress tracking with milestones and development goals\",\n            \"pages\": \"4-6 pages\",\n            \"includes\": [\"Achievement milestones\", \"Growth metrics\", \"Development areas\", \"Goal tracking\"]\n        }\n    }