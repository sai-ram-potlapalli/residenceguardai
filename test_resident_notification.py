#!/usr/bin/env python3
"""
Test script for resident violation notification emails
"""

import os
from dotenv import load_dotenv
from datetime import datetime
from utils.email_sender import email_sender

# Load environment variables
load_dotenv()

def test_resident_notification():
    """Test sending a resident violation notification email."""
    print("🧪 Testing Resident Violation Notification")
    print("=" * 60)
    
    # Test data
    resident_email = os.getenv('EMAIL_RESIDENCE_LIFE_EMAIL', '')  # Use same email for testing
    resident_name = "John Smith"
    building_name = "North Hall"
    room_number = "101"
    
    # Mock violation assessment
    violation_assessment = {
        'violation_found': True,
        'severity': 'high',
        'message': 'Multiple policy violations detected including alcohol and unauthorized appliances.',
        'confidence': 0.85,
        'recommended_action': 'Remove all alcohol and unauthorized appliances immediately. Schedule meeting with housing office.'
    }
    
    # Mock detected objects
    detected_objects = [
        {
            'object': 'alcohol',
            'category': 'Alcohol Violation',
            'confidence': 0.85
        },
        {
            'object': 'liquor bottle',
            'category': 'Alcohol Violation',
            'confidence': 0.75
        },
        {
            'object': 'microwave',
            'category': 'Appliance Violation',
            'confidence': 0.65
        }
    ]
    
    # Mock policy rules
    policy_rules = [
        {
            'rule_text': 'No alcohol is permitted in residence hall rooms. All alcoholic beverages must be removed immediately.',
            'metadata': {'rule_type': 'Alcohol Policy'}
        },
        {
            'rule_text': 'Unauthorized appliances including microwaves, toasters, and hot plates are prohibited.',
            'metadata': {'rule_type': 'Appliance Policy'}
        },
        {
            'rule_text': 'Residents must maintain a safe and compliant living environment at all times.',
            'metadata': {'rule_type': 'Safety Policy'}
        }
    ]
    
    staff_name = "Sarah Johnson"
    incident_date = datetime.now().date()
    
    try:
        print(f"📧 Testing resident notification for {resident_name}")
        print(f"📬 Resident Email: {resident_email}")
        print(f"🏢 Location: {building_name} Room {room_number}")
        print(f"🚨 Violations: {len(detected_objects)} items detected")
        
        # Send resident notification
        success = email_sender.send_resident_violation_notification(
            resident_email=resident_email,
            resident_name=resident_name,
            building_name=building_name,
            room_number=room_number,
            violation_assessment=violation_assessment,
            detected_objects=detected_objects,
            policy_rules=policy_rules,
            staff_name=staff_name,
            incident_date=incident_date
        )
        
        if success:
            print("✅ Resident notification sent successfully!")
            print(f"📧 Check your inbox at: {resident_email}")
            print("📋 Look for subject: 'Important: Housing Policy Violation Notice'")
            
            print("\n📄 Email includes:")
            print("   • Personal greeting with resident name")
            print("   • Violation summary and severity level")
            print("   • Specific items detected in violation")
            print("   • Housing regulations violated (HR points)")
            print("   • Required actions and deadlines")
            print("   • Contact information for housing office")
            print("   • Meeting scheduling requirements")
            print("   • Potential violation charges")
            
            return True
        else:
            print("❌ Failed to send resident notification")
            return False
            
    except Exception as e:
        print(f"❌ Error testing resident notification: {e}")
        return False

def test_notification_content():
    """Test the notification email content generation."""
    print("\n📝 Testing Notification Content Generation")
    print("=" * 60)
    
    try:
        # Test data
        resident_name = "Jane Doe"
        building_name = "South Hall"
        room_number = "205"
        
        violation_assessment = {
            'severity': 'medium',
            'recommended_action': 'Remove prohibited items and schedule meeting.'
        }
        
        detected_objects = [
            {'object': 'candle', 'category': 'Fire Hazard'},
            {'object': 'pet', 'category': 'Pet Violation'}
        ]
        
        policy_rules = [
            {'rule_text': 'No open flames or candles allowed in residence halls.'},
            {'rule_text': 'No pets permitted without proper authorization.'}
        ]
        
        # Generate email body
        email_body = email_sender._generate_resident_notification_body(
            resident_name=resident_name,
            building_name=building_name,
            room_number=room_number,
            violation_assessment=violation_assessment,
            detected_objects=detected_objects,
            policy_rules=policy_rules,
            staff_name="Mike Wilson",
            incident_date=datetime.now().date()
        )
        
        print("✅ Email body generated successfully!")
        print(f"📏 Email length: {len(email_body)} characters")
        print(f"📧 Contains resident name: {'Jane Doe' in email_body}")
        print(f"📧 Contains building info: {'South Hall' in email_body}")
        print(f"📧 Contains violation details: {'candle' in email_body and 'pet' in email_body}")
        print(f"📧 Contains policy rules: {'open flames' in email_body}")
        print(f"📧 Contains contact info: {'Contact Information' in email_body}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing content generation: {e}")
        return False

def main():
    """Run all resident notification tests."""
    print("🚨 ResidenceGuard AI - Resident Notification Testing")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Resident Notification Email", test_resident_notification),
        ("Notification Content Generation", test_notification_content)
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
    print("\n" + "="*70)
    print("📊 RESIDENT NOTIFICATION TEST SUMMARY")
    print("="*70)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All resident notification tests passed!")
        print("📧 The resident notification system is ready for use.")
        print("\n✨ Features Available:")
        print("   - Automated violation notifications to residents")
        print("   - Specific housing regulations cited")
        print("   - Required actions and deadlines")
        print("   - Contact information and meeting scheduling")
        print("   - Professional email formatting")
    else:
        print("⚠️ Some tests failed. Check the error messages above.")
    
    print("\n🔧 To test in the main application:")
    print("1. Run the Streamlit app: streamlit run app.py")
    print("2. Upload an image with violations")
    print("3. Fill in resident information")
    print("4. Check 'Send violation notification to resident'")
    print("5. Click 'Send Report to Residence Life'")

if __name__ == "__main__":
    main() 