#!/usr/bin/env python3
"""
Debug script to test analysis process
"""

import os
import sys
from modules.object_detection import detector
from modules.pdf_parser import parser
from modules.violation_checker import checker

def test_analysis_step_by_step():
    """Test analysis process step by step to identify the formatting error."""
    
    print("🔍 Testing Analysis Process Step by Step")
    print("=" * 50)
    
    # Check if we have test files
    test_pdf = "sample_policy.pdf"
    
    if not os.path.exists(test_pdf):
        print(f"❌ Test PDF not found: {test_pdf}")
        return
    
    try:
        print("1. Testing policy parsing...")
        policy_summary = parser.get_policy_summary(test_pdf)
        print(f"   ✅ Policy summary: {policy_summary}")
        
        print("\n2. Testing policy indexing...")
        parser.index_policy_rules(test_pdf, "test_policy")
        print("   ✅ Policy indexed")
        
        print("\n3. Testing rule search...")
        query = "microwave appliance"
        rules = parser.search_relevant_rules(query, n_results=2)
        print(f"   ✅ Found {len(rules)} relevant rules")
        
        if rules:
            print("   Sample rule:", rules[0])
            print("   Rule text type:", type(rules[0]['rule_text']))
            print("   Rule text content:", repr(rules[0]['rule_text']))
        
        print("\n4. Testing violation assessment with sample data...")
        # Test with sample data that might contain special characters
        sample_objects = [
            {"object": "microwave", "confidence": 0.8, "category": "appliance"}
        ]
        
        # Test with rules that might contain special characters
        sample_rules = [
            {"rule_text": "No microwaves allowed in rooms"},
            {"rule_text": "Appliances must be {approved} by housing"},
            {"rule_text": "No cooking devices except in designated areas"}
        ]
        
        image_context = {"room_type": "dorm room"}
        
        print("   Testing with sample data...")
        print("   Sample objects:", sample_objects)
        print("   Sample rules:", sample_rules)
        
        assessment = checker.assess_violation(sample_objects, sample_rules, image_context)
        print(f"   ✅ Assessment result: {assessment}")
        
        print("\n5. Testing with actual policy rules...")
        if rules:
            assessment2 = checker.assess_violation(sample_objects, rules, image_context)
            print(f"   ✅ Assessment with real rules: {assessment2}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_analysis_step_by_step() 