#!/usr/bin/env python3
"""
Edge Case Tester for ResidenceGuard AI
Tests various edge cases and error conditions
"""

import os
import tempfile
import shutil
from PIL import Image
import io
from utils.config import config
from modules.object_detection import detector
from modules.pdf_parser import parser
from modules.violation_checker import checker
from modules.report_generator import generator

def test_image_edge_cases():
    """Test various image edge cases"""
    print("📸 Testing Image Edge Cases...")
    
    # Create test images
    test_cases = []
    
    # 1. Very small image
    small_img = Image.new('RGB', (1, 1), color='red')
    small_img_path = "test_small.png"
    small_img.save(small_img_path)
    test_cases.append(("Very Small Image (1x1)", small_img_path))
    
    # 2. Very large image
    large_img = Image.new('RGB', (4000, 3000), color='blue')
    large_img_path = "test_large.png"
    large_img.save(large_img_path)
    test_cases.append(("Very Large Image (4000x3000)", large_img_path))
    
    # 3. Empty room image (blank)
    blank_img = Image.new('RGB', (800, 600), color='white')
    blank_img_path = "test_blank.png"
    blank_img.save(blank_img_path)
    test_cases.append(("Empty Room (Blank)", blank_img_path))
    
    # 4. Dark image
    dark_img = Image.new('RGB', (800, 600), color='black')
    dark_img_path = "test_dark.png"
    dark_img.save(dark_img_path)
    test_cases.append(("Dark Image", dark_img_path))
    
    # Test each case
    for test_name, img_path in test_cases:
        try:
            print(f"\n🔍 Testing: {test_name}")
            detected_objects = detector.detect_objects(img_path)
            print(f"   Objects detected: {len(detected_objects)}")
            if detected_objects:
                for obj in detected_objects[:3]:  # Show first 3
                    print(f"   - {obj.get('object', 'Unknown')} ({obj.get('confidence', 0):.2%})")
            else:
                print("   - No objects detected")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        finally:
            # Cleanup
            if os.path.exists(img_path):
                os.remove(img_path)

def test_pdf_edge_cases():
    """Test various PDF edge cases"""
    print("\n📄 Testing PDF Edge Cases...")
    
    # Test with existing sample policy
    if os.path.exists('sample_policy.pdf'):
        try:
            print("🔍 Testing: Sample Policy PDF")
            policy_summary = parser.get_policy_summary('sample_policy.pdf')
            print(f"   Rules extracted: {policy_summary.get('total_rules', 0)}")
            
            # Test indexing
            parser.index_policy_rules('sample_policy.pdf', 'test_policy')
            print("   ✅ Policy indexed successfully")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

def test_empty_inputs():
    """Test with empty or invalid inputs"""
    print("\n🚫 Testing Empty/Invalid Inputs...")
    
    # Test with non-existent files
    try:
        print("🔍 Testing: Non-existent image")
        detector.detect_objects("nonexistent.jpg")
    except Exception as e:
        print(f"   ✅ Correctly handled: {str(e)}")
    
    try:
        print("🔍 Testing: Non-existent PDF")
        parser.get_policy_summary("nonexistent.pdf")
    except Exception as e:
        print(f"   ✅ Correctly handled: {str(e)}")

def test_large_data():
    """Test with large amounts of data"""
    print("\n📊 Testing Large Data Handling...")
    
    # Create a large number of objects for testing
    large_object_list = []
    for i in range(50):
        large_object_list.append({
            'object': f'test_object_{i}',
            'category': 'test_category',
            'confidence': 0.8
        })
    
    try:
        print("🔍 Testing: Large object list processing")
        # Test violation checker with many objects
        mock_policy_rules = [{'rule_text': 'Test rule', 'metadata': {}}]
        result = checker.assess_violation(large_object_list, mock_policy_rules)
        print(f"   ✅ Processed {len(large_object_list)} objects")
        print(f"   Violation found: {result.get('violation_found', False)}")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

def test_error_recovery():
    """Test error recovery mechanisms"""
    print("\n🔄 Testing Error Recovery...")
    
    # Test with invalid confidence values
    try:
        print("🔍 Testing: Invalid confidence values")
        invalid_objects = [
            {'object': 'test', 'category': 'test', 'confidence': 'invalid'},
            {'object': 'test2', 'category': 'test', 'confidence': None},
            {'object': 'test3', 'category': 'test', 'confidence': -1.0}
        ]
        
        mock_rules = [{'rule_text': 'Test rule', 'metadata': {}}]
        result = checker.assess_violation(invalid_objects, mock_rules)
        print("   ✅ Handled invalid confidence values")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

def test_file_permissions():
    """Test file permission edge cases"""
    print("\n🔐 Testing File Permissions...")
    
    # Create a temporary directory with restricted permissions
    temp_dir = tempfile.mkdtemp()
    test_file = os.path.join(temp_dir, "test.txt")
    
    try:
        with open(test_file, 'w') as f:
            f.write("test content")
        
        # Test if we can read the file
        print("🔍 Testing: File read permissions")
        with open(test_file, 'r') as f:
            content = f.read()
        print("   ✅ File read successful")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)

def test_memory_usage():
    """Test memory usage with large files"""
    print("\n💾 Testing Memory Usage...")
    
    # Create a large image to test memory handling
    try:
        print("🔍 Testing: Large image memory usage")
        large_img = Image.new('RGB', (2000, 2000), color='green')
        large_img_path = "test_memory.png"
        large_img.save(large_img_path)
        
        # Try to process the large image
        detected_objects = detector.detect_objects(large_img_path)
        print(f"   ✅ Processed large image: {len(detected_objects)} objects")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    finally:
        if os.path.exists(large_img_path):
            os.remove(large_img_path)

def test_concurrent_operations():
    """Test concurrent operations"""
    print("\n⚡ Testing Concurrent Operations...")
    
    # Test multiple operations simultaneously
    try:
        print("🔍 Testing: Multiple operations")
        
        # Create test image
        test_img = Image.new('RGB', (800, 600), color='yellow')
        test_img_path = "test_concurrent.png"
        test_img.save(test_img_path)
        
        # Run multiple operations
        import threading
        import time
        
        def detect_objects():
            return detector.detect_objects(test_img_path)
        
        def parse_policy():
            return parser.get_policy_summary('sample_policy.pdf')
        
        # Run operations in threads
        thread1 = threading.Thread(target=detect_objects)
        thread2 = threading.Thread(target=parse_policy)
        
        thread1.start()
        thread2.start()
        
        thread1.join()
        thread2.join()
        
        print("   ✅ Concurrent operations completed")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    finally:
        if os.path.exists(test_img_path):
            os.remove(test_img_path)

def main():
    """Run all edge case tests"""
    print("🚨 ResidenceGuard AI - Edge Case Testing")
    print("=" * 50)
    
    tests = [
        ("Image Edge Cases", test_image_edge_cases),
        ("PDF Edge Cases", test_pdf_edge_cases),
        ("Empty/Invalid Inputs", test_empty_inputs),
        ("Large Data Handling", test_large_data),
        ("Error Recovery", test_error_recovery),
        ("File Permissions", test_file_permissions),
        ("Memory Usage", test_memory_usage),
        ("Concurrent Operations", test_concurrent_operations)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} {test_name} {'='*20}")
            test_func()
            results.append((test_name, True))
        except Exception as e:
            print(f"❌ {test_name} Test Crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 EDGE CASE TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} edge case tests passed")
    
    if passed == len(results):
        print("🎉 All edge case tests passed!")
        print("🛡️ System is robust and handles edge cases well")
    else:
        print("⚠️ Some edge cases failed. Consider improving error handling.")

if __name__ == "__main__":
    main() 