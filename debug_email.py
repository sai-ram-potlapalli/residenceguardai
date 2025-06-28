#!/usr/bin/env python3
"""
Comprehensive Email Debugging Script
Tests all aspects of email functionality and provides detailed diagnostics
"""

import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from utils.email_sender import email_sender
from utils.config import config

def check_environment_variables():
    """Check if all required email environment variables are set."""
    print("🔍 Checking Environment Variables")
    print("=" * 50)
    
    required_vars = [
        'EMAIL_SMTP_SERVER',
        'EMAIL_SMTP_PORT', 
        'EMAIL_SENDER_EMAIL',
        'EMAIL_SENDER_PASSWORD',
        'EMAIL_RESIDENCE_LIFE_EMAIL'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
            print(f"❌ {var}: Not set")
        else:
            # Mask password for security
            if 'PASSWORD' in var:
                masked_value = '*' * len(value) if value else 'Not set'
                print(f"✅ {var}: {masked_value}")
            else:
                print(f"✅ {var}: {value}")
    
    if missing_vars:
        print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file")
        return False
    
    print("\n✅ All environment variables are set!")
    return True

def test_smtp_connection():
    """Test SMTP server connection."""
    print("\n🔌 Testing SMTP Connection")
    print("=" * 50)
    
    try:
        smtp_server = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('EMAIL_SMTP_PORT', '587'))
        sender_email = os.getenv('EMAIL_SENDER_EMAIL', '')
        sender_password = os.getenv('EMAIL_SENDER_PASSWORD', '')
        
        print(f"🔗 Connecting to {smtp_server}:{smtp_port}...")
        
        # Test connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        print("✅ SMTP connection established")
        print("🔐 Attempting login...")
        
        # Test login
        server.login(sender_email, sender_password)
        print("✅ Login successful!")
        
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("\n💡 Common solutions:")
        print("1. Check if you're using an App Password (not your regular password)")
        print("2. Enable 2-factor authentication on your Gmail account")
        print("3. Generate a new App Password")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Common solutions:")
        print("1. Check your internet connection")
        print("2. Verify SMTP server and port are correct")
        print("3. Check if your firewall is blocking the connection")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_email_sending():
    """Test sending a simple email."""
    print("\n📧 Testing Email Sending")
    print("=" * 50)
    
    try:
        sender_email = os.getenv('EMAIL_SENDER_EMAIL', '')
        sender_password = os.getenv('EMAIL_SENDER_PASSWORD', '')
        recipient_email = os.getenv('EMAIL_RESIDENCE_LIFE_EMAIL', '')
        smtp_server = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('EMAIL_SMTP_PORT', '587'))
        
        # Create test email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"ResidenceGuard AI Test Email - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        body = f"""
        This is a test email from ResidenceGuard AI.
        
        Test Details:
        - Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        - SMTP Server: {smtp_server}:{smtp_port}
        - Sender: {sender_email}
        - Recipient: {recipient_email}
        
        If you receive this email, the email functionality is working correctly!
        
        Best regards,
        ResidenceGuard AI System
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        print("📤 Sending test email...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print("✅ Test email sent successfully!")
        print(f"📧 Check your inbox at: {recipient_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        return False

def test_email_sender_class():
    """Test the EmailSender class methods."""
    print("\n🏗️ Testing EmailSender Class")
    print("=" * 50)
    
    try:
        # Test subject generation
        sample_data = {
            "violation_assessment": {
                "severity": "high",
                "message": "Test violation"
            }
        }
        
        subject = email_sender._generate_subject(sample_data, "101", "Test Building")
        print(f"✅ Subject generation: {subject}")
        
        # Test email body generation
        email_body = email_sender._generate_email_body(
            sample_data, "Test Staff", "101", "Test Building"
        )
        print(f"✅ Email body generation: {len(email_body)} characters")
        
        # Test meeting date generation
        meeting_date = email_sender._get_next_business_day()
        print(f"✅ Meeting date generation: {meeting_date}")
        
        return True
        
    except Exception as e:
        print(f"❌ EmailSender class test failed: {e}")
        return False

def check_gmail_app_password():
    """Provide instructions for Gmail App Password setup."""
    print("\n📱 Gmail App Password Setup")
    print("=" * 50)
    print("If you're using Gmail, you need an App Password:")
    print()
    print("1. Go to your Google Account settings")
    print("2. Enable 2-Step Verification if not already enabled")
    print("3. Go to Security > App passwords")
    print("4. Generate a new app password for 'Mail'")
    print("5. Use this 16-character password in your .env file")
    print()
    print("Example .env configuration:")
    print("EMAIL_SENDER_EMAIL=your-email@gmail.com")
    print("EMAIL_SENDER_PASSWORD=abcd efgh ijkl mnop")
    print()

def check_spam_folder():
    """Provide instructions for checking spam folder."""
    print("\n📬 Email Delivery Check")
    print("=" * 50)
    print("If emails are being sent but not received:")
    print()
    print("1. Check your spam/junk folder")
    print("2. Add the sender email to your contacts")
    print("3. Check email filters and rules")
    print("4. Verify the recipient email address is correct")
    print()

def main():
    """Run all email diagnostics."""
    print("🚨 ResidenceGuard AI - Email Diagnostics")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all tests
    tests = [
        ("Environment Variables", check_environment_variables),
        ("SMTP Connection", test_smtp_connection),
        ("Email Sending", test_email_sending),
        ("EmailSender Class", test_email_sender_class)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("="*60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All email tests passed! Email functionality should be working.")
        print("📧 Check your inbox for the test email.")
    else:
        print("⚠️ Some tests failed. Check the error messages above.")
        print("\n💡 Common solutions:")
        check_gmail_app_password()
        check_spam_folder()
    
    print("\n🔧 For additional help:")
    print("- Check the EMAIL_SETUP.md file for detailed setup instructions")
    print("- Verify your .env file has the correct email credentials")
    print("- Test with a different email provider if Gmail doesn't work")

if __name__ == "__main__":
    main() 