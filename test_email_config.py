#!/usr/bin/env python3
"""
Test email configuration for ResidenceGuard AI.
This script helps diagnose email sending issues.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.config import config
from utils.email_sender import email_sender

def test_email_configuration():
    """Test the email configuration and provide detailed feedback."""
    print("🔧 Testing Email Configuration")
    print("=" * 50)
    
    # Check config values
    print("\n📋 Configuration Check:")
    print(f"SMTP Server: {config.EMAIL_HOST}")
    print(f"SMTP Port: {config.EMAIL_PORT}")
    print(f"Sender Email: {config.EMAIL_USER}")
    print(f"Password Set: {'✅ YES' if config.EMAIL_PASSWORD else '❌ NO'}")
    print(f"Residence Life Email: {config.RESIDENCE_LIFE_EMAIL}")
    
    # Check if required fields are set
    if not config.EMAIL_USER:
        print("\n❌ ERROR: EMAIL_USER is not set")
        print("Please set EMAIL_USER in your .env file or environment variables")
        return False
    
    if not config.EMAIL_PASSWORD:
        print("\n❌ ERROR: EMAIL_PASSWORD is not set")
        print("Please set EMAIL_PASSWORD in your .env file or environment variables")
        return False
    
    print("\n✅ Basic configuration looks good!")
    
    # Test SMTP connection
    print("\n🔌 Testing SMTP Connection:")
    try:
        print(f"Connecting to {config.EMAIL_HOST}:{config.EMAIL_PORT}...")
        server = smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT)
        server.starttls()
        print("✅ TLS connection established")
        
        print("Attempting login...")
        server.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
        print("✅ Login successful!")
        
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("\n💡 Common solutions:")
        print("1. Check your email and password are correct")
        print("2. If using Gmail, make sure you're using an App Password")
        print("3. Enable 2-Factor Authentication and generate an App Password")
        return False
        
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_email_sender_class():
    """Test the EmailSender class functionality."""
    print("\n📧 Testing EmailSender Class:")
    print("=" * 50)
    
    # Check email sender configuration
    config_info = email_sender.get_email_config()
    print("EmailSender Configuration:")
    for key, value in config_info.items():
        if 'password' in key.lower():
            print(f"  {key}: {'*' * len(value) if value else 'NOT SET'}")
        else:
            print(f"  {key}: {value}")
    
    # Test email generation
    print("\n📝 Testing Email Generation:")
    sample_data = {
        'violation_assessment': {
            'violation_found': True,
            'severity': 'high',
            'confidence': 0.95,
            'message': 'Test violation detected'
        },
        'image_analysis': {
            'detected_objects': [
                {'object': 'candle', 'confidence': 0.9, 'category': 'fire_hazard'}
            ]
        },
        'policy_analysis': {
            'relevant_rules': [
                {'rule_text': 'No open flames allowed in residence halls'}
            ]
        }
    }
    
    try:
        subject = email_sender._generate_subject(sample_data, "101", "Test Building")
        print(f"✅ Subject generated: {subject}")
        
        email_body = email_sender._generate_email_body(
            sample_data, "Test Staff", "101", "Test Building"
        )
        print("✅ Email body generated successfully")
        
        meeting_date = email_sender._get_next_business_day()
        print(f"✅ Meeting date calculated: {meeting_date}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating email content: {e}")
        return False

def send_test_email():
    """Send a test email to verify the complete email flow."""
    print("\n📤 Sending Test Email:")
    print("=" * 50)
    
    try:
        # Create a simple test email
        msg = MIMEMultipart()
        msg['From'] = config.EMAIL_USER
        msg['To'] = config.RESIDENCE_LIFE_EMAIL
        msg['Subject'] = "Test Email - ResidenceGuard AI Configuration"
        
        body = f"""
        <html>
        <body>
            <h2>ResidenceGuard AI - Email Configuration Test</h2>
            <p>This is a test email to verify that your email configuration is working correctly.</p>
            <p><strong>Test Details:</strong></p>
            <ul>
                <li>SMTP Server: {config.EMAIL_HOST}</li>
                <li>SMTP Port: {config.EMAIL_PORT}</li>
                <li>Sender: {config.EMAIL_USER}</li>
                <li>Recipient: {config.RESIDENCE_LIFE_EMAIL}</li>
                <li>Timestamp: {config.RESIDENCE_LIFE_EMAIL}</li>
            </ul>
            <p>If you receive this email, your email configuration is working correctly!</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Send the email
        server = smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT)
        server.starttls()
        server.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
        
        text = msg.as_string()
        server.sendmail(config.EMAIL_USER, config.RESIDENCE_LIFE_EMAIL, text)
        server.quit()
        
        print("✅ Test email sent successfully!")
        print(f"📧 Check your inbox at: {config.RESIDENCE_LIFE_EMAIL}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        return False

def main():
    """Run all email configuration tests."""
    print("🚀 ResidenceGuard AI - Email Configuration Test")
    print("=" * 60)
    
    # Test 1: Basic configuration
    config_ok = test_email_configuration()
    
    # Test 2: EmailSender class
    sender_ok = test_email_sender_class()
    
    # Test 3: Send test email (only if previous tests passed)
    if config_ok and sender_ok:
        print("\n" + "=" * 60)
        print("🎯 All basic tests passed! Sending test email...")
        email_ok = send_test_email()
        
        if email_ok:
            print("\n🎉 SUCCESS: Email configuration is working correctly!")
            print("You can now use the ResidenceGuard AI system to send violation reports.")
        else:
            print("\n⚠️ WARNING: Test email failed, but configuration looks correct.")
            print("This might be a temporary network issue or email provider restriction.")
    else:
        print("\n❌ FAILED: Email configuration has issues that need to be fixed.")
        print("Please check the error messages above and update your configuration.")
    
    print("\n" + "=" * 60)
    print("📚 For help with email setup, see EMAIL_SETUP.md")

if __name__ == "__main__":
    main() 