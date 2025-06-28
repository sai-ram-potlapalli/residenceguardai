#!/usr/bin/env python3
"""
Test script to verify object detection can detect general objects
"""

from PIL import Image
from modules.object_detection import detector

def test_flower_detection():
    """Test if the system can detect flowers and other general objects"""
    print("🌸 Testing Flower/Object Detection...")
    
    # Create a simple test image with flowers
    # Create a colorful image that might represent flowers
    img = Image.new('RGB', (800, 600), color='pink')
    test_image_path = "test_flowers.png"
    img.save(test_image_path)
    
    try:
        print("🔍 Testing object detection on flower-like image...")
        detected_objects = detector.detect_objects(test_image_path, confidence_threshold=0.1)
        
        print(f"📊 Objects detected: {len(detected_objects)}")
        
        if detected_objects:
            print("✅ Objects found:")
            for i, obj in enumerate(detected_objects[:5], 1):  # Show first 5
                print(f"   {i}. {obj['object']} ({obj['category']}) - {obj['confidence']:.2%}")
        else:
            print("❌ No objects detected")
            
        # Test with different confidence thresholds
        print("\n🔍 Testing with different confidence thresholds...")
        for threshold in [0.05, 0.1, 0.2, 0.3]:
            objects = detector.detect_objects(test_image_path, confidence_threshold=threshold)
            print(f"   Threshold {threshold}: {len(objects)} objects")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        # Cleanup
        if os.path.exists(test_image_path):
            os.remove(test_image_path)

def test_general_objects():
    """Test detection of various general objects"""
    print("\n🏠 Testing General Object Detection...")
    
    # Test with a room-like image
    img = Image.new('RGB', (800, 600), color='beige')
    test_image_path = "test_room.png"
    img.save(test_image_path)
    
    try:
        detected_objects = detector.detect_objects(test_image_path, confidence_threshold=0.1)
        
        print(f"📊 Objects detected: {len(detected_objects)}")
        
        if detected_objects:
            print("✅ Objects found:")
            for i, obj in enumerate(detected_objects[:10], 1):  # Show first 10
                print(f"   {i}. {obj['object']} ({obj['category']}) - {obj['confidence']:.2%}")
        else:
            print("❌ No objects detected")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        # Cleanup
        if os.path.exists(test_image_path):
            os.remove(test_image_path)

if __name__ == "__main__":
    import os
    test_flower_detection()
    test_general_objects()
    print("\n🎉 Object detection test completed!") 