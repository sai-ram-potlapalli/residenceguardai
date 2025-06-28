# Email Setup Guide

## Overview

The AI-Powered Violation Detection System now includes automatic email functionality that sends professional violation reports to the Residence Life office. The emails include:

- **Professional HTML formatting** with violation details
- **Meeting scheduling** with suggested dates
- **Policy violation charges** based on severity
- **PDF report attachment**
- **Immediate action requirements**

## Features

### 📧 Email Content Includes:
1. **Violation Summary** - Severity, confidence, and assessment
2. **Detected Objects** - List of violations found with confidence levels
3. **Policy Rules Violated** - Specific rules that were broken
4. **Meeting Scheduling** - Suggested meeting date (next business day)
5. **Policy Charges** - Standard fee structure:
   - Policy Violation Fee: $50.00
   - Safety Violation Fee: $100.00
   - Repeat Offense: Additional $25.00
   - Documentation Fee: $15.00
6. **Follow-up Actions** - Required steps for Residence Life staff
7. **Contact Information** - Office details and emergency contacts

### 🎯 Professional Communication:
- **Urgent subject lines** with priority levels
- **HTML formatting** with color-coded sections
- **Business-appropriate tone** and language
- **Clear action items** and deadlines
- **Professional branding** and contact information

## Setup Instructions

### 1. Email Configuration

Add the following variables to your `.env` file:

```bash
# Email Configuration
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SENDER_EMAIL=your-email@gmail.com
EMAIL_SENDER_PASSWORD=your-app-password
EMAIL_RESIDENCE_LIFE_EMAIL=reslife@university.edu
```

### 2. Gmail Setup (Recommended)

For Gmail, you'll need to:

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
   - Use this password in `EMAIL_SENDER_PASSWORD`

### 3. Other Email Providers

For other providers, use their SMTP settings:

**Outlook/Hotmail:**
```bash
EMAIL_SMTP_SERVER=smtp-mail.outlook.com
EMAIL_SMTP_PORT=587
```

**Yahoo:**
```bash
EMAIL_SMTP_SERVER=smtp.mail.yahoo.com
EMAIL_SMTP_PORT=587
```

**Custom SMTP:**
```bash
EMAIL_SMTP_SERVER=your-smtp-server.com
EMAIL_SMTP_PORT=587
```

## Usage

### 1. Enable Email in Streamlit

1. Open the Streamlit app
2. In the sidebar, check "Enable Email Notifications"
3. Configure your email settings
4. The system will automatically send emails when reports are generated

### 2. Email Workflow

1. **Upload image and policy document**
2. **Run analysis** to detect violations
3. **Generate report** with PDF
4. **Check "Send Email"** option
5. **Email is automatically sent** to Residence Life office

### 3. Email Preview

The system shows an email preview with:
- Subject line
- Recipient address
- Content summary

## Email Templates

### Subject Line Format:
```
URGENT: Policy Violation - [Building] Room [Number] - [SEVERITY] Priority
```

### Email Structure:
1. **Header** - Professional branding
2. **Violation Summary** - Key details and status
3. **Detected Violations** - List of objects found
4. **Policy Rules** - Specific rules violated
5. **Action Required** - Meeting scheduling and charges
6. **Contact Information** - Office details
7. **Footer** - System information

## Testing

Run the email test script:

```bash
python test_email.py
```

This will verify:
- Email configuration
- Template generation
- Subject line formatting
- Meeting date calculation

## Security Considerations

1. **App Passwords** - Use app-specific passwords, not your main password
2. **Environment Variables** - Never commit email credentials to version control
3. **SMTP Security** - Use TLS/SSL encryption (port 587 or 465)
4. **Access Control** - Limit who can send emails from the system

## Troubleshooting

### Common Issues:

1. **Authentication Failed**
   - Check email and password
   - Verify 2FA is enabled (for Gmail)
   - Use app password, not regular password

2. **SMTP Connection Error**
   - Check SMTP server and port
   - Verify firewall settings
   - Test with different email provider

3. **Email Not Sending**
   - Check internet connection
   - Verify email configuration
   - Check spam/junk folders

### Debug Mode:

Enable debug logging by adding to your `.env`:
```bash
EMAIL_DEBUG=true
```

## Customization

### Modify Email Templates:

Edit `utils/email_sender.py` to customize:
- Email styling and colors
- Fee structure and amounts
- Meeting scheduling logic
- Contact information
- Professional branding

### Add Custom Fields:

Extend the email data structure to include:
- Resident information
- Building-specific policies
- Custom fee schedules
- Department-specific contacts

## Support

For email setup issues:
1. Check the test script output
2. Verify SMTP settings with your email provider
3. Test with a simple email client first
4. Review security settings and app passwords

---

**Note:** This email system is designed for professional use in educational institutions. Ensure compliance with your organization's email policies and data protection regulations. 