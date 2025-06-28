#!/usr/bin/env python3
"""
Test script for email functionality
"""

import os
from utils.email_sender import email_sender

def test_email_configuration():
    """Test email configuration and functionality."""
    print("📧 Testing Email Configuration")
    print("=" * 40)
    
    # Check if email credentials are configured
    if not email_sender.sender_email or not email_sender.sender_password:
        print("❌ Email credentials not configured")
        print("Please set EMAIL_SENDER_EMAIL and EMAIL_SENDER_PASSWORD in your .env file")
        return False
    
    print(f"✅ SMTP Server: {email_sender.smtp_server}:{email_sender.smtp_port}")
    print(f"✅ Sender Email: {email_sender.sender_email}")
    print(f"✅ Residence Life Email: {email_sender.residence_life_email}")
    
    # Test email generation (without sending)
    sample_violation_data = {
        "violation_assessment": {
            "violation_found": True,
            "severity": "high",
            "confidence": 0.85,
            "message": "Microwave detected in room - safety violation"
        },
        "image_analysis": {
            "detected_objects": [
                {"object": "microwave", "confidence": 0.85, "category": "Appliance Violation"}
            ]
        },
        "policy_analysis": {
            "relevant_rules": [
                {"rule_text": "No microwaves allowed in residence hall rooms"}
            ]
        },
        "compliance_status": "non_compliant"
    }
    
    # Test subject generation
    subject = email_sender._generate_subject(sample_violation_data, "101", "North Hall")
    print(f"✅ Email Subject: {subject}")
    
    # Test email body generation
    email_body = email_sender._generate_email_body(
        sample_violation_data, "John Doe", "101", "North Hall"
    )
    print(f"✅ Email Body Generated: {len(email_body)} characters")
    
    # Test meeting date generation
    meeting_date = email_sender._get_next_business_day()
    print(f"✅ Suggested Meeting Date: {meeting_date}")
    
    print("\n📧 Email functionality is ready!")
    print("To send actual emails, configure your SMTP credentials in the .env file")
    
    return True

if __name__ == "__main__":
    test_email_configuration() 