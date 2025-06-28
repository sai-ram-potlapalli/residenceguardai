#!/usr/bin/env python3
"""
Test thumbnail creation
"""

import os
from PIL import Image
from utils.helpers import create_thumbnail

def test_thumbnail_creation():
    """Test thumbnail creation with a simple image."""
    # Create a simple test image
    test_image_path = "test_image.jpg"
    
    # Create a simple test image
    img = Image.new('RGB', (800, 600), color='white')
    img.save(test_image_path)
    
    print(f"Created test image: {test_image_path}")
    
    try:
        # Test thumbnail creation
        thumbnail_data = create_thumbnail(test_image_path, max_size=(400, 300))
        
        if thumbnail_data:
            print(f"✅ Thumbnail created successfully! Size: {len(thumbnail_data)} bytes")
            
            # Save thumbnail to verify it works
            with open("test_thumbnail.jpg", "wb") as f:
                f.write(thumbnail_data)
            print("✅ Thumbnail saved as test_thumbnail.jpg")
            
            # Clean up
            os.remove("test_thumbnail.jpg")
        else:
            print("❌ Thumbnail creation failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Clean up test image
        if os.path.exists(test_image_path):
            os.remove(test_image_path)

if __name__ == "__main__":
    test_thumbnail_creation() 