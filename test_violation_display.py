#!/usr/bin/env python3
"""
Test script to verify violation detection and display logic.
"""

def test_violation_display():
    """Test the violation display logic with sample data."""
    
    # Sample violation assessment (from your debug logs)
    violation_assessment = {
        'violation_found': True,
        'message': '🚨 CRITICAL POLICY VIOLATION DETECTED: alcohol, liquor bottle are strictly prohibited in residence halls.',
        'confidence': 0.99,
        'recommended_action': 'IMMEDIATE REMOVAL REQUIRED - Contact campus security immediately',
        'violating_objects': ['alcohol', 'liquor bottle'],
        'matching_rules': ['Alcohol policy - alcoholic beverages are not permitted'],
        'severity': 'critical'
    }
    
    print("🔍 Testing Violation Display Logic")
    print("=" * 50)
    
    # Test 1: Check violation_found
    print(f"1. violation_found value: {violation_assessment.get('violation_found')}")
    print(f"   Type: {type(violation_assessment.get('violation_found'))}")
    print(f"   Boolean check: {bool(violation_assessment.get('violation_found'))}")
    
    # Test 2: Check the condition
    condition_result = violation_assessment.get('violation_found')
    print(f"\n2. Condition check: {condition_result}")
    print(f"   Should show violations: {condition_result == True}")
    
    # Test 3: Test the actual UI logic
    if violation_assessment.get('violation_found'):
        print("\n3. ✅ UI Logic: Should display violations")
        print(f"   Message: {violation_assessment.get('message')}")
        print(f"   Violating objects: {violation_assessment.get('violating_objects')}")
    else:
        print("\n3. ❌ UI Logic: Should NOT display violations")
    
    # Test 4: Check compliance status
    compliance_status = "non_compliant" if violation_assessment.get('violation_found') else "compliant"
    print(f"\n4. Compliance status: {compliance_status}")
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")

if __name__ == "__main__":
    test_violation_display() 