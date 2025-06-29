#!/usr/bin/env python3
"""
Email functionality for sending violation reports to Residence Life office.
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from utils.config import config

class EmailSender:
    """Handles email communication for violation reports."""
    
    def __init__(self):
        # Use config object instead of environment variables directly
        self.smtp_server = config.EMAIL_HOST
        self.smtp_port = config.EMAIL_PORT
        self.sender_email = config.EMAIL_USER
        self.sender_password = config.EMAIL_PASSWORD
        self.residence_life_email = config.RESIDENCE_LIFE_EMAIL
        
    def get_email_config(self) -> Dict[str, str]:
        """Get current email configuration settings."""
        return {
            'smtp_server': self.smtp_server,
            'smtp_port': str(self.smtp_port),
            'sender_email': self.sender_email,
            'sender_password': self.sender_password,
            'residence_life_email': self.residence_life_email
        }
    
    def send_violation_report(self, 
                            report_path: str,
                            violation_data: Dict[str, Any],
                            staff_name: str = "",
                            room_number: str = "",
                            building_name: str = "") -> bool:
        """
        Send violation report email to Residence Life office.
        
        Args:
            report_path: Path to the generated PDF report
            violation_data: Dictionary containing violation details
            staff_name: Name of the staff member who conducted the inspection
            room_number: Room number where violation was found
            building_name: Building name where violation was found
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.residence_life_email
            msg['Subject'] = self._generate_subject(violation_data, room_number, building_name)
            
            # Generate email body
            email_body = self._generate_email_body(violation_data, staff_name, room_number, building_name)
            msg.attach(MIMEText(email_body, 'html'))
            
            # Attach PDF report
            if os.path.exists(report_path):
                with open(report_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(report_path)}'
                )
                msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, self.residence_life_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            print(f"SMTP Server: {self.smtp_server}:{self.smtp_port}")
            print(f"Sender Email: {self.sender_email}")
            print(f"Recipient Email: {self.residence_life_email}")
            return False
    
    def _generate_subject(self, violation_data: Dict[str, Any], room_number: str, building_name: str) -> str:
        """Generate email subject line."""
        severity = violation_data.get('violation_assessment', {}).get('severity', 'medium').upper()
        return f"URGENT: Policy Violation - {building_name} Room {room_number} - {severity} Priority"
    
    def _generate_email_body(self, violation_data: Dict[str, Any], staff_name: str, room_number: str, building_name: str) -> str:
        """Generate professional email body with violation details."""
        
        # Extract violation details
        violation_assessment = violation_data.get('violation_assessment', {})
        detected_objects = violation_data.get('image_analysis', {}).get('detected_objects', [])
        policy_rules = violation_data.get('policy_analysis', {}).get('relevant_rules', [])
        
        # Format detected objects
        objects_list = ""
        for obj in detected_objects[:5]:  # Show top 5 objects
            confidence = obj.get('confidence', 0)
            objects_list += f"<li><strong>{obj.get('object', 'Unknown')}</strong> ({confidence:.1%} confidence) - {obj.get('category', 'Unknown')}</li>"
        
        # Format policy rules
        rules_list = ""
        for rule in policy_rules[:3]:  # Show top 3 rules
            rules_list += f"<li>{rule.get('rule_text', 'No rule text available')}</li>"
        
        # Generate meeting date (next business day)
        meeting_date = self._get_next_business_day()
        
        # Generate email template
        email_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #d32f2f; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .violation-box {{ background-color: #fff3e0; border-left: 4px solid #ff9800; padding: 15px; margin: 15px 0; }}
                .action-box {{ background-color: #e8f5e8; border-left: 4px solid #4caf50; padding: 15px; margin: 15px 0; }}
                .urgent {{ color: #d32f2f; font-weight: bold; }}
                .highlight {{ background-color: #fff9c4; padding: 2px 4px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚨 POLICY VIOLATION REPORT</h1>
                <p>Residence Life Office - Immediate Action Required</p>
            </div>
            
            <div class="content">
                <p><strong>Date:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                <p><strong>Location:</strong> {building_name} - Room {room_number}</p>
                <p><strong>Inspected By:</strong> {staff_name or 'Residence Life Staff'}</p>
                
                <div class="violation-box">
                    <h2>🚨 VIOLATION SUMMARY</h2>
                    <p><strong>Status:</strong> <span class="urgent">POLICY VIOLATION CONFIRMED</span></p>
                    <p><strong>Severity Level:</strong> {violation_assessment.get('severity', 'medium').upper()}</p>
                    <p><strong>Confidence Level:</strong> {violation_assessment.get('confidence', 0):.1%}</p>
                    <p><strong>Assessment:</strong> {violation_assessment.get('message', 'Violation detected')}</p>
                </div>
                
                <h3>📸 DETECTED VIOLATIONS</h3>
                <ul>
                    {objects_list}
                </ul>
                
                <h3>📋 POLICY RULES VIOLATED</h3>
                <ul>
                    {rules_list}
                </ul>
                
                <div class="action-box">
                    <h2>⚡ IMMEDIATE ACTION REQUIRED</h2>
                    
                    <h3>1. Meeting Scheduling</h3>
                    <p>Please schedule a mandatory meeting with the resident for <span class="highlight">{meeting_date}</span> to discuss:</p>
                    <ul>
                        <li>Policy violation details and consequences</li>
                        <li>Required corrective actions</li>
                        <li>Potential disciplinary measures</li>
                        <li>Future compliance expectations</li>
                    </ul>
                    
                    <h3>2. Policy Violation Charges</h3>
                    <p>Based on the <span class="highlight">Residence Life Policy Document</span>, the following charges may apply:</p>
                    <ul>
                        <li><strong>Policy Violation Fee:</strong> $50.00 (standard violation)</li>
                        <li><strong>Safety Violation Fee:</strong> $100.00 (if safety hazard confirmed)</li>
                        <li><strong>Repeat Offense:</strong> Additional $25.00 (if applicable)</li>
                        <li><strong>Documentation Fee:</strong> $15.00 (processing and administrative)</li>
                    </ul>
                    
                    <h3>3. Required Follow-up Actions</h3>
                    <ul>
                        <li>Document this violation in the resident's file</li>
                        <li>Issue formal written warning</li>
                        <li>Schedule follow-up inspection within 48 hours</li>
                        <li>Update resident's compliance record</li>
                    </ul>
                </div>
                
                <h3>📞 Contact Information</h3>
                <p><strong>Residence Life Office:</strong> (555) 123-4567</p>
                <p><strong>Emergency Contact:</strong> (555) 999-8888</p>
                <p><strong>Email:</strong> reslife@university.edu</p>
                
                <p><strong>Note:</strong> This report has been automatically generated by the AI-Powered Violation Detection System. 
                All findings have been verified through image analysis and policy cross-reference.</p>
                
                <p><em>Please review the attached detailed report for complete documentation and evidence.</em></p>
                
                <hr>
                <p style="font-size: 12px; color: #666;">
                    This is an automated message from the Residence Life Violation Detection System.<br>
                    Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </p>
            </div>
        </body>
        </html>
        """
        
        return email_html
    
    def _get_next_business_day(self) -> str:
        """Get the next business day (Monday-Friday)."""
        today = datetime.now()
        next_day = today + timedelta(days=1)
        
        # Skip weekends
        while next_day.weekday() >= 5:  # Saturday = 5, Sunday = 6
            next_day += timedelta(days=1)
        
        return next_day.strftime('%A, %B %d, %Y at 2:00 PM')
    
    def send_confirmation_email(self, recipient_email: str, report_path: str, violation_data: Dict[str, Any]) -> bool:
        """Send confirmation email to staff member who generated the report."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = "Violation Report Generated Successfully"
            
            body = f"""
            <html>
            <body>
                <h2>✅ Violation Report Generated</h2>
                <p>Your violation report has been successfully generated and sent to the Residence Life office.</p>
                
                <h3>Report Details:</h3>
                <ul>
                    <li><strong>Date:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</li>
                    <li><strong>Violation Status:</strong> {violation_data.get('compliance_status', 'unknown')}</li>
                    <li><strong>Report File:</strong> {os.path.basename(report_path)}</li>
                </ul>
                
                <p>The Residence Life office has been notified and will follow up with the resident as appropriate.</p>
                
                <p><em>Thank you for using the AI-Powered Violation Detection System.</em></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Attach report
            if os.path.exists(report_path):
                with open(report_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(report_path)}'
                )
                msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, recipient_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error sending confirmation email: {e}")
            return False

    def send_incident_report(self, 
                           report_path: str,
                           staff_name: str = "",
                           building_name: str = "",
                           room_number: str = "",
                           incident_date = None,
                           incident_time = None,
                           student_name: str = "") -> bool:
        """
        Send incident report email to Residence Life office.
        
        Args:
            report_path: Path to the generated PDF report
            staff_name: Name of the staff member who conducted the inspection
            building_name: Building name where incident occurred
            room_number: Room number where incident occurred
            incident_date: Date of the incident
            incident_time: Time of the incident
            student_name: Name of the student involved
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Validate email configuration
            if not self.sender_email or not self.sender_password:
                print(f"ERROR: Email configuration missing. Sender: {self.sender_email}, Password: {'SET' if self.sender_password else 'NOT SET'}")
                return False
            
            # Validate report file exists
            if not os.path.exists(report_path):
                print(f"ERROR: Report file not found: {report_path}")
                return False
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.residence_life_email
            msg['Subject'] = f"Incident Report - {building_name} Room {room_number}"
            
            # Generate email body
            email_body = self._generate_body(
                staff_name=staff_name,
                building_name=building_name,
                room_number=room_number,
                incident_date=incident_date,
                incident_time=incident_time,
                student_name=student_name
            )
            msg.attach(MIMEText(email_body, 'html'))
            
            # Attach PDF report
            with open(report_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(report_path)}'
            )
            msg.attach(part)
            
            # Send email with detailed error handling
            print(f"DEBUG: Attempting to send email via {self.smtp_server}:{self.smtp_port}")
            print(f"DEBUG: From: {self.sender_email}")
            print(f"DEBUG: To: {self.residence_life_email}")
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            
            print("DEBUG: Starting SMTP login...")
            server.login(self.sender_email, self.sender_password)
            print("DEBUG: SMTP login successful")
            
            text = msg.as_string()
            server.sendmail(self.sender_email, self.residence_life_email, text)
            server.quit()
            
            print("DEBUG: Email sent successfully")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"ERROR: SMTP Authentication failed: {e}")
            print("This usually means the email or password is incorrect, or 2FA is enabled without an app password")
            return False
        except smtplib.SMTPException as e:
            print(f"ERROR: SMTP error occurred: {e}")
            return False
        except Exception as e:
            print(f"ERROR: Unexpected error sending email: {e}")
            print(f"SMTP Server: {self.smtp_server}:{self.smtp_port}")
            print(f"Sender Email: {self.sender_email}")
            print(f"Recipient Email: {self.residence_life_email}")
            return False
    
    def _generate_body(self, 
                      staff_name: str = "",
                      building_name: str = "",
                      room_number: str = "",
                      incident_date = None,
                      incident_time = None,
                      student_name: str = "") -> str:
        """Generate email body for incident report."""
        
        # Format date and time
        date_str = incident_date.strftime('%B %d, %Y') if incident_date else datetime.now().strftime('%B %d, %Y')
        time_str = incident_time.strftime('%I:%M %p') if incident_time else datetime.now().strftime('%I:%M %p')
        
        # Generate email template
        email_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #1976d2; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .info-box {{ background-color: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; margin: 15px 0; }}
                .action-box {{ background-color: #e8f5e8; border-left: 4px solid #4caf50; padding: 15px; margin: 15px 0; }}
                .highlight {{ background-color: #fff9c4; padding: 2px 4px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📋 INCIDENT REPORT</h1>
                <p>ResidenceGuard AI - Automated Incident Documentation</p>
            </div>
            
            <div class="content">
                <div class="info-box">
                    <h2>📅 Incident Details</h2>
                    <p><strong>Date:</strong> {date_str}</p>
                    <p><strong>Time:</strong> {time_str}</p>
                    <p><strong>Location:</strong> {building_name} - Room {room_number}</p>
                    <p><strong>Inspected By:</strong> {staff_name or 'Residence Life Staff'}</p>
                    {f'<p><strong>Student:</strong> {student_name}</p>' if student_name else ''}
                </div>
                
                <h3>📋 Report Summary</h3>
                <p>An incident report has been generated using the AI-Powered Violation Detection System. 
                The attached PDF contains detailed information about the inspection findings, including:</p>
                
                <ul>
                    <li>Objects detected in the room</li>
                    <li>Policy compliance assessment</li>
                    <li>Violation details (if any)</li>
                    <li>Relevant policy rules</li>
                    <li>Recommended actions</li>
                </ul>
                
                <div class="action-box">
                    <h2>⚡ Next Steps</h2>
                    <ol>
                        <li><strong>Review the attached report</strong> for complete incident details</li>
                        <li><strong>Schedule follow-up</strong> if violations were detected</li>
                        <li><strong>Document in student records</strong> as appropriate</li>
                        <li><strong>Take corrective action</strong> if required</li>
                    </ol>
                </div>
                
                <h3>📞 Contact Information</h3>
                <p><strong>Residence Life Office:</strong> (555) 123-4567</p>
                <p><strong>Email:</strong> {self.residence_life_email}</p>
                
                <p><strong>Note:</strong> This report was automatically generated by ResidenceGuard AI. 
                All findings have been verified through AI-powered image analysis and policy cross-reference.</p>
                
                <hr>
                <p style="font-size: 12px; color: #666;">
                    This is an automated message from ResidenceGuard AI.<br>
                    Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </p>
            </div>
        </body>
        </html>
        """
        
        return email_html

    def send_resident_violation_notification(self,
                                           resident_email: str,
                                           resident_name: str,
                                           building_name: str,
                                           room_number: str,
                                           violation_assessment: dict,
                                           detected_objects: list,
                                           policy_rules: list,
                                           staff_name: str = "",
                                           incident_date = None) -> bool:
        """
        Send violation notification email to resident.
        
        Args:
            resident_email: Email address of the resident
            resident_name: Name of the resident
            building_name: Building name where violation occurred
            room_number: Room number where violation occurred
            violation_assessment: Dictionary containing violation details
            detected_objects: List of detected objects
            policy_rules: List of relevant policy rules
            staff_name: Name of the staff member who conducted the inspection
            incident_date: Date of the incident
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            print(f"🔍 DEBUG: send_resident_violation_notification called for {resident_name}")
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = resident_email
            msg['Subject'] = f"Important: Housing Policy Violation Notice - {building_name} Room {room_number}"
            
            # Generate email body
            email_body = self._generate_resident_notification_body(
                resident_name=resident_name,
                building_name=building_name,
                room_number=room_number,
                violation_assessment=violation_assessment,
                detected_objects=detected_objects,
                policy_rules=policy_rules,
                staff_name=staff_name,
                incident_date=incident_date
            )
            msg.attach(MIMEText(email_body, 'html'))
            
            # Send email
            print(f"🔍 DEBUG: Sending resident notification to {resident_email}")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, resident_email, text)
            server.quit()
            
            print(f"✅ Resident notification sent successfully to {resident_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending resident notification: {e}")
            print(f"❌ Error type: {type(e)}")
            import traceback
            print(f"❌ Full traceback: {traceback.format_exc()}")
            return False
    
    def _generate_resident_notification_body(self,
                                           resident_name: str,
                                           building_name: str,
                                           room_number: str,
                                           violation_assessment: dict,
                                           detected_objects: list,
                                           policy_rules: list,
                                           staff_name: str = "",
                                           incident_date = None) -> str:
        """Generate email body for resident violation notification."""
        
        # Format date
        date_str = incident_date.strftime('%B %d, %Y') if incident_date else datetime.now().strftime('%B %d, %Y')
        
        # Format detected objects
        objects_list = ""
        for obj in detected_objects[:5]:  # Show top 5 objects
            confidence = obj.get('confidence', 0)
            if isinstance(confidence, dict):
                confidence = list(confidence.values())[0] if confidence else 0
            objects_list += f"<li><strong>{obj.get('object', 'Unknown')}</strong> - {obj.get('category', 'Unknown')}</li>"
        
        # Format policy rules
        rules_list = ""
        for i, rule in enumerate(policy_rules[:3], 1):  # Show top 3 rules
            rule_text = rule.get('rule_text', 'No rule text available')
            rules_list += f"<li><strong>HR {i}:</strong> {rule_text}</li>"
        
        # Get severity and recommended action
        severity = violation_assessment.get('severity', 'medium')
        if isinstance(severity, str):
            severity_display = severity.upper()
        else:
            severity_display = str(severity)
        
        recommended_action = violation_assessment.get('recommended_action', 'Please contact the Housing Office for guidance.')
        
        # Generate meeting date (next business day)
        meeting_date = self._get_next_business_day()
        
        # Generate email template
        email_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #d32f2f; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .violation-box {{ background-color: #fff3e0; border-left: 4px solid #ff9800; padding: 15px; margin: 15px 0; }}
                .action-box {{ background-color: #e8f5e8; border-left: 4px solid #4caf50; padding: 15px; margin: 15px 0; }}
                .urgent {{ color: #d32f2f; font-weight: bold; }}
                .highlight {{ background-color: #fff9c4; padding: 2px 4px; }}
                .contact-box {{ background-color: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚨 HOUSING POLICY VIOLATION NOTICE</h1>
                <p>Residence Life Office - Immediate Action Required</p>
            </div>
            
            <div class="content">
                <p>Dear <strong>{resident_name}</strong>,</p>
                
                <p>This notice is to inform you that a policy violation has been detected in your residence hall room during a routine inspection conducted on <span class="highlight">{date_str}</span>.</p>
                
                <div class="violation-box">
                    <h2>🚨 VIOLATION SUMMARY</h2>
                    <p><strong>Location:</strong> {building_name} - Room {room_number}</p>
                    <p><strong>Inspection Date:</strong> {date_str}</p>
                    <p><strong>Inspected By:</strong> {staff_name or 'Residence Life Staff'}</p>
                    <p><strong>Severity Level:</strong> <span class="urgent">{severity_display}</span></p>
                    <p><strong>Status:</strong> <span class="urgent">POLICY VIOLATION CONFIRMED</span></p>
                </div>
                
                <h3>📸 ITEMS DETECTED IN VIOLATION</h3>
                <ul>
                    {objects_list}
                </ul>
                
                <h3>📋 SPECIFIC HOUSING REGULATIONS VIOLATED</h3>
                <p>The following Housing Regulations (HR) have been violated:</p>
                <ul>
                    {rules_list}
                </ul>
                
                <div class="action-box">
                    <h2>⚡ IMMEDIATE ACTION REQUIRED</h2>
                    
                    <h3>1. Mandatory Meeting</h3>
                    <p>You are required to schedule a meeting with the Residence Life Office by <span class="highlight">{meeting_date}</span> to discuss:</p>
                    <ul>
                        <li>Policy violation details and consequences</li>
                        <li>Required corrective actions</li>
                        <li>Potential disciplinary measures</li>
                        <li>Future compliance expectations</li>
                    </ul>
                    
                    <h3>2. Required Corrective Actions</h3>
                    <p><strong>Recommended Action:</strong> {recommended_action}</p>
                    
                    <h3>3. Policy Violation Charges</h3>
                    <p>Based on the Housing Regulations, the following charges may apply:</p>
                    <ul>
                        <li><strong>Policy Violation Fee:</strong> $50.00 (standard violation)</li>
                        <li><strong>Safety Violation Fee:</strong> $100.00 (if safety hazard confirmed)</li>
                        <li><strong>Repeat Offense:</strong> Additional $25.00 (if applicable)</li>
                        <li><strong>Documentation Fee:</strong> $15.00 (processing and administrative)</li>
                    </ul>
                </div>
                
                <div class="contact-box">
                    <h2>📞 CONTACT INFORMATION</h2>
                    <p><strong>Housing and Residence Life Office:</strong></p>
                    <ul>
                        <li><strong>Phone:</strong> (555) 123-4567</li>
                        <li><strong>Email:</strong> housing@university.edu</li>
                        <li><strong>Office Hours:</strong> Monday-Friday, 8:00 AM - 5:00 PM</li>
                        <li><strong>Location:</strong> Student Center, Room 101</li>
                    </ul>
                    
                    <p><strong>Emergency Contact:</strong> (555) 999-8888 (24/7)</p>
                </div>
                
                <h3>📋 IMPORTANT NEXT STEPS</h3>
                <ol>
                    <li><strong>Contact the Housing Office</strong> within 24 hours to schedule your meeting</li>
                    <li><strong>Remove or correct</strong> the violating items immediately</li>
                    <li><strong>Review the Housing Regulations</strong> to prevent future violations</li>
                    <li><strong>Attend the scheduled meeting</strong> to discuss the violation</li>
                </ol>
                
                <p><strong>Note:</strong> This violation has been documented in your student record. Failure to address this matter promptly may result in additional disciplinary action.</p>
                
                <p>If you have any questions or need clarification about this notice, please contact the Housing and Residence Life Office immediately.</p>
                
                <p>Sincerely,<br>
                <strong>Housing and Residence Life Office</strong><br>
                University Name</p>
                
                <hr>
                <p style="font-size: 12px; color: #666;">
                    This is an automated notice from the Residence Life Violation Detection System.<br>
                    Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                    Reference ID: {datetime.now().strftime('%Y%m%d%H%M%S')}
                </p>
            </div>
        </body>
        </html>
        """
        
        return email_html

# Global email sender instance
email_sender = EmailSender() 