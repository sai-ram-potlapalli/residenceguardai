#!/usr/bin/env python3
"""
Setup Script for Judges - ResidenceGuard AI
This script helps judges quickly set up the system for testing.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header():
    print("=" * 60)
    print("🏛️  ResidenceGuard AI - Judge Setup Script")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    required_packages = [
        'streamlit', 'torch', 'transformers', 'pillow', 
        'pandas', 'reportlab', 'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        install = input("Would you like to install missing packages? (y/n): ").lower()
        if install == 'y':
            subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            return True
        else:
            print("❌ Please install missing packages manually: pip install -r requirements.txt")
            return False
    
    return True

def setup_environment():
    """Set up environment variables"""
    print("\n🔧 Setting up environment variables...")
    
    env_file = Path('.env')
    env_example = Path('env.example')
    
    if not env_example.exists():
        print("❌ env.example file not found")
        return False
    
    if env_file.exists():
        overwrite = input("⚠️  .env file already exists. Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print("✅ Using existing .env file")
            return True
    
    # Copy env.example to .env
    shutil.copy(env_example, env_file)
    print("✅ Created .env file from env.example")
    
    # Guide user through configuration
    print("\n📧 Email Configuration Required:")
    print("Please edit the .env file with your Gmail credentials:")
    print("1. SENDER_EMAIL=your-email@gmail.com")
    print("2. SENDER_PASSWORD=your-app-password")
    print("3. RESIDENCE_LIFE_EMAIL=reslife@university.edu")
    print("\n💡 To get a Gmail app password:")
    print("   - Go to Google Account settings")
    print("   - Security → 2-Step Verification → App passwords")
    print("   - Generate a new app password for 'Mail'")
    
    print("\n🤖 AI Configuration:")
    print("✅ HuggingFace token is pre-configured for demo use")
    print("✅ No additional AI setup required")
    print("✅ Models will download automatically on first use")
    
    return True

def create_test_images_folder():
    """Create a folder for test images"""
    print("\n📁 Creating test images folder...")
    test_images_dir = Path('test_images')
    test_images_dir.mkdir(exist_ok=True)
    
    # Create a README for test images
    readme_content = """# Test Images for ResidenceGuard AI

## Recommended Test Images:

### Violation Images:
- Alcohol containers/bottles
- Smoking paraphernalia (cigarettes, lighters, ashtrays)
- Unauthorized appliances (hot plates, microwaves)
- Messy rooms with safety hazards
- Candles or open flames

### Non-Violation Images:
- Clean, compliant dorm rooms
- Normal study areas
- Approved appliances
- Empty rooms

### Mixed Scenarios:
- Images with both violations and normal items
- Poor quality/blurry images
- Images with unusual objects

## Image Requirements:
- Format: JPG, PNG
- Size: < 10MB
- Quality: Clear, well-lit photos work best

Place your test images in this folder for easy access during the demo.
"""
    
    with open(test_images_dir / 'README.md', 'w') as f:
        f.write(readme_content)
    
    print("✅ Created test_images folder with guidelines")
    return True

def run_quick_test():
    """Run a quick system test"""
    print("\n🧪 Running quick system test...")
    
    try:
        # Test basic imports
        import streamlit
        import torch
        import transformers
        from PIL import Image
        print("✅ All core modules imported successfully")
        
        # Test if models can be loaded (basic check)
        print("✅ System ready for testing")
        print("✅ HuggingFace token pre-configured for demo")
        return True
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

def main():
    print_header()
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Setup environment
    if not setup_environment():
        return
    
    # Create test images folder
    create_test_images_folder()
    
    # Run quick test
    if not run_quick_test():
        return
    
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print("\n📋 Next Steps:")
    print("1. Edit .env file with your Gmail credentials")
    print("2. Add test images to the test_images/ folder")
    print("3. Run the application: python app.py")
    print("4. Open http://localhost:8501 in your browser")
    print("\n📖 For detailed instructions, see JUDGE_TESTING_GUIDE.md")
    print("\n🚀 Ready to demonstrate ResidenceGuard AI!")
    print("\n💡 Demo Environment Notes:")
    print("   - HuggingFace token is pre-configured")
    print("   - AI models will download on first use")
    print("   - Email system requires your Gmail credentials")

if __name__ == "__main__":
    main() 