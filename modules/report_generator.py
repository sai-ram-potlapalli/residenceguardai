import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from utils.config import config
from utils.helpers import format_timestamp, create_thumbnail, generate_unique_filename, extract_confidence

class ReportGenerator:
    """Generate structured incident reports in PDF format."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the report."""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # Section header style
        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkred
        )
        
        # Normal text style
        self.normal_style = ParagraphStyle(
            'NormalText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_LEFT
        )
        
        # Violation alert style
        self.violation_style = ParagraphStyle(
            'ViolationAlert',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            alignment=TA_LEFT,
            textColor=colors.red,
            backColor=colors.lightyellow
        )
    
    def generate_incident_report(self, 
                                image_path: str,
                                detected_objects: List[Dict[str, Any]],
                                violation_assessment: Dict[str, Any],
                                policy_rules: List[Dict[str, Any]],
                                user_notes: str = "",
                                staff_name: str = "",
                                room_number: str = "",
                                building_name: str = "") -> str:
        """
        Generate a comprehensive incident report PDF.
        
        Args:
            image_path: Path to the violation image
            detected_objects: List of detected objects
            violation_assessment: Violation assessment result
            policy_rules: Relevant policy rules
            user_notes: Additional notes from staff
            staff_name: Name of the reporting staff member
            room_number: Room number where violation occurred
            building_name: Building name
            
        Returns:
            Path to the generated PDF report
        """
        # Generate unique filename for the report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"incident_report_{timestamp}.pdf"
        report_path = config.get_report_path(report_filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(report_path, pagesize=letter)
        story = []
        
        # Add title
        story.append(Paragraph("INCIDENT REPORT", self.title_style))
        story.append(Spacer(1, 20))
        
        # Add report metadata
        story.extend(self._create_metadata_section(staff_name, room_number, building_name))
        
        # Add violation summary
        if violation_assessment.get("violation_found", False):
            story.extend(self._create_violation_summary_section(violation_assessment))
        
        # Add detected objects
        story.extend(self._create_objects_section(detected_objects))
        
        # Add policy rules
        story.extend(self._create_policy_rules_section(policy_rules))
        
        # Add image evidence
        image_story, temp_thumb_path = self._create_image_section(image_path)
        story.extend(image_story)
        
        # Add user notes
        if user_notes:
            story.extend(self._create_notes_section(user_notes))
        
        # Add action items
        story.extend(self._create_action_items_section(violation_assessment))
        
        # Build PDF
        doc.build(story)
        
        # Clean up temp file after PDF is built
        if temp_thumb_path and os.path.exists(temp_thumb_path):
            try:
                os.remove(temp_thumb_path)
            except Exception:
                pass
        
        return report_path
    
    def generate_incident_report_simple(self, incident_data: Dict[str, Any]) -> str:
        """
        Generate a simple incident report PDF from incident data.
        
        Args:
            incident_data: Dictionary containing incident information
            
        Returns:
            Path to the generated PDF report
        """
        # Generate unique filename for the report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"incident_report_{incident_data.get('incident_id', timestamp)}.pdf"
        report_path = os.path.join(config.REPORTS_DIR, report_filename)
        
        # Ensure reports directory exists
        os.makedirs(config.REPORTS_DIR, exist_ok=True)
        
        # Create PDF document
        doc = SimpleDocTemplate(report_path, pagesize=letter)
        story = []
        
        # Add title
        story.append(Paragraph("INCIDENT REPORT", self.title_style))
        story.append(Spacer(1, 20))
        
        # Add incident data
        story.append(Paragraph("Incident Information", self.section_style))
        
        data = [
            ["Incident ID:", incident_data.get("incident_id", "N/A")],
            ["Date:", incident_data.get("date", "N/A")],
            ["Location:", incident_data.get("location", "N/A")],
            ["Violation Type:", incident_data.get("violation_type", "N/A")],
            ["Description:", incident_data.get("description", "N/A")],
            ["Severity:", incident_data.get("severity", "N/A")],
            ["Action Taken:", incident_data.get("action_taken", "N/A")]
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        story.append(table)
        
        # Build PDF
        doc.build(story)
        
        return report_path
    
    def render_template(self, incident_data: Dict[str, Any]) -> str:
        """
        Render HTML template for incident report.
        
        Args:
            incident_data: Dictionary containing incident information
            
        Returns:
            HTML content as string
        """
        html_content = f"""
        <html>
        <head>
            <title>Incident Report - {incident_data.get('incident_id', 'N/A')}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 10px; text-align: center; }}
                .section {{ margin: 20px 0; }}
                .field {{ margin: 10px 0; }}
                .label {{ font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>INCIDENT REPORT</h1>
            </div>
            
            <div class="section">
                <h2>Incident Information</h2>
                <div class="field">
                    <span class="label">Incident ID:</span> {incident_data.get('incident_id', 'N/A')}
                </div>
                <div class="field">
                    <span class="label">Date:</span> {incident_data.get('date', 'N/A')}
                </div>
                <div class="field">
                    <span class="label">Location:</span> {incident_data.get('location', 'N/A')}
                </div>
                <div class="field">
                    <span class="label">Violation Type:</span> {incident_data.get('violation_type', 'N/A')}
                </div>
                <div class="field">
                    <span class="label">Description:</span> {incident_data.get('description', 'N/A')}
                </div>
                <div class="field">
                    <span class="label">Severity:</span> {incident_data.get('severity', 'N/A')}
                </div>
                <div class="field">
                    <span class="label">Action Taken:</span> {incident_data.get('action_taken', 'N/A')}
                </div>
            </div>
        </body>
        </html>
        """
        return html_content
    
    def _create_metadata_section(self, staff_name: str, room_number: str, building_name: str) -> List:
        """Create the metadata section of the report."""
        story = []
        
        story.append(Paragraph("Report Information", self.section_style))
        
        # Create metadata table
        data = [
            ["Report Date:", format_timestamp(datetime.now())],
            ["Staff Member:", staff_name or "Not specified"],
            ["Building:", building_name or "Not specified"],
            ["Room Number:", room_number or "Not specified"],
            ["Report ID:", f"IR-{datetime.now().strftime('%Y%m%d%H%M%S')}"]
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_violation_summary_section(self, violation_assessment: Dict[str, Any]) -> List:
        """Create the violation summary section."""
        story = []
        
        story.append(Paragraph("🚨 VIOLATION SUMMARY", self.section_style))
        
        # Violation status
        status_text = "VIOLATION DETECTED" if violation_assessment.get("violation_found", False) else "No Violation"
        status_color = colors.red if violation_assessment.get("violation_found", False) else colors.green
        
        status_style = ParagraphStyle(
            'Status',
            parent=self.normal_style,
            textColor=status_color,
            fontSize=14,
            spaceAfter=10
        )
        
        story.append(Paragraph(status_text, status_style))
        
        # Violation details
        if violation_assessment.get("violation_found", False):
            details = []
            
            if "message" in violation_assessment:
                details.append(f"Assessment: {violation_assessment['message']}")
            
            if "confidence" in violation_assessment:
                confidence = extract_confidence(violation_assessment["confidence"])
                details.append(f"Confidence: {confidence:.1%}")
            
            print("DEBUG violation_assessment:", violation_assessment)
            severity = violation_assessment.get('severity', 'Unknown')
            if isinstance(severity, str):
                details.append(f"Severity: {severity.upper()}")
            else:
                details.append(f"Severity: {severity}")
            
            if "recommended_action" in violation_assessment:
                details.append(f"Recommended Action: {violation_assessment['recommended_action']}")
            
            for detail in details:
                story.append(Paragraph(detail, self.normal_style))
        
        story.append(Spacer(1, 15))
        return story
    
    def _create_objects_section(self, detected_objects: List[Dict[str, Any]]) -> List:
        """Create the detected objects section."""
        story = []
        
        story.append(Paragraph("Detected Objects", self.section_style))
        
        if not detected_objects:
            story.append(Paragraph("No objects detected in the image.", self.normal_style))
        else:
            # Create objects table
            headers = ["Object", "Category", "Confidence"]
            data = [headers]
            
            for obj in detected_objects:
                data.append([
                    obj.get("object", "Unknown"),
                    obj.get("category", "Unknown"),
                    f"{extract_confidence(obj.get('confidence', 0)):.1%}"
                ])
            
            table = Table(data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            story.append(table)
        
        story.append(Spacer(1, 15))
        return story
    
    def _create_policy_rules_section(self, policy_rules: List[Dict[str, Any]]) -> List:
        """Create the policy rules section."""
        story = []
        
        story.append(Paragraph("Relevant Policy Rules", self.section_style))
        
        if not policy_rules:
            story.append(Paragraph("No relevant policy rules found.", self.normal_style))
        else:
            for i, rule in enumerate(policy_rules, 1):
                rule_text = rule.get("rule_text", "No rule text available")
                rule_type = rule.get("metadata", {}).get("rule_type", "General Policy")
                
                story.append(Paragraph(f"Rule {i} ({rule_type}):", self.normal_style))
                story.append(Paragraph(rule_text, self.normal_style))
                story.append(Spacer(1, 8))
        
        story.append(Spacer(1, 15))
        return story
    
    def _create_image_section(self, image_path: str):
        """Create the image evidence section. Returns (story, temp_thumb_path)."""
        story = []
        temp_thumb_path = None
        story.append(Paragraph("Image Evidence", self.section_style))
        try:
            # Create thumbnail for the report
            thumbnail_data = create_thumbnail(image_path, max_size=(400, 300))
            if thumbnail_data:
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                    temp_file.write(thumbnail_data)
                    temp_thumb_path = temp_file.name
                img = RLImage(temp_thumb_path, width=4*inch, height=3*inch)
                story.append(img)
            else:
                story.append(Paragraph("Image could not be processed for report.", self.normal_style))
        except Exception as e:
            story.append(Paragraph(f"Error processing image: {str(e)}", self.normal_style))
        story.append(Spacer(1, 15))
        return story, temp_thumb_path
    
    def _create_notes_section(self, user_notes: str) -> List:
        """Create the user notes section."""
        story = []
        
        story.append(Paragraph("Staff Notes", self.section_style))
        story.append(Paragraph(user_notes, self.normal_style))
        story.append(Spacer(1, 15))
        
        return story
    
    def _create_action_items_section(self, violation_assessment: Dict[str, Any]) -> List:
        """Create the action items section."""
        story = []
        
        story.append(Paragraph("Recommended Actions", self.section_style))
        
        if violation_assessment.get("violation_found", False):
            actions = [
                "1. Document the violation with this report",
                "2. Contact the resident to discuss the violation",
                "3. Issue appropriate disciplinary action if necessary",
                "4. Schedule a follow-up inspection",
                "5. Update resident file with violation record"
            ]
            
            for action in actions:
                story.append(Paragraph(action, self.normal_style))
        else:
            story.append(Paragraph("No immediate action required. Room appears to be compliant with housing policies.", self.normal_style))
        
        story.append(Spacer(1, 20))
        
        # Add signature line
        story.append(Paragraph("Staff Signature: _________________________", self.normal_style))
        story.append(Paragraph("Date: _________________________", self.normal_style))
        
        return story
    
    def generate_summary_report(self, reports_data: List[Dict[str, Any]]) -> str:
        """Generate a summary report of multiple incidents."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"summary_report_{timestamp}.pdf"
        report_path = config.get_report_path(report_filename)
        
        doc = SimpleDocTemplate(report_path, pagesize=letter)
        story = []
        
        # Title
        story.append(Paragraph("VIOLATION SUMMARY REPORT", self.title_style))
        story.append(Spacer(1, 20))
        
        # Summary statistics
        total_reports = len(reports_data)
        violations_found = sum(1 for r in reports_data if r.get("violation_found", False))
        
        summary_data = [
            ["Total Reports:", str(total_reports)],
            ["Violations Found:", str(violations_found)],
            ["Compliance Rate:", f"{((total_reports - violations_found) / total_reports * 100):.1f}%" if total_reports > 0 else "N/A"],
            ["Report Period:", f"{datetime.now().strftime('%B %Y')}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Individual reports summary
        story.append(Paragraph("Individual Reports", self.section_style))
        
        for i, report in enumerate(reports_data, 1):
            story.append(Paragraph(f"Report {i}:", self.normal_style))
            story.append(Paragraph(f"  - Date: {report.get('date', 'Unknown')}", self.normal_style))
            story.append(Paragraph(f"  - Room: {report.get('room_number', 'Unknown')}", self.normal_style))
            story.append(Paragraph(f"  - Violation: {'Yes' if report.get('violation_found', False) else 'No'}", self.normal_style))
            story.append(Spacer(1, 8))
        
        doc.build(story)
        return report_path

# Global generator instance
generator = ReportGenerator() 