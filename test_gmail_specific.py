#!/usr/bin/env python3
"""
Gmail-specific email testing to ensure emails are properly sent and visible
"""

import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Load environment variables
load_dotenv()

def test_gmail_smtp_ssl():
    """Test Gmail SMTP with SSL (port 465) instead of TLS."""
    print("🔒 Testing Gmail SMTP with SSL (Port 465)")
    print("=" * 50)
    
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 465  # SSL port
        sender_email = os.getenv('EMAIL_SENDER_EMAIL', '')
        sender_password = os.getenv('EMAIL_SENDER_PASSWORD', '')
        recipient_email = os.getenv('EMAIL_RESIDENCE_LIFE_EMAIL', '')
        
        print(f"🔗 Connecting to {smtp_server}:{smtp_port} (SSL)...")
        
        # Use SMTP_SSL instead of SMTP
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
        print("✅ SSL connection established")
        
        # Login
        print("🔐 Attempting login...")
        server.login(sender_email, sender_password)
        print("✅ Login successful!")
        
        # Create test email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"🔒 Gmail SSL Test - {datetime.now().strftime('%H%M%S')}"
        
        body = f"""
Gmail SSL Test Email

This email was sent using Gmail's SSL connection (port 465).

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Sender: {sender_email}
Recipient: {recipient_email}
Method: SMTP_SSL (Port 465)

If you receive this, SSL connection is working!

Best regards,
ResidenceGuard AI
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        print("📤 Sending email via SSL...")
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print("✅ Email sent successfully via SSL!")
        print(f"📧 Subject: {msg['Subject']}")
        print(f"📬 To: {recipient_email}")
        
        return True
        
    except Exception as e:
        print(f"❌ SSL test failed: {e}")
        return False

def test_gmail_with_different_from():
    """Test with different From address format."""
    print("\n📧 Testing Different From Address Format")
    print("=" * 50)
    
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv('EMAIL_SENDER_EMAIL', '')
        sender_password = os.getenv('EMAIL_SENDER_PASSWORD', '')
        recipient_email = os.getenv('EMAIL_RESIDENCE_LIFE_EMAIL', '')
        
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Create test email with different From format
        msg = MIMEMultipart()
        msg['From'] = f"ResidenceGuard AI <{sender_email}>"  # Different format
        msg['To'] = recipient_email
        msg['Subject'] = f"📧 From Format Test - {datetime.now().strftime('%H%M%S')}"
        
        body = f"""
From Format Test Email

This email uses a different From address format.

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
From: ResidenceGuard AI <{sender_email}>
To: {recipient_email}

Best regards,
ResidenceGuard AI
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        print("📤 Sending email with different From format...")
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print("✅ Email sent with different From format!")
        print(f"📧 Subject: {msg['Subject']}")
        
        return True
        
    except Exception as e:
        print(f"❌ From format test failed: {e}")
        return False

def test_gmail_to_self():
    """Test sending email to the same Gmail account."""
    print("\n📧 Testing Email to Self")
    print("=" * 50)
    
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv('EMAIL_SENDER_EMAIL', '')
        sender_password = os.getenv('EMAIL_SENDER_PASSWORD', '')
        
        # Send to the same email address
        recipient_email = sender_email
        
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Create test email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"📧 Self Test - {datetime.now().strftime('%H%M%S')}"
        
        body = f"""
Self Test Email

This email was sent to the same Gmail account.

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
From: {sender_email}
To: {recipient_email}

This should definitely appear in your inbox!

Best regards,
ResidenceGuard AI
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        print(f"📤 Sending email to self ({sender_email})...")
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print("✅ Self-test email sent!")
        print(f"📧 Subject: {msg['Subject']}")
        print(f"📬 Check your inbox at: {sender_email}")
        
        return True
        
    except Exception as e:
        print(f"❌ Self test failed: {e}")
        return False

def test_gmail_with_reply_to():
    """Test with Reply-To header."""
    print("\n📧 Testing with Reply-To Header")
    print("=" * 50)
    
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv('EMAIL_SENDER_EMAIL', '')
        sender_password = os.getenv('EMAIL_SENDER_PASSWORD', '')
        recipient_email = os.getenv('EMAIL_RESIDENCE_LIFE_EMAIL', '')
        
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Create test email with Reply-To
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Reply-To'] = sender_email  # Add Reply-To header
        msg['Subject'] = f"📧 Reply-To Test - {datetime.now().strftime('%H%M%S')}"
        
        body = f"""
Reply-To Test Email

This email includes a Reply-To header.

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
From: {sender_email}
To: {recipient_email}
Reply-To: {sender_email}

Best regards,
ResidenceGuard AI
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        print("📤 Sending email with Reply-To header...")
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print("✅ Email with Reply-To sent!")
        print(f"📧 Subject: {msg['Subject']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Reply-To test failed: {e}")
        return False

def check_gmail_settings():
    """Provide Gmail-specific troubleshooting tips."""
    print("\n🔧 Gmail-Specific Troubleshooting")
    print("=" * 50)
    
    print("📱 Check Gmail Settings:")
    print("1. Go to Gmail Settings (gear icon)")
    print("2. Check 'General' tab")
    print("3. Look for 'Send mail as' settings")
    print("4. Verify your email address is properly configured")
    
    print("\n🔍 Check Gmail Filters:")
    print("1. Go to Gmail Settings > Filters and Blocked Addresses")
    print("2. Check if there are any filters blocking your emails")
    print("3. Look for filters that might move emails to spam/trash")
    
    print("\n📧 Check Gmail Labels:")
    print("1. Look for custom labels that might be hiding emails")
    print("2. Check 'All Mail' instead of just 'Inbox'")
    print("3. Search for 'in:all' to see all emails")
    
    print("\n🚫 Check Gmail Security:")
    print("1. Go to Google Account Security")
    print("2. Check 'Less secure app access' (if applicable)")
    print("3. Verify 2-Step Verification is properly set up")
    print("4. Check if there are any security alerts")

def main():
    """Run Gmail-specific email tests."""
    print("🚨 ResidenceGuard AI - Gmail-Specific Email Testing")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run Gmail-specific tests
    tests = [
        ("Gmail SSL Test", test_gmail_smtp_ssl),
        ("Different From Format", test_gmail_with_different_from),
        ("Email to Self", test_gmail_to_self),
        ("Reply-To Header", test_gmail_with_reply_to)
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
    print("📊 GMAIL EMAIL TEST SUMMARY")
    print("="*60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All Gmail tests passed!")
        print("📧 Multiple test emails have been sent")
        print("📬 Check your Gmail inbox, spam, and all mail")
    else:
        print("⚠️ Some Gmail tests failed.")
    
    # Provide Gmail-specific troubleshooting
    check_gmail_settings()
    
    print(f"\n🔧 Next Steps:")
    print(f"1. Check your Gmail inbox at: {os.getenv('EMAIL_SENDER_EMAIL', '')}")
    print(f"2. Check the recipient email: {os.getenv('EMAIL_RESIDENCE_LIFE_EMAIL', '')}")
    print(f"3. Look for emails with subjects containing 'Test'")
    print(f"4. Check Gmail's 'All Mail' section")
    print(f"5. Search for 'in:all' in Gmail")

if __name__ == "__main__":
    main() 