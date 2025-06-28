#!/usr/bin/env python3
"""
Comprehensive Email Delivery Debugging Script
Tests multiple scenarios to ensure emails are actually received
"""

import os
from dotenv import load_dotenv
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import requests
import json

# Load environment variables FIRST
load_dotenv()

def check_email_configuration():
    """Check email configuration and provide detailed diagnostics."""
    print("🔍 EMAIL CONFIGURATION DIAGNOSTICS")
    print("=" * 60)
    
    # Get environment variables
    smtp_server = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('EMAIL_SMTP_PORT', '587'))
    sender_email = os.getenv('EMAIL_SENDER_EMAIL', '')
    sender_password = os.getenv('EMAIL_SENDER_PASSWORD', '')
    recipient_email = os.getenv('EMAIL_RESIDENCE_LIFE_EMAIL', '')
    
    print(f"📧 SMTP Server: {smtp_server}:{smtp_port}")
    print(f"📧 Sender Email: {sender_email}")
    print(f"📧 Recipient Email: {recipient_email}")
    print(f"📧 Password: {'*' * len(sender_password) if sender_password else 'NOT SET'}")
    
    # Validate configuration
    issues = []
    if not sender_email:
        issues.append("❌ Sender email not configured")
    if not sender_password:
        issues.append("❌ Sender password not configured")
    if not recipient_email:
        issues.append("❌ Recipient email not configured")
    if '@' not in sender_email:
        issues.append("❌ Invalid sender email format")
    if '@' not in recipient_email:
        issues.append("❌ Invalid recipient email format")
    
    if issues:
        print("\n🚨 CONFIGURATION ISSUES:")
        for issue in issues:
            print(f"   {issue}")
        return False
    else:
        print("\n✅ Configuration looks good!")
        return True

def test_smtp_connection_detailed():
    """Test SMTP connection with detailed error reporting."""
    print("\n🔌 DETAILED SMTP CONNECTION TEST")
    print("=" * 60)
    
    try:
        smtp_server = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('EMAIL_SMTP_PORT', '587'))
        sender_email = os.getenv('EMAIL_SENDER_EMAIL', '')
        sender_password = os.getenv('EMAIL_SENDER_PASSWORD', '')
        
        print(f"🔗 Connecting to {smtp_server}:{smtp_port}...")
        
        # Test connection
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        print("✅ SMTP connection established")
        
        # Test STARTTLS
        server.starttls()
        print("✅ STARTTLS enabled")
        
        # Test login
        print("🔐 Attempting login...")
        server.login(sender_email, sender_password)
        print("✅ Login successful!")
        
        # Test server capabilities
        print("📋 Server capabilities:")
        if server.has_extn('AUTH'):
            print("   ✅ AUTH supported")
        if server.has_extn('STARTTLS'):
            print("   ✅ STARTTLS supported")
        
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("\n💡 Gmail App Password Solutions:")
        print("1. Go to https://myaccount.google.com/security")
        print("2. Enable 2-Step Verification")
        print("3. Go to 'App passwords'")
        print("4. Generate password for 'Mail'")
        print("5. Use the 16-character password (not your regular password)")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Connection Solutions:")
        print("1. Check internet connection")
        print("2. Try different SMTP port (587 or 465)")
        print("3. Check firewall settings")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def send_test_email_with_tracking():
    """Send a test email with unique tracking information."""
    print("\n📤 SENDING TEST EMAIL WITH TRACKING")
    print("=" * 60)
    
    try:
        smtp_server = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('EMAIL_SMTP_PORT', '587'))
        sender_email = os.getenv('EMAIL_SENDER_EMAIL', '')
        sender_password = os.getenv('EMAIL_SENDER_PASSWORD', '')
        recipient_email = os.getenv('EMAIL_RESIDENCE_LIFE_EMAIL', '')
        
        # Create unique tracking ID
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        tracking_id = f"RGAI_{timestamp}"
        
        # Create email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"🧪 ResidenceGuard AI Test - {tracking_id}"
        
        # Create detailed body
        body = f"""
🚨 ResidenceGuard AI - Email Delivery Test

📊 Test Information:
- Tracking ID: {tracking_id}
- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- SMTP Server: {smtp_server}:{smtp_port}
- Sender: {sender_email}
- Recipient: {recipient_email}

✅ If you receive this email, the delivery system is working!

🔍 Next Steps:
1. Reply to this email with "RECEIVED" to confirm delivery
2. Check your spam/junk folder if you don't see it
3. Add {sender_email} to your contacts

📧 Email Details:
- Subject: {msg['Subject']}
- From: {sender_email}
- To: {recipient_email}
- Date: {datetime.now().strftime('%B %d, %Y at %I:%M:%S %p')}

Best regards,
ResidenceGuard AI System

---
This is an automated test email from the Residence Life Violation Detection System.
Tracking ID: {tracking_id}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        print(f"📤 Sending test email...")
        print(f"   Tracking ID: {tracking_id}")
        print(f"   Subject: {msg['Subject']}")
        print(f"   To: {recipient_email}")
        
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()
        server.login(sender_email, sender_password)
        
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print("✅ Test email sent successfully!")
        print(f"📬 Please check your inbox at: {recipient_email}")
        print(f"🔍 Look for subject: {msg['Subject']}")
        print(f"📋 Tracking ID: {tracking_id}")
        
        return tracking_id
        
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        return None

def test_multiple_recipients():
    """Test sending to multiple email addresses to isolate the issue."""
    print("\n📧 TESTING MULTIPLE RECIPIENTS")
    print("=" * 60)
    
    # Test recipients (add your own email addresses here)
    test_recipients = [
        os.getenv('EMAIL_RESIDENCE_LIFE_EMAIL', ''),
        # Add your personal email for testing
        # "your-personal-email@gmail.com"
    ]
    
    smtp_server = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('EMAIL_SMTP_PORT', '587'))
    sender_email = os.getenv('EMAIL_SENDER_EMAIL', '')
    sender_password = os.getenv('EMAIL_SENDER_PASSWORD', '')
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()
        server.login(sender_email, sender_password)
        
        for recipient in test_recipients:
            if not recipient:
                continue
                
            print(f"📤 Testing recipient: {recipient}")
            
            # Create test email
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = f"🧪 ResidenceGuard AI Test - {datetime.now().strftime('%H%M%S')}"
            
            body = f"""
ResidenceGuard AI Test Email

This is a test email to verify delivery to: {recipient}

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

If you receive this, please reply with "RECEIVED".

Best regards,
ResidenceGuard AI
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            text = msg.as_string()
            server.sendmail(sender_email, recipient, text)
            print(f"   ✅ Sent to {recipient}")
        
        server.quit()
        print("\n✅ All test emails sent!")
        
    except Exception as e:
        print(f"❌ Error testing multiple recipients: {e}")

def check_email_delivery_tips():
    """Provide comprehensive email delivery troubleshooting tips."""
    print("\n💡 EMAIL DELIVERY TROUBLESHOOTING")
    print("=" * 60)
    
    print("📬 Check these locations for emails:")
    print("   1. 📧 Inbox")
    print("   2. 🗑️ Spam/Junk folder")
    print("   3. 📁 All Mail (Gmail)")
    print("   4. 📂 Archive folder")
    print("   5. 🔍 Search for 'ResidenceGuard' or 'Test'")
    
    print("\n🔧 Common Solutions:")
    print("   1. Add sender email to contacts")
    print("   2. Check email filters and rules")
    print("   3. Whitelist the sender domain")
    print("   4. Check email client settings")
    print("   5. Try a different email client")
    
    print("\n📱 Gmail-Specific Tips:")
    print("   1. Check 'Promotions' tab")
    print("   2. Look in 'Updates' tab")
    print("   3. Search for 'in:spam' or 'in:trash'")
    print("   4. Check 'All Mail' instead of 'Inbox'")
    
    print("\n⏰ Timing Considerations:")
    print("   - Emails may take 1-5 minutes to arrive")
    print("   - Check again after 10 minutes")
    print("   - Some servers have delivery delays")

def test_email_with_attachment():
    """Test sending email with attachment to ensure full functionality."""
    print("\n📎 TESTING EMAIL WITH ATTACHMENT")
    print("=" * 60)
    
    try:
        # Create a test attachment
        test_file = "test_attachment.txt"
        with open(test_file, "w") as f:
            f.write("This is a test attachment from ResidenceGuard AI\n")
            f.write(f"Generated at: {datetime.now()}\n")
            f.write("If you can see this, email attachments are working!\n")
        
        smtp_server = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('EMAIL_SMTP_PORT', '587'))
        sender_email = os.getenv('EMAIL_SENDER_EMAIL', '')
        sender_password = os.getenv('EMAIL_SENDER_PASSWORD', '')
        recipient_email = os.getenv('EMAIL_RESIDENCE_LIFE_EMAIL', '')
        
        # Create email with attachment
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"📎 ResidenceGuard AI - Attachment Test {datetime.now().strftime('%H%M%S')}"
        
        body = """
ResidenceGuard AI - Attachment Test

This email includes a test attachment to verify full email functionality.

If you receive this email with the attachment, the complete email system is working!

Best regards,
ResidenceGuard AI
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach file
        with open(test_file, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {test_file}'
        )
        msg.attach(part)
        
        # Send email
        print(f"📤 Sending email with attachment...")
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()
        server.login(sender_email, sender_password)
        
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print("✅ Email with attachment sent successfully!")
        print(f"📎 Attachment: {test_file}")
        
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email with attachment: {e}")
        return False

def main():
    """Run comprehensive email delivery diagnostics."""
    print("🚨 ResidenceGuard AI - Email Delivery Diagnostics")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all diagnostics
    tests = [
        ("Configuration Check", check_email_configuration),
        ("SMTP Connection", test_smtp_connection_detailed),
        ("Test Email with Tracking", send_test_email_with_tracking),
        ("Multiple Recipients", test_multiple_recipients),
        ("Email with Attachment", test_email_with_attachment)
    ]
    
    results = {}
    tracking_id = None
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_name == "Test Email with Tracking":
                tracking_id = test_func()
                results[test_name] = tracking_id is not None
            else:
                results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*70)
    print("📊 EMAIL DELIVERY DIAGNOSTIC SUMMARY")
    print("="*70)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All email tests passed!")
        if tracking_id:
            print(f"📧 Test email sent with tracking ID: {tracking_id}")
        print("📬 Please check your email inbox and spam folder")
    else:
        print("⚠️ Some tests failed. Check the error messages above.")
    
    # Provide troubleshooting tips
    check_email_delivery_tips()
    
    print(f"\n🔧 Next Steps:")
    print(f"1. Check your email inbox at: {os.getenv('EMAIL_RESIDENCE_LIFE_EMAIL', '')}")
    print(f"2. Look for emails with subject containing 'ResidenceGuard AI'")
    if tracking_id:
        print(f"3. Search for tracking ID: {tracking_id}")
    print(f"4. Check spam/junk folder")
    print(f"5. Reply to any test emails you receive")

if __name__ == "__main__":
    main() 