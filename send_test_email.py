#!/usr/bin/env python3
"""
Send a test email to verify delivery
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_test_email():
    """Send a test email with unique subject."""
    
    # Get email configuration
    sender_email = os.getenv('EMAIL_SENDER_EMAIL', '')
    sender_password = os.getenv('EMAIL_SENDER_PASSWORD', '')
    recipient_email = os.getenv('EMAIL_RESIDENCE_LIFE_EMAIL', '')
    
    # Create unique subject
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    subject = f"🧪 ResidenceGuard AI Test Email - {timestamp}"
    
    # Create email content
    body = f"""
    🚨 ResidenceGuard AI - Email Test
    
    This is a test email to verify that the email functionality is working correctly.
    
    📊 Test Details:
    - Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    - Test ID: {timestamp}
    - Sender: {sender_email}
    - Recipient: {recipient_email}
    
    ✅ If you receive this email, the email system is working perfectly!
    
    🔍 Next Steps:
    1. Reply to this email to confirm receipt
    2. Check that you can receive violation reports
    3. Test the full application email functionality
    
    Best regards,
    ResidenceGuard AI System
    
    ---
    This is an automated test email from the Residence Life Violation Detection System.
    """
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        print(f"📤 Sending test email to {recipient_email}...")
        print(f"📧 Subject: {subject}")
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print("✅ Test email sent successfully!")
        print(f"📬 Please check your inbox at: {recipient_email}")
        print("🔍 Don't forget to check your spam folder!")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        return False

if __name__ == "__main__":
    print("🧪 ResidenceGuard AI - Email Test")
    print("=" * 40)
    send_test_email() 