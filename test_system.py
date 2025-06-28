#!/usr/bin/env python3
"""
Test suite for the Violation Detection and Reporting System.
Tests all major components and their integration.
"""

import os
import sys
import tempfile
from PIL import Image
import numpy as np

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_configuration():
    """Test configuration loading."""
    print("🔧 Testing configuration...")
    try:
        from utils.config import config
        # Check if required config attributes exist
        assert hasattr(config, 'OPENAI_API_KEY'), "OPENAI_API_KEY not found in config"
        assert hasattr(config, 'MODEL_NAME'), "MODEL_NAME not found in config"
        print("✅ Configuration test passed")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_helper_functions():
    """Test helper functions."""
    print("🛠️ Testing helper functions...")
    try:
        from utils.helpers import create_upload_folder, generate_report_filename
        from utils.helpers import validate_file_type, sanitize_filename
        
        # Test folder creation
        test_folder = "test_uploads"
        create_upload_folder(test_folder)
        assert os.path.exists(test_folder), "Upload folder not created"
        
        # Test filename generation
        filename = generate_report_filename("test_incident")
        assert "test_incident" in filename, "Filename generation failed"
        assert filename.endswith(".pdf"), "Filename should end with .pdf"
        
        # Test file validation
        assert validate_file_type("test.jpg", [".jpg", ".png"]), "File validation failed"
        assert not validate_file_type("test.txt", [".jpg", ".png"]), "File validation should reject invalid types"
        
        # Test filename sanitization
        sanitized = sanitize_filename("test file (1).jpg")
        assert "test file (1).jpg" == sanitized, "Filename sanitization should preserve safe characters"
        
        # Cleanup
        if os.path.exists(test_folder):
            os.rmdir(test_folder)
            
        print("✅ Helper functions test passed")
        return True
    except Exception as e:
        print(f"❌ Helper functions test failed: {e}")
        return False

def test_object_detection():
    """Test object detection module."""
    print("📷 Testing object detection...")
    try:
        from modules.object_detection import detector
        
        # Create a test image
        test_image_path = create_test_image()
        
        # Use global detector instance
        # Test object detection
        detected_objects = detector.detect_objects(test_image_path, confidence_threshold=0.1)
        
        # Basic validation
        assert isinstance(detected_objects, list), "detect_objects should return a list"
        
        # Test summary generation
        summary = detector.get_detection_summary(detected_objects)
        assert isinstance(summary, dict), "get_detection_summary should return a dict"
        assert "violation_detected" in summary, "Summary should contain violation_detected"
        
        # Test image context analysis
        context = detector.analyze_image_context(test_image_path)
        assert isinstance(context, dict), "analyze_image_context should return a dict"
        
        # Cleanup
        os.remove(test_image_path)
        
        print("✅ Object detection test passed")
        return True
    except Exception as e:
        print(f"❌ Object detection test failed: {e}")
        return False

def test_pdf_parser():
    """Test PDF parser module."""
    print("📄 Testing PDF parser...")
    try:
        from modules.pdf_parser import PDFParser
        
        # Create a test PDF
        test_pdf_path = create_test_pdf()
        
        # Initialize parser
        parser = PDFParser()
        
        # Test PDF parsing
        rules = parser.parse_policy_document(test_pdf_path)
        assert isinstance(rules, list), "parse_policy_document should return a list"
        
        # Test rule search
        search_results = parser.search_relevant_rules("candle", n_results=3)
        assert isinstance(search_results, list), "search_relevant_rules should return a list"
        
        # Test rule extraction
        extracted_rules = parser.extract_rules_from_text("No candles allowed in rooms.")
        assert isinstance(extracted_rules, list), "extract_rules_from_text should return a list"
        
        # Cleanup
        os.remove(test_pdf_path)
        
        print("✅ PDF parser test passed")
        return True
    except Exception as e:
        print(f"❌ PDF parser test failed: {e}")
        return False

def test_violation_checker():
    """Test violation checker module."""
    print("🔍 Testing violation checker...")
    try:
        from modules.violation_checker import ViolationChecker
        
        # Create mock data
        detected_objects = [
            {"object": "candle", "confidence": 0.8, "category": "Fire Hazard"}
        ]
        
        policy_rules = [
            {"rule_text": "No candles or open flames allowed in residence halls."}
        ]
        
        # Initialize checker (with mock API key if needed)
        os.environ['OPENAI_API_KEY'] = 'test_key'  # Mock key for testing
        checker = ViolationChecker()
        
        # Test violation assessment
        assessment = checker.assess_violation(detected_objects, policy_rules)
        assert isinstance(assessment, dict), "assess_violation should return a dict"
        assert "violation_found" in assessment, "Assessment should contain violation_found"
        
        # Test summary generation
        summary = checker.get_violation_summary(assessment)
        assert isinstance(summary, str), "get_violation_summary should return a string"
        
        print("✅ Violation checker test passed")
        return True
    except Exception as e:
        print(f"❌ Violation checker test failed: {e}")
        return False

def test_report_generator():
    """Test report generator module."""
    print("📋 Testing report generator...")
    try:
        from modules.report_generator import ReportGenerator
        
        # Create test data
        incident_data = {
            "incident_id": "TEST-001",
            "date": "2024-01-15",
            "location": "Room 101",
            "violation_type": "Fire Hazard",
            "description": "Candle detected in room",
            "severity": "Medium",
            "action_taken": "Warning issued"
        }
        
        # Initialize generator
        generator = ReportGenerator()
        
        # Test report generation
        report_path = generator.generate_incident_report_simple(incident_data)
        assert os.path.exists(report_path), "Report file should be created"
        assert report_path.endswith(".pdf"), "Report should be a PDF file"
        
        # Test template rendering
        html_content = generator.render_template(incident_data)
        assert isinstance(html_content, str), "Template rendering should return a string"
        assert "TEST-001" in html_content, "Template should contain incident data"
        
        # Cleanup
        os.remove(report_path)
        
        print("✅ Report generator test passed")
        return True
    except Exception as e:
        print(f"❌ Report generator test failed: {e}")
        return False

def test_integration():
    """Test component integration."""
    print("🔗 Testing component integration...")
    try:
        from modules.object_detection import detector
        from modules.pdf_parser import parser
        from modules.violation_checker import ViolationChecker
        from modules.report_generator import ReportGenerator
        
        # Create test files
        test_image_path = create_test_image()
        test_pdf_path = create_test_pdf()
        
        # Test full workflow
        # 1. Object detection
        detected_objects = detector.detect_objects(test_image_path)
        
        # 2. Policy parsing
        policy_rules = parser.parse_policy_document(test_pdf_path)
        
        # 3. Violation assessment
        os.environ['OPENAI_API_KEY'] = 'test_key'  # Mock key
        checker = ViolationChecker()
        assessment = checker.assess_violation(detected_objects, policy_rules)
        
        # 4. Report generation (if violation found)
        if assessment.get("violation_found", False):
            generator = ReportGenerator()
            incident_data = {
                "incident_id": "INTEGRATION-TEST-001",
                "date": "2024-01-15",
                "location": "Test Room",
                "violation_type": assessment.get("severity", "Unknown"),
                "description": assessment.get("message", "Test violation"),
                "severity": assessment.get("severity", "Medium"),
                "action_taken": assessment.get("recommended_action", "Review required")
            }
            report_path = generator.generate_incident_report_simple(incident_data)
            
            # Cleanup report
            if os.path.exists(report_path):
                os.remove(report_path)
        
        # Cleanup test files
        os.remove(test_image_path)
        os.remove(test_pdf_path)
        
        print("✅ Integration test passed")
        return True
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def create_test_image():
    """Create a test image for testing."""
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='white')
    test_path = "test_image.jpg"
    img.save(test_path)
    return test_path

def create_test_pdf():
    """Create a test PDF for testing."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        test_path = "test_policy.pdf"
        c = canvas.Canvas(test_path, pagesize=letter)
        c.drawString(100, 750, "Sample Housing Policy")
        c.drawString(100, 700, "No candles or open flames allowed in residence halls.")
        c.drawString(100, 650, "No pets allowed without proper documentation.")
        c.drawString(100, 600, "No unauthorized appliances in rooms.")
        c.save()
        return test_path
    except ImportError:
        # Fallback: create a text file
        test_path = "test_policy.txt"
        with open(test_path, 'w') as f:
            f.write("Sample Housing Policy\n")
            f.write("No candles or open flames allowed in residence halls.\n")
            f.write("No pets allowed without proper documentation.\n")
            f.write("No unauthorized appliances in rooms.\n")
        return test_path

def main():
    """Run all tests."""
    print("🧪 Starting Violation Detection System Tests")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Helper Functions", test_helper_functions),
        ("Object Detection", test_object_detection),
        ("PDF Parser", test_pdf_parser),
        ("Violation Checker", test_violation_checker),
        ("Report Generator", test_report_generator),
        ("Integration", test_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📝 Running {test_name} test...")
        try:
            if test_func():
                passed += 1
            else:
                print(f"⚠️ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test failed: {e}")
            print(f"⚠️ {test_name} test failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! System is ready to use.")
    else:
        print("❌ Some tests failed. Please check the configuration and dependencies.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 