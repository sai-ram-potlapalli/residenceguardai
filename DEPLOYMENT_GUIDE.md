# 🚀 Deployment Guide - ResidenceGuard AI

## 🎯 **Recommended: Streamlit Cloud Deployment**

### **Why Streamlit Cloud?**
- ✅ **Easiest Setup**: Designed specifically for Streamlit apps
- ✅ **Free Tier**: Available for public apps
- ✅ **AI Model Support**: Handles large models and dependencies
- ✅ **Automatic Scaling**: Handles multiple users
- ✅ **Direct Access**: Judges can access via URL immediately

### **Step 1: Prepare for Deployment**

#### **1.1 Create Streamlit Cloud Account**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign up with GitHub account
3. Connect your repository

#### **1.2 Update Requirements**
Ensure your `requirements.txt` is deployment-ready:
```txt
# Core Framework
streamlit>=1.25.0
fastapi>=0.100.0
uvicorn>=0.20.0

# AI/ML Libraries
transformers>=4.30.0
torch>=2.0.0
Pillow>=9.5.0

# PDF Processing
PyMuPDF>=1.23.0
pdfplumber>=0.9.0

# Vector Database
chromadb>=0.4.0
sentence-transformers>=2.2.0

# Utilities
python-multipart>=0.0.6
pydantic>=2.0.0
python-dotenv>=1.0.0
reportlab>=4.0.0
jinja2>=3.1.0

# Email
smtplib2>=0.2.1
```

#### **1.3 Create Streamlit Configuration**
Create `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 10
enableXsrfProtection = false
enableCORS = false

[browser]
gatherUsageStats = false
```

### **Step 2: Deploy to Streamlit Cloud**

#### **2.1 Push to GitHub**
```bash
git add .
git commit -m "Deploy to Streamlit Cloud"
git push origin main
```

#### **2.2 Deploy on Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository
4. Set main file path: `app.py`
5. Click "Deploy"

#### **2.3 Configure Environment Variables**
In Streamlit Cloud dashboard:
- `HUGGINGFACE_TOKEN`: Your HuggingFace API token
- `SENDER_EMAIL`: Demo email for testing
- `SENDER_PASSWORD`: Email app password
- `RESIDENCE_LIFE_EMAIL`: Demo recipient email

### **Step 3: Test Deployment**
1. Access your app at: `https://your-app-name.streamlit.app`
2. Test all features:
   - Image upload
   - PDF upload
   - AI analysis
   - Email functionality
3. Verify performance and reliability

## 🔥 **Alternative: Firebase Deployment**

### **Option 2A: Firebase Hosting + Cloud Functions**

#### **Pros:**
- ✅ **Scalable**: Handles high traffic
- ✅ **Professional**: Enterprise-grade hosting
- ✅ **Custom Domain**: Professional URL

#### **Cons:**
- ❌ **Complex Setup**: Requires converting Streamlit to web app
- ❌ **Cost**: Pay-per-use pricing
- ❌ **Development Time**: Significant refactoring needed

#### **Implementation Steps:**
1. **Convert Streamlit to Flask/FastAPI**
2. **Create Firebase project**
3. **Deploy backend to Cloud Functions**
4. **Deploy frontend to Firebase Hosting**

### **Option 2B: Firebase + Streamlit (Hybrid)**

#### **Simpler Approach:**
1. **Keep Streamlit app as-is**
2. **Deploy to Streamlit Cloud**
3. **Use Firebase for:**
   - Custom domain
   - Analytics
   - Additional services

## 🚂 **Alternative: Railway/Heroku**

### **Option 3: Railway Deployment**

#### **Pros:**
- ✅ **Easy Setup**: Similar to Streamlit Cloud
- ✅ **Good Performance**: Fast deployment
- ✅ **Free Tier**: Available for testing

#### **Steps:**
1. Go to [railway.app](https://railway.app)
2. Connect GitHub repository
3. Set environment variables
4. Deploy automatically

### **Option 4: Heroku Deployment**

#### **Pros:**
- ✅ **Reliable**: Established platform
- ✅ **Good Documentation**: Extensive guides

#### **Cons:**
- ❌ **No Free Tier**: Paid service only
- ❌ **Slower**: Compared to newer platforms

## 📋 **Deployment Checklist**

### **Pre-Deployment:**
- [ ] Code is production-ready
- [ ] Environment variables configured
- [ ] Dependencies optimized
- [ ] Error handling implemented
- [ ] Security measures in place

### **Post-Deployment:**
- [ ] Test all features
- [ ] Verify email functionality
- [ ] Check performance
- [ ] Monitor error logs
- [ ] Update documentation

## 🎯 **For Judges: Access Instructions**

### **Streamlit Cloud (Recommended):**
1. **URL**: `https://residenceguard-ai.streamlit.app`
2. **No Installation Required**: Works in any browser
3. **Test Images**: Provided in documentation
4. **Demo Credentials**: Pre-configured for testing

### **Demo Environment:**
- **HuggingFace Token**: Pre-configured
- **Email System**: Demo credentials provided
- **Test Data**: Sample images and PDFs included
- **Support**: Documentation and troubleshooting guides

## 🔧 **Troubleshooting**

### **Common Issues:**
1. **Model Loading Slow**: First-time users may experience delays
2. **Memory Issues**: Large models require sufficient RAM
3. **Email Errors**: Check SMTP configuration
4. **Upload Failures**: Verify file size limits

### **Performance Optimization:**
1. **Model Caching**: Implement model caching
2. **Image Compression**: Optimize upload sizes
3. **Async Processing**: Use background tasks
4. **CDN**: Use content delivery networks

## 📊 **Monitoring & Analytics**

### **Streamlit Cloud Analytics:**
- User visits and engagement
- Performance metrics
- Error tracking
- Usage patterns

### **Custom Analytics:**
- Violation detection accuracy
- User feedback collection
- System performance metrics
- Feature usage statistics

---

**Recommendation**: Start with Streamlit Cloud for immediate judge access, then consider Firebase for production deployment if needed. 