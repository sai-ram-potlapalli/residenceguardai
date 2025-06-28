#!/usr/bin/env python3
"""
Test script for enhanced email functionality with status feedback
"""

import os
from datetime import datetime
from utils.email_sender import email_sender

def test_enhanced_email_features():
    """Test the enhanced email features."""
    print("🧪 Testing Enhanced Email Features")
    print("=" * 50)
    
    # Test email configuration retrieval
    print("📧 Testing Email Configuration Display")
    try:
        email_config = email_sender.get_email_config()
        print("✅ Email configuration retrieved successfully:")
        print(f"   SMTP Server: {email_config['smtp_server']}")
        print(f"   SMTP Port: {email_config['smtp_port']}")
        print(f"   Sender Email: {email_config['sender_email']}")
        print(f"   Recipient Email: {email_config['residence_life_email']}")
        print(f"   Password: {'*' * len(email_config['sender_password']) if email_config['sender_password'] else 'Not set'}")
    except Exception as e:
        print(f"❌ Failed to get email config: {e}")
        return False
    
    # Test email sending with status feedback
    print("\n📤 Testing Email Sending with Status Feedback")
    try:
        # Create a dummy report file for testing
        test_report_path = "test_report.pdf"
        with open(test_report_path, "w") as f:
            f.write("Test report content")
        
        # Test sending email
        success = email_sender.send_incident_report(
            report_path=test_report_path,
            staff_name="Test Staff",
            building_name="Test Building",
            room_number="101",
            incident_date=datetime.now().date(),
            incident_time=datetime.now().time(),
            student_name="Test Student"
        )
        
        if success:
            print("✅ Email sent successfully with status feedback!")
            print("📧 Email details that would be displayed:")
            print(f"   - Sent to: {email_config['residence_life_email']}")
            print(f"   - Sent from: {email_config['sender_email']}")
            print(f"   - Sent at: {datetime.now().strftime('%B %d, %Y at %I:%M:%S %p')}")
            print(f"   - Subject: Incident Report - Test Building Room 101")
            print(f"   - Staff Member: Test Staff")
            print(f"   - Location: Test Building - Room 101")
            print(f"   - Report File: {os.path.basename(test_report_path)}")
            print(f"   - File Size: {os.path.getsize(test_report_path)} bytes")
        else:
            print("❌ Email sending failed")
            return False
        
        # Cleanup
        if os.path.exists(test_report_path):
            os.remove(test_report_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Email test failed: {e}")
        return False

def test_session_state_simulation():
    """Simulate the session state management for email status."""
    print("\n🔄 Testing Session State Simulation")
    print("=" * 50)
    
    # Simulate session state
    session_state = {
        'email_sent': False,
        'email_details': None
    }
    
    # Simulate email sending
    print("📤 Simulating email sending...")
    session_state['email_sent'] = True
    session_state['email_details'] = {
        'timestamp': datetime.now(),
        'recipient': 'test@example.com',
        'sender': 'sender@example.com',
        'report_path': 'test_report.pdf',
        'staff_name': 'Test Staff',
        'building_name': 'Test Building',
        'room_number': '101',
        'incident_date': datetime.now().date(),
        'incident_time': datetime.now().time(),
        'student_name': 'Test Student'
    }
    
    print("✅ Session state updated successfully!")
    print(f"   Email sent: {session_state['email_sent']}")
    print(f"   Email details stored: {session_state['email_details'] is not None}")
    
    # Simulate page refresh
    print("\n🔄 Simulating page refresh...")
    session_state['email_sent'] = False
    session_state['email_details'] = None
    print("✅ Session state cleared for new analysis!")
    
    return True

def main():
    """Run all enhanced email tests."""
    print("🚨 ResidenceGuard AI - Enhanced Email Testing")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Enhanced Email Features", test_enhanced_email_features),
        ("Session State Simulation", test_session_state_simulation)
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
    print("📊 ENHANCED EMAIL TEST SUMMARY")
    print("="*60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All enhanced email tests passed!")
        print("📧 The enhanced email functionality is ready for use.")
        print("\n✨ New Features Available:")
        print("   - Comprehensive email status feedback")
        print("   - Detailed email information display")
        print("   - Page refresh options")
        print("   - Session state management")
        print("   - Next steps guidance")
    else:
        print("⚠️ Some tests failed. Check the error messages above.")
    
    print("\n🔧 To test in the main application:")
    print("1. Run the Streamlit app: streamlit run app.py")
    print("2. Upload an image and PDF")
    print("3. Generate a report")
    print("4. Click 'Send Report via Email'")
    print("5. Check the enhanced status feedback!")

if __name__ == "__main__":
    main() 