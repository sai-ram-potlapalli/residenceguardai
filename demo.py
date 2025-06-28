#!/usr/bin/env python3
"""
Demo script for the Violation Detection System.
This script demonstrates the system capabilities with sample data.
"""

import os
import sys
import tempfile
from PIL import Image, ImageDraw, ImageFont
import json

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_sample_image():
    """Create a sample image with a candle for demonstration."""
    # Create a simple room image with a candle
    img = Image.new('RGB', (400, 300), color='lightgray')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple room
    # Floor
    draw.rectangle([0, 200, 400, 300], fill='brown')
    
    # Wall
    draw.rectangle([0, 0, 400, 200], fill='white')
    
    # Window
    draw.rectangle([50, 50, 150, 150], fill='lightblue', outline='black', width=2)
    
    # Table
    draw.rectangle([200, 150, 350, 200], fill='darkbrown')
    
    # Candle (the violation!)
    # Candle base
    draw.ellipse([275, 120, 285, 150], fill='white', outline='black')
    # Candle flame
    draw.ellipse([275, 110, 285, 130], fill='yellow')
    draw.ellipse([278, 108, 282, 125], fill='orange')
    
    # Add some text
    try:
        font = ImageFont.load_default()
        draw.text((10, 10), "Sample Room with Candle", fill='black', font=font)
    except:
        draw.text((10, 10), "Sample Room with Candle", fill='black')
    
    return img

def create_sample_policy():
    """Create a sample policy document."""
    policy_content = """
    UNIVERSITY HOUSING POLICIES
    
    FIRE SAFETY RULES:
    1. Candles, incense, and any open flames are strictly prohibited in all residence halls.
    2. Smoking and vaping are not allowed in any building.
    3. Smoke detectors must not be covered or tampered with.
    
    APPLIANCE POLICIES:
    4. Only university-approved appliances are permitted.
    5. Microwaves, toasters, and hot plates are prohibited.
    
    PET POLICIES:
    6. Pets are not allowed except for approved service animals.
    
    ALCOHOL POLICIES:
    7. Alcohol is prohibited for students under 21 years of age.
    
    VIOLATION CONSEQUENCES:
    8. Violations may result in disciplinary action including fines or removal from housing.
    """
    
    return policy_content

def run_demo():
    """Run the complete demo."""
    print("🎬 Starting Violation Detection System Demo")
    print("=" * 50)
    
    try:
        # Import our modules
        from utils.config import config
        from modules.object_detection import detector
        from modules.pdf_parser import parser
        from modules.violation_checker import checker
        from modules.report_generator import generator
        
        print("✅ All modules imported successfully")
        
        # Create sample data
        print("\n📸 Creating sample image...")
        sample_image = create_sample_image()
        
        # Save sample image
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            sample_image.save(tmp_file.name, 'JPEG')
            image_path = tmp_file.name
        
        print("✅ Sample image created")
        
        # Create sample policy
        print("\n📄 Creating sample policy document...")
        policy_content = create_sample_policy()
        
        # Save policy as text file (simulating PDF content)
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp_file:
            tmp_file.write(policy_content.encode())
            policy_path = tmp_file.name
        
        print("✅ Sample policy created")
        
        # Step 1: Object Detection
        print("\n🔍 Step 1: Object Detection")
        print("-" * 30)
        
        detected_objects = detector.detect_objects(image_path, confidence_threshold=0.2)
        print(f"Detected {len(detected_objects)} objects:")
        
        for i, obj in enumerate(detected_objects, 1):
            print(f"  {i}. {obj['object']} ({obj['category']}) - Confidence: {obj['confidence']:.1%}")
        
        # Step 2: Policy Analysis
        print("\n📋 Step 2: Policy Analysis")
        print("-" * 30)
        
        # Extract rules from policy content
        rules = parser.extract_policy_rules_from_text(policy_content)
        print(f"Extracted {len(rules)} policy rules:")
        
        for i, rule in enumerate(rules[:3], 1):  # Show first 3 rules
            print(f"  {i}. {rule['rule_text'][:80]}...")
        
        # Step 3: Violation Assessment
        print("\n🚨 Step 3: Violation Assessment")
        print("-" * 30)
        
        # Search for relevant rules
        relevant_rules = []
        for obj in detected_objects:
            query = f"{obj['object']} {obj['category']}"
            rules_found = parser.search_relevant_rules(query, n_results=2)
            relevant_rules.extend(rules_found)
        
        # Remove duplicates
        unique_rules = []
        seen_texts = set()
        for rule in relevant_rules:
            if rule["rule_text"] not in seen_texts:
                seen_texts.add(rule["rule_text"])
                unique_rules.append(rule)
        
        # Assess violations
        image_context = detector.analyze_image_context(image_path)
        violation_assessment = checker.assess_violation(detected_objects, unique_rules, image_context)
        
        print(f"Violation Found: {violation_assessment.get('violation_found', False)}")
        print(f"Assessment: {violation_assessment.get('message', 'No message')}")
        print(f"Confidence: {violation_assessment.get('confidence', 0):.1%}")
        print(f"Severity: {violation_assessment.get('severity', 'unknown')}")
        
        # Step 4: Report Generation
        print("\n📄 Step 4: Report Generation")
        print("-" * 30)
        
        if violation_assessment.get('violation_found', False):
            report_path = generator.generate_incident_report(
                image_path=image_path,
                detected_objects=detected_objects,
                violation_assessment=violation_assessment,
                policy_rules=unique_rules,
                user_notes="Demo violation detected during system testing.",
                staff_name="Demo Staff",
                room_number="Demo Room",
                building_name="Demo Building"
            )
            
            print(f"✅ Incident report generated: {os.path.basename(report_path)}")
            print(f"📁 Report saved to: {report_path}")
        else:
            print("ℹ️ No violations detected - no report generated")
        
        # Step 5: Summary
        print("\n📊 Demo Summary")
        print("-" * 30)
        
        summary = {
            "objects_detected": len(detected_objects),
            "policy_rules_extracted": len(rules),
            "relevant_rules_found": len(unique_rules),
            "violation_detected": violation_assessment.get('violation_found', False),
            "assessment_confidence": violation_assessment.get('confidence', 0),
            "report_generated": violation_assessment.get('violation_found', False)
        }
        
        for key, value in summary.items():
            if isinstance(value, float):
                print(f"  {key.replace('_', ' ').title()}: {value:.1%}")
            else:
                print(f"  {key.replace('_', ' ').title()}: {value}")
        
        # Cleanup
        os.unlink(image_path)
        os.unlink(policy_path)
        
        print("\n🎉 Demo completed successfully!")
        print("\n💡 Next steps:")
        print("  1. Set up your OpenAI API key in .env file")
        print("  2. Run 'python run.py --mode streamlit' to start the web interface")
        print("  3. Upload real images and policy documents")
        print("  4. Generate actual incident reports")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("  1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("  2. Check that your OpenAI API key is set in .env file")
        print("  3. Run 'python test_system.py' to check system components")
        return False

def main():
    """Main demo function."""
    print("🚨 AI-Powered Violation Detection System - Demo")
    print("=" * 60)
    print("This demo will showcase the system's capabilities with sample data.")
    print("No real data will be processed or stored.")
    print()
    
    # Check if OpenAI API key is configured
    try:
        from utils.config import config
        if not config.OPENAI_API_KEY or config.OPENAI_API_KEY == "your_openai_api_key_here":
            print("⚠️  Warning: OpenAI API key not configured")
            print("   The demo will run but LLM-based violation assessment may not work properly.")
            print("   Set your API key in .env file for full functionality.")
            print()
    except:
        pass
    
    # Run the demo
    success = run_demo()
    
    if success:
        print("\n✅ Demo completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Demo failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 