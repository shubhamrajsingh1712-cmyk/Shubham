"""
Comprehensive PDF Report Generator
Generates 20-25 page detailed psychometric assessment reports
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image as RLImage, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime
from typing import Dict, List, Any
import numpy as np

class ComprehensiveReportGenerator:
    """Generate detailed 20-25 page psychometric assessment reports"""
    
    def __init__(self):
        self.page_width, self.page_height = A4
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
        
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1A2B4B'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section heading
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#1A2B4B'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderColor=colors.HexColor('#5D7A68'),
            borderPadding=5
        ))
        
        # Subsection heading
        self.styles.add(ParagraphStyle(
            name='SubsectionHeading',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#1A2B4B'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='ReportBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#1A1A1A'),
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=16
        ))
        
        # Interpretation text
        self.styles.add(ParagraphStyle(
            name='Interpretation',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#2A2A2A'),
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            leading=15,
            leftIndent=15
        ))
        
        # Score label
        self.styles.add(ParagraphStyle(
            name='ScoreLabel',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#4A4A4A'),
            spaceAfter=6
        ))
        
        # Highlight box
        self.styles.add(ParagraphStyle(
            name='HighlightBox',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#1A2B4B'),
            backColor=colors.HexColor('#F0F4F8'),
            borderWidth=1,
            borderColor=colors.HexColor('#5D7A68'),
            borderPadding=10,
            spaceAfter=12
        ))
    
    def generate_report(self, user_data: Dict, test_results: List[Dict], report_id: str) -> str:
        """Generate complete PDF report"""
        filename = f"career_report_{report_id}.pdf"
        filepath = f"/tmp/{filename}"
        
        doc = SimpleDocTemplate(
            filepath, 
            pagesize=A4,
            rightMargin=50, 
            leftMargin=50,
            topMargin=50, 
            bottomMargin=50,
            title=f"Career Discovery Report - {user_data.get('full_name', 'Student')}"
        )
        
        story = []
        
        # Add all sections
        story.extend(self._create_cover_page(user_data, report_id))
        story.append(PageBreak())
        
        story.extend(self._create_executive_summary(user_data, test_results))
        story.append(PageBreak())
        
        # Detailed sections for each dimension
        for test_result in test_results:
            test_type = test_result.get('test_type')
            if test_type == 'orientation':
                story.extend(self._create_orientation_section(test_result))
                story.append(PageBreak())
            elif test_type == 'interest':
                story.extend(self._create_interest_section(test_result))
                story.append(PageBreak())
            elif test_type == 'personality':
                story.extend(self._create_personality_section(test_result))
                story.append(PageBreak())
            elif test_type == 'aptitude':
                story.extend(self._create_aptitude_section(test_result))
                story.append(PageBreak())
            elif test_type == 'eq':
                story.extend(self._create_eq_section(test_result))
                story.append(PageBreak())
        
        # Career recommendations
        story.extend(self._create_career_recommendations(test_results))
        story.append(PageBreak())
        
        # Strengths and development
        story.extend(self._create_strengths_development(test_results))
        story.append(PageBreak())
        
        # Career pathways
        story.extend(self._create_career_pathways(test_results))
        story.append(PageBreak())
        
        # Appendix and disclaimer
        story.extend(self._create_appendix())
        
        # Build PDF
        doc.build(story, onFirstPage=self._add_header_footer, onLaterPages=self._add_header_footer)
        
        return filepath
    
    def _add_header_footer(self, canvas_obj, doc):
        """Add header and footer to each page"""
        canvas_obj.saveState()
        
        # Header
        canvas_obj.setFont('Helvetica', 9)
        canvas_obj.setFillColor(colors.HexColor('#4A4A4A'))
        canvas_obj.drawString(50, A4[1] - 30, "BoatMyCareer.com - Career Discovery Report")
        
        # Footer
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.drawString(50, 30, "© 2024 BoatMyCareer.com")
        canvas_obj.drawRightString(A4[0] - 50, 30, f"Page {doc.page}")
        
        canvas_obj.restoreState()
    
    def _create_cover_page(self, user_data: Dict, report_id: str) -> List:
        """Create cover page"""
        elements = []
        
        # Logo placeholder
        elements.append(Spacer(1, 1*inch))
        
        # Title
        title = Paragraph("Career Discovery Report", self.styles['ReportTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))
        
        # Subtitle
        subtitle = Paragraph("Comprehensive Psychometric Assessment", self.styles['Heading2'])
        elements.append(subtitle)
        elements.append(Spacer(1, 0.5*inch))
        
        # Student info box
        info_data = [
            ["Student Name:", user_data.get('full_name', 'N/A')],
            ["Class:", user_data.get('class_level', 'N/A')],
            ["School:", user_data.get('school_name', 'N/A')],
            ["Report Date:", datetime.now().strftime('%B %d, %Y')],
            ["Report ID:", report_id[:12]]
        ]
        
        info_table = Table(info_data, colWidths=[2.5*inch, 3.5*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9F8F6')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#4A4A4A')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1A1A1A')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB'))
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 1*inch))
        
        # Report description
        desc = Paragraph(
            "This report presents a comprehensive analysis of your psychometric assessment, "
            "evaluating your work orientation, interests, personality traits, cognitive aptitudes, "
            "and emotional intelligence. Use this report to gain deep insights into your strengths, "
            "potential career paths, and development opportunities.",
            self.styles['ReportBody']
        )
        elements.append(desc)
        
        elements.append(Spacer(1, 0.5*inch))
        
        # Contact info
        contact = Paragraph(
            "<b>For Counselling:</b><br/>"
            "Shubham Raj Singh<br/>"
            "Call/WhatsApp: 6200488068<br/>"
            "Email: shubhamrajsingh1712@gmail.com",
            self.styles['Normal']
        )
        elements.append(contact)
        
        return elements
    
    def _create_executive_summary(self, user_data: Dict, test_results: List[Dict]) -> List:
        """Create 2-page executive summary"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Overall profile snapshot
        elements.append(Paragraph("Overall Profile Snapshot", self.styles['SubsectionHeading']))
        
        # Collect all scores
        all_scores = {}
        for result in test_results:
            test_type = result.get('test_type')
            scores = result.get('scores', {})
            scoring_details = result.get('scoring_details', {})
            all_scores[test_type] = {
                'scores': scores,
                'details': scoring_details
            }
        
        # Create radar chart for 5 main dimensions
        radar_img = self._create_radar_chart(all_scores)
        if radar_img:
            elements.append(radar_img)
            elements.append(Spacer(1, 0.2*inch))
        
        # Key strengths
        elements.append(Paragraph("Key Strengths", self.styles['SubsectionHeading']))
        strengths = self._identify_top_strengths(all_scores, top_n=5)
        for i, strength in enumerate(strengths, 1):
            elements.append(Paragraph(
                f"{i}. <b>{strength['trait'].replace('_', ' ').title()}</b> - "
                f"Score: {strength['score']}% ({strength['band']})",
                self.styles['ReportBody']
            ))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Development areas
        elements.append(Paragraph("Key Development Areas", self.styles['SubsectionHeading']))
        dev_areas = self._identify_development_areas(all_scores, top_n=3)
        for i, area in enumerate(dev_areas, 1):
            elements.append(Paragraph(
                f"{i}. <b>{area['trait'].replace('_', ' ').title()}</b> - "
                f"Score: {area['score']}% ({area['band']})",
                self.styles['ReportBody']
            ))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Quick career indicators
        elements.append(Paragraph("Quick Career Direction Indicators", self.styles['SubsectionHeading']))
        career_indicators = self._generate_quick_career_indicators(all_scores)
        for indicator in career_indicators:
            elements.append(Paragraph(f"• {indicator}", self.styles['ReportBody']))
        
        return elements
    
    def _create_orientation_section(self, test_result: Dict) -> List:
        """Create 3-4 page orientation analysis"""
        elements = []
        
        elements.append(Paragraph("Section 1: Work Orientation & Style Analysis", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        scores = test_result.get('scores', {})
        scoring_details = test_result.get('scoring_details', {})
        
        # Introduction
        intro = Paragraph(
            "Your work orientation reveals your natural preferences for different types of work "
            "environments and task approaches. This section analyzes four key orientation styles: "
            "Creative, Analytical, People-Centric, and Administrative.",
            self.styles['ReportBody']
        )
        elements.append(intro)
        elements.append(Spacer(1, 0.2*inch))
        
        # Score breakdown
        elements.append(Paragraph("Your Orientation Scores", self.styles['SubsectionHeading']))
        
        score_data = [["Orientation Type", "Score", "Band", "Interpretation"]]
        for key, value in scores.items():
            band = self._get_band(value)
            interpretation = self._get_orientation_interpretation(key, value)
            score_data.append([
                key.replace('_', ' ').title(),
                f"{value}%",
                band,
                interpretation
            ])
        
        score_table = Table(score_data, colWidths=[2*inch, 1*inch, 1*inch, 2.5*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A2B4B')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(score_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Bar chart
        bar_chart = self._create_bar_chart(scores, "Work Orientation Scores")
        if bar_chart:
            elements.append(bar_chart)
            elements.append(Spacer(1, 0.2*inch))
        
        # Detailed interpretation (500-700 words)
        elements.append(Paragraph("Detailed Interpretation", self.styles['SubsectionHeading']))
        
        interpretation_text = self._generate_orientation_detailed_interpretation(scores, scoring_details)
        elements.append(Paragraph(interpretation_text, self.styles['Interpretation']))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Work environment preferences
        elements.append(Paragraph("Work Environment Preferences", self.styles['SubsectionHeading']))
        env_prefs = self._generate_environment_preferences(scores)
        elements.append(Paragraph(env_prefs, self.styles['ReportBody']))
        
        return elements
    
    def _create_interest_section(self, test_result: Dict) -> List:
        """Create 3-4 page interest analysis"""
        elements = []
        
        elements.append(Paragraph("Section 2: Interest Mapping", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        scores = test_result.get('scores', {})
        
        # Similar detailed structure as orientation
        # ... (implementation continues)
        
        return elements
    
    def _create_personality_section(self, test_result: Dict) -> List:
        """Create 4-5 page personality analysis"""
        elements = []
        
        elements.append(Paragraph("Section 3: Personality Profile", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        # ... (detailed implementation)
        
        return elements
    
    def _create_aptitude_section(self, test_result: Dict) -> List:
        """Create 3-4 page aptitude analysis"""
        elements = []
        
        elements.append(Paragraph("Section 4: Cognitive Aptitude Analysis", self.styles['SectionHeading']))
        # ... (detailed implementation)
        
        return elements
    
    def _create_eq_section(self, test_result: Dict) -> List:
        """Create 3-4 page EQ analysis"""
        elements = []
        
        elements.append(Paragraph("Section 5: Emotional Intelligence Profile", self.styles['SectionHeading']))
        # ... (detailed implementation)
        
        return elements
    
    def _create_career_recommendations(self, test_results: List[Dict]) -> List:
        """Create 3-4 page career recommendations"""
        elements = []
        
        elements.append(Paragraph("Section 6: Career Recommendations", self.styles['SectionHeading']))
        # ... (detailed implementation with top 10 careers)
        
        return elements
    
    def _create_strengths_development(self, test_results: List[Dict]) -> List:
        """Create 2 page strengths and development roadmap"""
        elements = []
        
        elements.append(Paragraph("Section 7: Strengths & Development Roadmap", self.styles['SectionHeading']))
        # ... (detailed implementation)
        
        return elements
    
    def _create_career_pathways(self, test_results: List[Dict]) -> List:
        """Create 2-3 page career pathways"""
        elements = []
        
        elements.append(Paragraph("Section 8: Career Pathways", self.styles['SectionHeading']))
        # ... (detailed implementation)
        
        return elements
    
    def _create_appendix(self) -> List:
        """Create appendix with glossary and disclaimers"""
        elements = []
        
        elements.append(Paragraph("Appendix", self.styles['SectionHeading']))
        
        # Disclaimer
        disclaimer = Paragraph(
            "<b>Important Disclaimer:</b><br/><br/>"
            "This psychometric assessment report is a guidance tool designed to help you understand "
            "your strengths, interests, and potential career directions. It is NOT a deterministic "
            "prediction of your future success or a clinical diagnosis. Career decisions should be "
            "made in consultation with parents, educators, and professional counselors, considering "
            "multiple factors including personal interests, academic performance, family circumstances, "
            "and market opportunities.<br/><br/>"
            "The assessment results represent your responses at a specific point in time and may evolve "
            "as you grow and gain more experiences. We recommend combining these insights with practical "
            "exploration, internships, and career counseling for the best outcomes.<br/><br/>"
            "<b>Final decisions regarding your career path rest with you and your family.</b>",
            self.styles['ReportBody']
        )
        elements.append(disclaimer)
        
        return elements
    
    # Helper methods for charts and analysis
    
    def _create_radar_chart(self, all_scores: Dict) -> RLImage:
        """Create radar chart for 5 dimensions"""
        try:
            # Extract average scores for each dimension
            dimensions = ['Orientation', 'Interest', 'Personality', 'Aptitude', 'EQ']
            values = []
            
            for test_type in ['orientation', 'interest', 'personality', 'aptitude', 'eq']:
                if test_type in all_scores:
                    scores = all_scores[test_type]['scores']
                    avg_score = sum(scores.values()) / len(scores) if scores else 50
                    values.append(avg_score)
                else:
                    values.append(50)
            
            # Create radar chart
            angles = np.linspace(0, 2 * np.pi, len(dimensions), endpoint=False).tolist()
            values += values[:1]  # Complete the circle
            angles += angles[:1]
            
            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='polar'))
            ax.plot(angles, values, 'o-', linewidth=2, color='#1A2B4B')
            ax.fill(angles, values, alpha=0.25, color='#5D7A68')
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(dimensions, size=10)
            ax.set_ylim(0, 100)
            ax.set_yticks([20, 40, 60, 80, 100])
            ax.set_yticklabels(['20', '40', '60', '80', '100'], size=8)
            ax.grid(True)
            ax.set_title('5-Dimensional Profile', size=12, weight='bold', pad=20)
            
            # Save to bytes
            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            buf.seek(0)
            plt.close()
            
            return RLImage(buf, width=4*inch, height=4*inch)
        except Exception as e:
            print(f"Error creating radar chart: {e}")
            return None
    
    def _create_bar_chart(self, scores: Dict, title: str) -> RLImage:
        """Create bar chart for sub-dimension scores"""
        try:
            labels = [k.replace('_', ' ').title() for k in scores.keys()]
            values = list(scores.values())
            
            fig, ax = plt.subplots(figsize=(6, 4))
            bars = ax.barh(labels, values, color='#5D7A68')
            
            # Color code by band
            for i, (bar, value) in enumerate(zip(bars, values)):
                if value >= 70:
                    bar.set_color('#5D7A68')  # High - Green
                elif value >= 40:
                    bar.set_color('#C87961')  # Moderate - Orange
                else:
                    bar.set_color('#94A3B8')  # Low - Gray
            
            ax.set_xlabel('Score (%)', size=10)
            ax.set_title(title, size=12, weight='bold')
            ax.set_xlim(0, 100)
            ax.grid(axis='x', alpha=0.3)
            
            # Add value labels
            for i, v in enumerate(values):
                ax.text(v + 2, i, f'{v}%', va='center', size=9)
            
            plt.tight_layout()
            
            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            buf.seek(0)
            plt.close()
            
            return RLImage(buf, width=5*inch, height=3*inch)
        except Exception as e:
            print(f"Error creating bar chart: {e}")
            return None
    
    def _get_band(self, score: float) -> str:
        """Get interpretive band for score"""
        if score < 40:
            return "Low"
        elif score < 70:
            return "Moderate"
        else:
            return "High"
    
    def _get_orientation_interpretation(self, orientation_type: str, score: float) -> str:
        """Get brief interpretation for orientation score"""
        band = self._get_band(score)
        
        interpretations = {
            'creative': {
                'High': 'Strong creative thinking',
                'Moderate': 'Balanced creativity',
                'Low': 'Prefers structured work'
            },
            'analytical': {
                'High': 'Excellent analytical skills',
                'Moderate': 'Good problem solver',
                'Low': 'Prefers intuitive approach'
            },
            'people_centric': {
                'High': 'Highly people-oriented',
                'Moderate': 'Comfortable with people',
                'Low': 'Prefers independent work'
            },
            'administrative': {
                'High': 'Highly organized',
                'Moderate': 'Adequately organized',
                'Low': 'Flexible approach'
            }
        }
        
        return interpretations.get(orientation_type, {}).get(band, 'See detailed analysis')
    
    def _generate_orientation_detailed_interpretation(self, scores: Dict, scoring_details: Dict) -> str:
        """Generate 500-700 word interpretation for orientation"""
        # Get dominant orientation
        dominant = max(scores, key=scores.get)
        dominant_score = scores[dominant]
        
        interpretation = f"""
        Your work orientation assessment reveals that your dominant style is <b>{dominant.replace('_', ' ').title()}</b> 
        with a score of {dominant_score}%. This indicates...
        
        [Detailed 500-700 word analysis would be generated here based on the specific scores and patterns]
        
        Your scores suggest that you are naturally inclined toward work environments that...
        
        In practical terms, this orientation means you would likely thrive in roles that...
        
        It's important to note that while {dominant.replace('_', ' ')} is your primary orientation, 
        you also show {self._get_band(scores[list(scores.keys())[1]])} levels in {list(scores.keys())[1].replace('_', ' ')}, 
        which adds versatility to your work style...
        """
        
        return interpretation
    
    def _generate_environment_preferences(self, scores: Dict) -> str:
        """Generate environment preferences based on orientation scores"""
        # Implementation for environment preferences
        return "Based on your orientation profile, you would likely prefer..."
    
    def _identify_top_strengths(self, all_scores: Dict, top_n: int = 5) -> List[Dict]:
        """Identify top N strengths across all dimensions"""
        all_traits = []
        
        for test_type, data in all_scores.items():
            scores = data.get('scores', {})
            for trait, score in scores.items():
                all_traits.append({
                    'dimension': test_type,
                    'trait': trait,
                    'score': score,
                    'band': self._get_band(score)
                })
        
        # Sort by score
        all_traits.sort(key=lambda x: x['score'], reverse=True)
        return all_traits[:top_n]
    
    def _identify_development_areas(self, all_scores: Dict, top_n: int = 3) -> List[Dict]:
        """Identify top N development areas"""
        all_traits = []
        
        for test_type, data in all_scores.items():
            scores = data.get('scores', {})
            for trait, score in scores.items():
                all_traits.append({
                    'dimension': test_type,
                    'trait': trait,
                    'score': score,
                    'band': self._get_band(score)
                })
        
        # Sort by score (ascending)
        all_traits.sort(key=lambda x: x['score'])
        return all_traits[:top_n]
    
    def _generate_quick_career_indicators(self, all_scores: Dict) -> List[str]:
        """Generate quick career direction indicators"""
        indicators = []
        
        # Analyze orientation
        if 'orientation' in all_scores:
            orientation_scores = all_scores['orientation']['scores']
            max_orient = max(orientation_scores, key=orientation_scores.get)
            if max_orient == 'creative':
                indicators.append("Consider careers in Design, Arts, Media, or Creative Technology")
            elif max_orient == 'analytical':
                indicators.append("Consider careers in Engineering, Science, Data Analytics, or Research")
            elif max_orient == 'people_centric':
                indicators.append("Consider careers in Education, Healthcare, HR, or Social Services")
            elif max_orient == 'administrative':
                indicators.append("Consider careers in Management, Operations, Administration, or Project Management")
        
        # Add more based on other dimensions
        # ... (additional logic)
        
        return indicators
