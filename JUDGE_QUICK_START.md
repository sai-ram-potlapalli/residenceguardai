# 🚀 Quick Start for Judges - ResidenceGuard AI

## ⚡ 5-Minute Setup

### 1. **Run Setup Script**
```bash
python setup_for_judges.py
```

### 2. **Configure Email** (Required for full demo)
Edit `.env` file:
```
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-gmail-app-password
RESIDENCE_LIFE_EMAIL=reslife@university.edu
```

**Note**: HuggingFace token is pre-configured for demo use.

### 3. **Add Test Images**
- Place violation images in `test_images/` folder
- Include: alcohol bottles, smoking items, unauthorized appliances

### 4. **Launch Application**
```bash
python app.py
```
Open: http://localhost:8501

## 🎯 Demo Flow (10 minutes)

### **Step 1: Upload & Analyze** (3 min)
- Upload violation image
- Show detected objects and confidence scores
- Highlight AI assessment (powered by HuggingFace LLM)

### **Step 2: Resident Notification** (4 min)
- Enter resident name and email
- Check "Send violation notification to resident"
- Click "Send Report to Residence Life"
- Verify both emails sent successfully

### **Step 3: Review Output** (3 min)
- Show generated PDF report
- Demonstrate download functionality
- Highlight professional formatting

## 🔑 Key Features to Highlight

✅ **AI-Powered Detection**: CLIP model + HuggingFace LLM  
✅ **Dual Email System**: Professional reports + Resident notifications  
✅ **Automated Workflow**: One-click from detection to notification  
✅ **Professional Output**: PDF reports with complete documentation  

## 🆘 Quick Troubleshooting

**Email not sending?**
- Check Gmail app password
- Verify `.env` file exists
- Test with: `python test_email_functionality.py`

**AI models not loading?**
- Ensure 4GB+ RAM available
- Check internet connection
- HuggingFace token is pre-configured for demo

**Images not uploading?**
- Use JPG/PNG format
- Keep file size < 10MB
- Try different images

## 📞 Support Files
- `JUDGE_TESTING_GUIDE.md` - Detailed instructions
- `test_email_functionality.py` - Email testing
- `test_resident_notification.py` - Notification testing
- `debug_email.py` - Email debugging

## 🔧 Demo Environment Notes

**HuggingFace Token**: Pre-configured for demo use
- Uses developer's token for AI processing
- Rate-limited but sufficient for testing
- In production, each institution would use their own token

**Email System**: Requires Gmail setup
- Judges need to provide their own Gmail credentials
- App password required for authentication
- Test emails sent to real addresses

---

**Goal**: Demonstrate how AI transforms manual violation reporting into an automated, efficient system that benefits both staff and residents. 