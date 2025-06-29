#!/usr/bin/env python3
"""
Streamlit Debug Tool for ResidenceGuard AI
This tool helps diagnose configuration and email issues on Streamlit Cloud.
"""

import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.config import config
from utils.email_sender import email_sender

def main():
    st.set_page_config(
        page_title="ResidenceGuard AI - Debug Tool",
        page_icon="🔧",
        layout="wide"
    )
    
    st.title("🔧 ResidenceGuard AI - Debug Tool")
    st.markdown("This tool helps diagnose configuration and email issues on Streamlit Cloud.")
    
    # Configuration Check
    st.header("📋 Configuration Check")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Environment Variables")
        
        # Check each environment variable
        env_vars = {
            "HUGGINGFACE_API_TOKEN": os.getenv('HUGGINGFACE_API_TOKEN'),
            "EMAIL_SMTP_SERVER": os.getenv('EMAIL_SMTP_SERVER'),
            "EMAIL_SMTP_PORT": os.getenv('EMAIL_SMTP_PORT'),
            "EMAIL_SENDER_EMAIL": os.getenv('EMAIL_SENDER_EMAIL'),
            "EMAIL_SENDER_PASSWORD": os.getenv('EMAIL_SENDER_PASSWORD'),
            "EMAIL_RESIDENCE_LIFE_EMAIL": os.getenv('EMAIL_RESIDENCE_LIFE_EMAIL'),
        }
        
        for var_name, var_value in env_vars.items():
            if var_value:
                if 'PASSWORD' in var_name:
                    st.success(f"✅ {var_name}: {'*' * len(var_value)}")
                else:
                    st.success(f"✅ {var_name}: {var_value}")
            else:
                st.error(f"❌ {var_name}: NOT SET")
    
    with col2:
        st.subheader("Config Object Values")
        
        # Check config object values
        config_values = {
            "HUGGINGFACE_API_TOKEN": config.HUGGINGFACE_API_TOKEN,
            "EMAIL_HOST": config.EMAIL_HOST,
            "EMAIL_PORT": config.EMAIL_PORT,
            "EMAIL_USER": config.EMAIL_USER,
            "EMAIL_PASSWORD": config.EMAIL_PASSWORD,
            "RESIDENCE_LIFE_EMAIL": config.RESIDENCE_LIFE_EMAIL,
        }
        
        for var_name, var_value in config_values.items():
            if var_value:
                if 'PASSWORD' in var_name:
                    st.success(f"✅ {var_name}: {'*' * len(var_value)}")
                else:
                    st.success(f"✅ {var_name}: {var_value}")
            else:
                st.error(f"❌ {var_name}: NOT SET")
    
    # Email Sender Check
    st.header("📧 Email Sender Check")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("EmailSender Configuration")
        
        email_config = email_sender.get_email_config()
        for key, value in email_config.items():
            if 'password' in key.lower():
                st.info(f"🔐 {key}: {'*' * len(value) if value else 'NOT SET'}")
            else:
                st.info(f"📧 {key}: {value}")
    
    with col2:
        st.subheader("Email Configuration Status")
        
        # Check if email configuration is complete
        if email_sender.sender_email and email_sender.sender_password:
            st.success("✅ Email configuration appears complete")
        else:
            st.error("❌ Email configuration incomplete")
            if not email_sender.sender_email:
                st.error("Missing sender email")
            if not email_sender.sender_password:
                st.error("Missing sender password")
    
    # SMTP Connection Test
    st.header("🔌 SMTP Connection Test")
    
    if st.button("🧪 Test SMTP Connection", type="primary"):
        with st.spinner("Testing SMTP connection..."):
            try:
                # Test SMTP connection
                st.info(f"Connecting to {email_sender.smtp_server}:{email_sender.smtp_port}...")
                
                server = smtplib.SMTP(email_sender.smtp_server, email_sender.smtp_port)
                st.success("✅ SMTP connection established")
                
                server.starttls()
                st.success("✅ TLS started")
                
                st.info("Attempting login...")
                server.login(email_sender.sender_email, email_sender.sender_password)
                st.success("✅ Login successful!")
                
                server.quit()
                st.success("✅ SMTP test completed successfully!")
                
            except smtplib.SMTPAuthenticationError as e:
                st.error(f"❌ Authentication failed: {e}")
                st.warning("💡 This usually means:")
                st.markdown("""
                - Email or password is incorrect
                - 2-Factor Authentication is enabled but no App Password is used
                - Gmail security settings need to be adjusted
                """)
                
            except smtplib.SMTPException as e:
                st.error(f"❌ SMTP error: {e}")
                
            except Exception as e:
                st.error(f"❌ Connection error: {e}")
    
    # Test Email Send
    st.header("📤 Test Email Send")
    
    if st.button("📧 Send Test Email", type="secondary"):
        with st.spinner("Sending test email..."):
            try:
                # Create test email
                msg = MIMEMultipart()
                msg['From'] = email_sender.sender_email
                msg['To'] = email_sender.residence_life_email
                msg['Subject'] = "Test Email - ResidenceGuard AI Debug Tool"
                
                body = f"""
                This is a test email from the ResidenceGuard AI Debug Tool.
                
                Configuration Details:
                - SMTP Server: {email_sender.smtp_server}
                - SMTP Port: {email_sender.smtp_port}
                - Sender: {email_sender.sender_email}
                - Recipient: {email_sender.residence_life_email}
                
                If you receive this email, your email configuration is working correctly!
                """
                
                msg.attach(MIMEText(body, 'plain'))
                
                # Send email
                server = smtplib.SMTP(email_sender.smtp_server, email_sender.smtp_port)
                server.starttls()
                server.login(email_sender.sender_email, email_sender.sender_password)
                
                text = msg.as_string()
                server.sendmail(email_sender.sender_email, email_sender.residence_life_email, text)
                server.quit()
                
                st.success("✅ Test email sent successfully!")
                st.info(f"📧 Check your inbox at: {email_sender.residence_life_email}")
                
            except Exception as e:
                st.error(f"❌ Failed to send test email: {e}")
    
    # System Information
    st.header("💻 System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Python Environment")
        st.code(f"""
Python Version: {os.sys.version}
Platform: {os.sys.platform}
Working Directory: {os.getcwd()}
        """)
    
    with col2:
        st.subheader("File System")
        
        # Check if important directories exist
        directories = ["reports", "uploads", "chroma_db"]
        for directory in directories:
            if os.path.exists(directory):
                st.success(f"✅ {directory}/ directory exists")
            else:
                st.warning(f"⚠️ {directory}/ directory missing")
        
        # Check if important files exist
        files = ["sample_policy.pdf", "requirements.txt"]
        for file in files:
            if os.path.exists(file):
                st.success(f"✅ {file} exists")
            else:
                st.warning(f"⚠️ {file} missing")
    
    # Troubleshooting Guide
    st.header("🔍 Troubleshooting Guide")
    
    with st.expander("Email Configuration Issues", expanded=False):
        st.markdown("""
        ### Common Email Issues:
        
        **1. Authentication Failed**
        - Check your email and password are correct
        - If using Gmail, make sure you're using an App Password
        - Enable 2-Factor Authentication and generate an App Password
        
        **2. Connection Refused**
        - Check firewall settings
        - Verify SMTP server and port are correct
        - Try different ports (587, 465, 25)
        
        **3. Environment Variables Not Loading**
        - Check variable names match exactly (case-sensitive)
        - Restart the Streamlit app after changing variables
        - Use Streamlit secrets instead of environment variables
        
        **4. Gmail Specific Issues**
        - Enable "Less secure app access" (not recommended)
        - Use App Passwords instead of regular password
        - Check Gmail account security settings
        """)
    
    with st.expander("Streamlit Cloud Setup", expanded=False):
        st.markdown("""
        ### Setting up on Streamlit Cloud:
        
        **1. Environment Variables**
        Go to your app settings and add these secrets:
        ```
        EMAIL_SMTP_SERVER = "smtp.gmail.com"
        EMAIL_SMTP_PORT = "587"
        EMAIL_SENDER_EMAIL = "your-email@gmail.com"
        EMAIL_SENDER_PASSWORD = "your-app-password"
        EMAIL_RESIDENCE_LIFE_EMAIL = "reslife@university.edu"
        HUGGINGFACE_API_TOKEN = "your-huggingface-token"
        ```
        
        **2. Gmail App Password Setup**
        1. Go to your Google Account settings
        2. Enable 2-Factor Authentication
        3. Generate an App Password for "Mail"
        4. Use the 16-character app password
        
        **3. Deploy**
        1. Push your code to GitHub
        2. Connect your repository to Streamlit Cloud
        3. Set the secrets in the app settings
        4. Deploy the app
        """)

if __name__ == "__main__":
    main() 