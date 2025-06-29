#!/usr/bin/env python3
"""
Deployment Helper Script for ResidenceGuard AI
Checks if the project is ready for Streamlit Cloud deployment.
"""

import os
import sys
from pathlib import Path

def print_header():
    print("=" * 60)
    print("🚀 ResidenceGuard AI - Deployment Check")
    print("=" * 60)
    print()

def check_requirements():
    """Check if requirements.txt exists and is valid"""
    print("📦 Checking requirements.txt...")
    
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found")
        return False
    
    with open("requirements.txt", "r") as f:
        requirements = f.read()
    
    # Check for essential packages
    essential_packages = [
        "streamlit",
        "transformers", 
        "torch",
        "Pillow",
        "PyMuPDF",
        "chromadb"
    ]
    
    missing_packages = []
    for package in essential_packages:
        if package not in requirements:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing essential packages: {', '.join(missing_packages)}")
        return False
    
    print("✅ requirements.txt is valid")
    return True

def check_main_app():
    """Check if main app file exists"""
    print("\n📱 Checking main application...")
    
    if not Path("app.py").exists():
        print("❌ app.py not found")
        return False
    
    print("✅ app.py found")
    return True

def check_streamlit_config():
    """Check Streamlit configuration"""
    print("\n⚙️ Checking Streamlit configuration...")
    
    config_path = Path(".streamlit/config.toml")
    if not config_path.exists():
        print("❌ .streamlit/config.toml not found")
        return False
    
    print("✅ Streamlit configuration found")
    return True

def check_environment_variables():
    """Check environment variables setup"""
    print("\n🔧 Checking environment variables...")
    
    env_example = Path("env.example")
    if not env_example.exists():
        print("❌ env.example not found")
        return False
    
    print("✅ env.example found")
    print("💡 Remember to set environment variables in Streamlit Cloud:")
    print("   - HUGGINGFACE_TOKEN")
    print("   - SENDER_EMAIL")
    print("   - SENDER_PASSWORD")
    print("   - RESIDENCE_LIFE_EMAIL")
    
    return True

def check_git_status():
    """Check if repository is ready for deployment"""
    print("\n📋 Checking Git repository...")
    
    try:
        import subprocess
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            print("⚠️  Uncommitted changes detected")
            print("   Consider committing changes before deployment")
            return False
        else:
            print("✅ Repository is clean")
            return True
            
    except Exception as e:
        print(f"⚠️  Could not check Git status: {e}")
        return True  # Don't fail deployment for this

def generate_deployment_instructions():
    """Generate deployment instructions"""
    print("\n" + "=" * 60)
    print("📋 Deployment Instructions")
    print("=" * 60)
    
    print("\n1. 🚀 Deploy to Streamlit Cloud:")
    print("   - Go to: https://share.streamlit.io")
    print("   - Sign up with GitHub account")
    print("   - Click 'New app'")
    print("   - Select your repository")
    print("   - Set main file path: app.py")
    print("   - Click 'Deploy'")
    
    print("\n2. 🔧 Configure Environment Variables:")
    print("   In Streamlit Cloud dashboard:")
    print("   - HUGGINGFACE_TOKEN = your_huggingface_token")
    print("   - SENDER_EMAIL = demo_email@gmail.com")
    print("   - SENDER_PASSWORD = your_app_password")
    print("   - RESIDENCE_LIFE_EMAIL = reslife@university.edu")
    
    print("\n3. 🧪 Test Deployment:")
    print("   - Access your app at: https://your-app-name.streamlit.app")
    print("   - Test image upload and analysis")
    print("   - Verify email functionality")
    print("   - Check all features work correctly")
    
    print("\n4. 📧 Share with Judges:")
    print("   - Provide the Streamlit Cloud URL")
    print("   - Include test images and documentation")
    print("   - Share JUDGE_QUICK_START.md")
    print("   - Provide demo credentials")

def main():
    print_header()
    
    checks = [
        check_requirements(),
        check_main_app(),
        check_streamlit_config(),
        check_environment_variables(),
        check_git_status()
    ]
    
    if all(checks):
        print("\n🎉 All checks passed! Your project is ready for deployment.")
        generate_deployment_instructions()
    else:
        print("\n❌ Some checks failed. Please fix the issues before deploying.")
        print("\n💡 Common fixes:")
        print("   - Ensure all required files exist")
        print("   - Check requirements.txt includes all dependencies")
        print("   - Verify environment variables are set up")
        print("   - Commit any uncommitted changes")

if __name__ == "__main__":
    main() 