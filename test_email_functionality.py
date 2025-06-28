#!/usr/bin/env python3
"""
Email Functionality Test Script for ResidenceGuard AI
Tests all email components and configurations
"""

import os
import sys
from datetime import datetime
from utils.config import config
from utils.email_sender import email_sender

def test_email_configuration():
    """Test email configuration loading"""
    print("🔧 Testing Email Configuration...")
    
    try:
        # Test config loading
        email_config = config.get_email_config()
        print(f"✅ SMTP Server: {email_config['smtp_server']}")
        print(f"✅ SMTP Port: {email_config['smtp_port']}")
        print(f"✅ Sender Email: {email_config['sender_email']}")
        print(f"✅ Residence Life Email: {email_config['residence_life_email']}")
        
        # Check if password is set (don't print it)
        if email_config['sender_password']:
            print("✅ Sender Password: [CONFIGURED]")
        else:
            print("❌ Sender Password: [NOT CONFIGURED]")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Configuration Error: {str(e)}")
        return False

def test_smtp_connection():
    """Test SMTP connection"""
    print("\n🔌 Testing SMTP Connection...")
    
    try:
        # Test connection without sending
        import smtplib
        
        smtp_server = config.get_email_config()['smtp_server']
        smtp_port = int(config.get_email_config()['smtp_port'])
        
        print(f"Connecting to {smtp_server}:{smtp_port}...")
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            print("✅ SMTP Connection: SUCCESS")
            return True
            
    except Exception as e:
        print(f"❌ SMTP Connection Failed: {str(e)}")
        return False

def test_email_authentication():
    """Test email authentication"""
    print("\n🔐 Testing Email Authentication...")
    
    try:
        import smtplib
        
        email_config = config.get_email_config()
        smtp_server = email_config['smtp_server']
        smtp_port = int(email_config['smtp_port'])
        sender_email = email_config['sender_email']
        sender_password = email_config['sender_password']
        
        print(f"Authenticating {sender_email}...")
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            print("✅ Email Authentication: SUCCESS")
            return True
            
    except Exception as e:
        print(f"❌ Email Authentication Failed: {str(e)}")
        if "Invalid credentials" in str(e):
            print("💡 Tip: Check if you're using an App Password for Gmail")
        elif "Username and Password not accepted" in str(e):
            print("💡 Tip: Enable 2-factor authentication and generate an App Password")
        return False

def test_email_sending():
    """Test actual email sending"""
    print("\n📧 Testing Email Sending...")
    
    try:
        # Create a test report file
        test_report_path = "test_report.pdf"
        with open(test_report_path, "w") as f:
            f.write("This is a test report for email functionality testing.")
        
        # Test sending email
        email_config = config.get_email_config()
        
        result = email_sender.send_incident_report(
            report_path=test_report_path,
            staff_name="Test Staff",
            building_name="Test Building",
            room_number="101",
            incident_date=datetime.now().date(),
            incident_time=datetime.now().time(),
            student_name="Test Student"
        )
        
        # Clean up test file
        if os.path.exists(test_report_path):
            os.remove(test_report_path)
        
        if result:
            print("✅ Email Sending: SUCCESS")
            print("📬 Check your email inbox for the test message")
            return True
        else:
            print("❌ Email Sending: FAILED")
            return False
            
    except Exception as e:
        print(f"❌ Email Sending Error: {str(e)}")
        return False

def test_email_content():
    """Test email content generation"""
    print("\n📝 Testing Email Content Generation...")
    
    try:
        # Test subject generation
        subject = email_sender._generate_subject(
            {"violation_assessment": {"violation_found": True}},
            "101",
            "Test Building"
        )
        print(f"✅ Subject Generation: {subject}")
        
        # Test body generation
        body = email_sender._generate_body(
            staff_name="Test Staff",
            building_name="Test Building",
            room_number="101",
            incident_date=datetime.now().date(),
            incident_time=datetime.now().time(),
            student_name="Test Student"
        )
        print(f"✅ Body Generation: {len(body)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Content Generation Error: {str(e)}")
        return False

def main():
    """Run all email tests"""
    print("🚨 ResidenceGuard AI - Email Functionality Test")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("💡 Please copy env.example to .env and configure your email settings")
        return
    
    # Run tests
    tests = [
        ("Configuration", test_email_configuration),
        ("SMTP Connection", test_smtp_connection),
        ("Authentication", test_email_authentication),
        ("Content Generation", test_email_content),
        ("Email Sending", test_email_sending)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} Test Crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All email functionality tests passed!")
        print("📧 Email system is ready for use")
    else:
        print("⚠️ Some tests failed. Please check your email configuration.")
        print("\n💡 Common Issues:")
        print("1. Gmail requires App Passwords (not regular passwords)")
        print("2. Enable 2-factor authentication on your Gmail account")
        print("3. Generate an App Password in Google Account settings")
        print("4. Use the App Password in your .env file")

if __name__ == "__main__":
    main() 