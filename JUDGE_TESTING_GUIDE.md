# 🏛️ Judge Testing Guide - ResidenceGuard AI

## 📋 Pre-Testing Requirements

### 🖥️ **System Requirements**
- **Operating System**: macOS, Windows, or Linux
- **Python**: Version 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: At least 2GB free space
- **Internet Connection**: Required for initial setup and model downloads

### 📧 **Email Setup (Required for Full Demo)**
- **Gmail Account**: For sending emails (Residence Life reports + Resident notifications)
- **App Password**: Generated from Gmail security settings
- **Environment Variables**: Will be configured during setup

### 🤖 **AI Configuration (Pre-configured)**
- **HuggingFace Token**: Pre-configured for demo use (developer's token)
- **Rate Limits**: Free tier sufficient for testing
- **Models**: CLIP for object detection, HuggingFace LLM for violation assessment

### 📱 **Test Images**
- **Violation Images**: Photos showing potential housing violations
  - Alcohol containers/bottles
  - Smoking paraphernalia
  - Unauthorized appliances
  - Messy rooms
  - Safety hazards
- **Non-Violation Images**: Photos showing compliant rooms
- **Mixed Scenarios**: Images with both violations and normal items

## 🚀 Setup Instructions for Judges

### 1. **Clone/Download the Repository**
```bash
git clone <repository-url>
cd "Violation Detection and Reporting System"
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Configure Email Settings**
1. Copy `env.example` to `.env`
2. Add your Gmail credentials:
   ```
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=your-app-password
   RESIDENCE_LIFE_EMAIL=reslife@university.edu
   ```
3. **Note**: HuggingFace token is pre-configured for demo use

### 4. **Run the Application**
```bash
python app.py
```

## 🧪 Testing Scenarios

### **Scenario 1: Basic Violation Detection**
**Objective**: Test core AI detection capabilities
- Upload image with clear violations (alcohol, smoking items)
- Verify object detection accuracy (CLIP model)
- Check violation assessment quality (HuggingFace LLM)
- Review policy rule matching

### **Scenario 2: Resident Notification System**
**Objective**: Test dual email functionality
- Enter resident information (name + email)
- Enable resident notification checkbox
- Send report to Residence Life
- Verify both emails are sent successfully
- Check email content quality

### **Scenario 3: Edge Cases**
**Objective**: Test system robustness
- Upload image with no violations
- Test with poor quality/blurry images
- Try images with multiple violation types
- Test with unusual objects

### **Scenario 4: Report Generation**
**Objective**: Test professional report output
- Generate incident report
- Review PDF format and content
- Check all required fields are included
- Verify professional formatting

## 📊 Evaluation Criteria

### **Technical Performance**
- [ ] Object detection accuracy (CLIP model)
- [ ] Violation assessment quality (HuggingFace LLM)
- [ ] Policy rule relevance
- [ ] System response time
- [ ] Error handling

### **User Experience**
- [ ] Interface intuitiveness
- [ ] Workflow efficiency
- [ ] Data validation
- [ ] Success/error messaging
- [ ] Professional appearance

### **Email Functionality**
- [ ] Email delivery success
- [ ] Content quality and formatting
- [ ] Attachment handling
- [ ] Dual email system (Residence Life + Resident)
- [ ] Professional tone and structure

### **Report Quality**
- [ ] PDF generation
- [ ] Content completeness
- [ ] Professional formatting
- [ ] Required information inclusion
- [ ] Download functionality

## 🔧 Troubleshooting

### **Common Issues**
1. **Email Not Sending**
   - Check Gmail app password
   - Verify environment variables
   - Check internet connection

2. **AI Models Not Loading**
   - Ensure sufficient RAM (4GB+)
   - Check internet connection for model downloads
   - HuggingFace token is pre-configured for demo
   - Restart application if needed

3. **Image Upload Problems**
   - Check file format (JPG, PNG)
   - Verify file size (< 10MB)
   - Try different images

### **Support Files Available**
- `test_email_functionality.py` - Test email system
- `test_resident_notification.py` - Test resident notifications
- `debug_email.py` - Email debugging tools
- `test_system.py` - Full system testing

## 📝 Demo Script Suggestions

### **Opening (2 minutes)**
- "Welcome to ResidenceGuard AI - an intelligent violation detection and reporting system"
- "This system uses AI to automatically detect housing violations and generate professional reports"
- "The AI is powered by HuggingFace models for object detection and violation assessment"
- "Let me show you how it streamlines the entire process from detection to notification"

### **Core Demo (5-7 minutes)**
1. **Upload and Analysis** (2 min)
   - Upload violation image
   - Show detected objects and confidence scores (CLIP model)
   - Highlight violation assessment (HuggingFace LLM)

2. **Resident Notification** (2 min)
   - Enter resident details
   - Enable notification
   - Send both emails

3. **Report Review** (1 min)
   - Show generated PDF
   - Highlight professional formatting
   - Demonstrate download

### **Closing (1 minute)**
- "The system handles the entire workflow automatically"
- "Residence Life gets professional reports, residents get immediate notifications"
- "This reduces manual work and ensures consistent, timely communication"
- "In production, each institution would use their own AI tokens and email systems"

## 🎯 Key Features to Highlight

### **AI-Powered Detection**
- CLIP model for object recognition
- HuggingFace LLM for violation assessment
- PDF policy parsing and matching

### **Dual Email System**
- Professional reports to Residence Life
- Immediate notifications to residents
- Automated workflow

### **Professional Output**
- PDF report generation
- Consistent formatting
- Complete documentation

### **User-Friendly Interface**
- Streamlit-based web interface
- Intuitive workflow
- Real-time feedback

## 🔧 Demo Environment Configuration

### **HuggingFace Token**
- **Status**: Pre-configured for demo use
- **Source**: Developer's personal token
- **Usage**: AI processing (object detection + violation assessment)
- **Limits**: Free tier sufficient for testing
- **Production**: Each institution would use their own token

### **Email System**
- **Configuration**: Judges provide their own Gmail credentials
- **Authentication**: App password required
- **Testing**: Real emails sent to actual addresses
- **Production**: Institution's email system

## 📞 Support During Demo

If technical issues arise during the demo:
1. Check the console output for error messages
2. Use the test scripts in the `utils/` folder
3. Restart the application if needed
4. Have backup images ready
5. Monitor HuggingFace usage if needed

---

**Remember**: The goal is to demonstrate how this system transforms a manual, time-consuming process into an automated, efficient workflow that benefits both staff and residents. The demo environment uses pre-configured AI tokens for simplicity, but production deployments would use institution-specific configurations. 