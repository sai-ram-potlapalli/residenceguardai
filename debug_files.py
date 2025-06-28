#!/usr/bin/env python3
"""
Debug script to test file validation
"""

import os
import sys
from PIL import Image
import fitz  # PyMuPDF

def test_image_validation(file_path):
    """Test image validation with detailed error reporting."""
    print(f"Testing image: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ File does not exist: {file_path}")
        return False
    
    try:
        # Test with PIL
        with Image.open(file_path) as img:
            print(f"✅ PIL can open the image")
            print(f"   Format: {img.format}")
            print(f"   Mode: {img.mode}")
            print(f"   Size: {img.size}")
            
            # Try to verify (this is what the validation function does)
            img.verify()
            print(f"✅ Image verification passed")
            return True
            
    except Exception as e:
        print(f"❌ Image validation failed: {e}")
        return False

def test_pdf_validation(file_path):
    """Test PDF validation with detailed error reporting."""
    print(f"Testing PDF: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ File does not exist: {file_path}")
        return False
    
    try:
        # Test with PyMuPDF
        doc = fitz.open(file_path)
        print(f"✅ PyMuPDF can open the PDF")
        print(f"   Pages: {len(doc)}")
        print(f"   Metadata: {doc.metadata}")
        doc.close()
        
        # Test header check
        with open(file_path, 'rb') as f:
            header = f.read(4)
            if header == b'%PDF':
                print(f"✅ PDF header check passed")
                return True
            else:
                print(f"❌ PDF header check failed: {header}")
                return False
                
    except Exception as e:
        print(f"❌ PDF validation failed: {e}")
        return False

def main():
    """Test files in uploads directory."""
    uploads_dir = "uploads"
    
    if not os.path.exists(uploads_dir):
        print(f"❌ Uploads directory does not exist: {uploads_dir}")
        return
    
    files = os.listdir(uploads_dir)
    if not files:
        print(f"❌ No files found in uploads directory")
        return
    
    print(f"Found {len(files)} files in uploads directory:")
    
    for filename in files:
        file_path = os.path.join(uploads_dir, filename)
        print(f"\n{'='*50}")
        print(f"File: {filename}")
        
        # Check file extension
        _, ext = os.path.splitext(filename.lower())
        print(f"Extension: {ext}")
        
        # Test based on file type
        if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']:
            test_image_validation(file_path)
        elif ext == '.pdf':
            test_pdf_validation(file_path)
        else:
            print(f"❌ Unknown file type: {ext}")

if __name__ == "__main__":
    main() 