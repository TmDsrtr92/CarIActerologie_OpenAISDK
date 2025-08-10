"""
PDF Report Generation Module for CarIActerology
Professional psychological reports using ReportLab - Clean Version
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import io
import sys
import os

# Add the project root to Python path for data imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.mock_data import (
    get_mock_user_profile, get_primary_character_type,
    get_mock_session_history, get_mock_insights_gallery,
    get_mock_progress_metrics, get_mock_recommendations
)

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
        ]))
        
        story.append(user_table)
        story.append(Spacer(1, 30))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        story.append(Paragraph(
            f"This comprehensive psychological analysis reveals a {character_type['name']} character profile "
            f"with a confidence level of {user_profile['confidence_score']*100:.1f}%. Through {user_profile['analysis_sessions']} "
            f"analytical sessions and {user_profile['total_interactions']} interactions, we have identified key "
            f"personality traits, behavioral patterns, and areas for personal development.",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 20))
        
        # Character Type Analysis
        story.append(Paragraph("Character Type Analysis", self.styles['SectionHeader']))
        story.append(Paragraph(f"Primary Type: {character_type['name']}", self.styles['SubsectionHeader']))
        story.append(Paragraph(character_type['description'], self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Strengths and Challenges
        story.append(Paragraph("Strengths and Growth Areas", self.styles['SectionHeader']))
        
        # Strengths
        story.append(Paragraph("Key Strengths:", self.styles['SubsectionHeader']))
        for strength in character_type['strengths']:
            story.append(Paragraph(f"• {strength}", self.styles['Normal']))
        story.append(Spacer(1, 10))
        
        # Challenges
        story.append(Paragraph("Growth Areas:", self.styles['SubsectionHeader']))
        for challenge in character_type['challenges']:
            story.append(Paragraph(f"• {challenge}", self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Key Insights Section
        story.append(Paragraph("Key Psychological Insights", self.styles['SectionHeader']))
        
        # Group insights by category
        insight_categories = {}
        for insight in insights[:8]:  # Limit to top 8 insights
            category = insight['category']
            if category not in insight_categories:
                insight_categories[category] = []
            insight_categories[category].append(insight)
        
        for category, category_insights in insight_categories.items():
            story.append(Paragraph(category, self.styles['SubsectionHeader']))
            for insight in category_insights[:2]:  # Max 2 per category
                story.append(Paragraph(f"• {insight['text']}", self.styles['Normal']))
            story.append(Spacer(1, 10))
        
        story.append(Spacer(1, 20))
        
        # Personalized Recommendations
        story.append(Paragraph("Personalized Recommendations", self.styles['SectionHeader']))
        
        for i, rec in enumerate(recommendations[:3], 1):  # Top 3 recommendations
            story.append(Paragraph(f"{i}. {rec['title']}", self.styles['SubsectionHeader']))
            story.append(Paragraph(rec['description'], self.styles['Normal']))
            story.append(Paragraph(f"Category: {rec['category']} | Priority: {rec['priority'].title()}", self.styles['Normal']))
            story.append(Spacer(1, 15))
        
        # Conclusion
        story.append(Paragraph("Conclusion and Next Steps", self.styles['SectionHeader']))
        story.append(Paragraph(
            f"This analysis represents {user_profile['analysis_sessions']} sessions of deep psychological exploration "
            f"using René Le Senne's proven characterology framework. Your {character_type['name']} profile shows "
            f"significant potential for continued growth, particularly in the areas identified above. "
            f"Regular engagement with the recommended practices will support your ongoing personal development journey.",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph(
            "Recommended Follow-up: Continue regular analysis sessions, implement personalized recommendations, "
            "and monitor progress through periodic assessments. The insights gained through this process will deepen "
            "with consistent application and self-reflection.",
            self.styles['Normal']
        ))
        
        # Build PDF
        doc.build(story, onFirstPage=self.create_header_footer, onLaterPages=self.create_header_footer)
        
        # Return buffer
        buffer.seek(0)
        return buffer
    
    def generate_session_summary_report(self, session_count: int = 5) -> io.BytesIO:
        """Generate a focused session summary report"""
        
        sessions = get_mock_session_history(30)[:session_count]
        insights = get_mock_insights_gallery()[:6]
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        
        # Title
        story.append(Paragraph("Session Summary Report", self.styles['ReportTitle']))
        story.append(Spacer(1, 30))
        
        # Session overview
        story.append(Paragraph("Recent Session Overview", self.styles['SectionHeader']))
        
        total_duration = sum(s['duration_minutes'] for s in sessions)
        total_insights = sum(s['insights_discovered'] for s in sessions)
        avg_satisfaction = sum(s['satisfaction_score'] for s in sessions) / len(sessions)
        
        story.append(Paragraph(f"Sessions Analyzed: {len(sessions)}", self.styles['Normal']))
        story.append(Paragraph(f"Total Time: {total_duration} minutes ({total_duration/60:.1f} hours)", self.styles['Normal']))
        story.append(Paragraph(f"Insights Discovered: {total_insights}", self.styles['Normal']))
        story.append(Paragraph(f"Average Satisfaction: {avg_satisfaction:.1f}/10", self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Key insights
        story.append(Paragraph("Key Insights from Recent Sessions", self.styles['SectionHeader']))
        
        for insight in insights:
            story.append(Paragraph(f"• {insight['text']}", self.styles['Normal']))
        
        doc.build(story, onFirstPage=self.create_header_footer, onLaterPages=self.create_header_footer)
        buffer.seek(0)
        return buffer
    
    def generate_progress_report(self) -> io.BytesIO:
        """Generate a progress-focused report"""
        
        progress = get_mock_progress_metrics()
        user_profile = get_mock_user_profile()
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        
        # Title
        story.append(Paragraph("Personal Development Progress Report", self.styles['ReportTitle']))
        story.append(Spacer(1, 30))
        
        # Progress overview
        story.append(Paragraph("Development Progress Overview", self.styles['SectionHeader']))
        
        # Milestones achieved
        story.append(Paragraph("Recent Milestones", self.styles['SubsectionHeader']))
        for milestone in progress['milestone_achievements']:
            story.append(Paragraph(
                f"{milestone['milestone']} - {milestone['achieved_date'].strftime('%B %Y')}",
                self.styles['Normal']
            ))
            story.append(Paragraph(milestone['description'], self.styles['Normal']))
            story.append(Spacer(1, 8))
        
        doc.build(story, onFirstPage=self.create_header_footer, onLaterPages=self.create_header_footer)
        buffer.seek(0)
        return buffer

# Utility functions
def generate_report(report_type: str) -> io.BytesIO:
    """Generate specified report type"""
    generator = ReportGenerator()
    
    if report_type == "complete_analysis":
        return generator.generate_complete_analysis_report()
    elif report_type == "session_summary":
        return generator.generate_session_summary_report()
    elif report_type == "progress_report":
        return generator.generate_progress_report()
    else:
        raise ValueError(f"Unknown report type: {report_type}")

def get_available_report_types() -> dict:
    """Get list of available report types with descriptions"""
    return {
        "complete_analysis": {
            "name": "Complete Psychological Analysis",
            "description": "Comprehensive character analysis with traits, insights, and recommendations",
            "pages": "8-12 pages",
            "includes": ["Character type analysis", "Trait visualization", "Key insights", "Personalized recommendations", "Progress metrics"]
        },
        "session_summary": {
            "name": "Session Summary Report",
            "description": "Focused summary of recent therapy sessions and discoveries",
            "pages": "3-5 pages",
            "includes": ["Session overview", "Key insights", "Progress highlights", "Next steps"]
        },
        "progress_report": {
            "name": "Personal Development Progress",
            "description": "Progress tracking with milestones and development goals",
            "pages": "4-6 pages",
            "includes": ["Achievement milestones", "Growth metrics", "Development areas", "Goal tracking"]
        }
    }