# 🎯 Demo Configuration Guide - HuggingFace Token

## 🏛️ **Recommended Approach for Judge Testing**

### **Option 1: Demo Token (Recommended)**
Create a dedicated HuggingFace account for demos:
1. Create a new HuggingFace account: `residenceguard-demo`
2. Generate a new API token for this account
3. Use this token for all judge testing
4. Monitor usage and reset if needed

### **Option 2: Your Token (If Needed)**
If using your personal token:
- **Advantages**: Quick setup, guaranteed access
- **Disadvantages**: Rate limits, security concerns
- **Mitigation**: Monitor usage, have backup plan

### **Option 3: No Token (Fallback)**
For basic demos without LLM features:
- System will work with object detection only
- Violation assessment will be simplified
- Still demonstrates core functionality

## 🔧 **Implementation Options**

### **For Demo Environment:**
```bash
# Option 1: Demo token
HUGGINGFACE_TOKEN=hf_demo_token_here

# Option 2: Your token (temporary)
HUGGINGFACE_TOKEN=your_personal_token

# Option 3: No token (fallback)
HUGGINGFACE_TOKEN=
```

### **Token Management Strategy:**
1. **Pre-Demo**: Set up demo token in `.env`
2. **During Demo**: Monitor usage in HuggingFace dashboard
3. **Post-Demo**: Reset or rotate token if needed

## 📊 **Usage Considerations**

### **Rate Limits:**
- **Free Tier**: 30,000 requests/month
- **Demo Usage**: ~10-50 requests per demo
- **Multiple Judges**: Could hit limits with 5+ judges

### **Cost Implications:**
- **Free Tier**: Usually sufficient for demos
- **Paid Tier**: Consider if heavy usage expected
- **Monitoring**: Track usage to avoid surprises

## 🛡️ **Security Best Practices**

### **Token Protection:**
- Never commit tokens to Git
- Use environment variables only
- Rotate tokens regularly
- Monitor for unauthorized usage

### **Demo Environment:**
- Use dedicated demo account
- Limit token permissions
- Set up usage alerts
- Have backup tokens ready

## 🎯 **Recommendation for Your Presentation**

### **Best Approach:**
1. **Create Demo Account**: `residenceguard-demo@example.com`
2. **Generate Demo Token**: Limited permissions
3. **Pre-configure**: Set up in `.env` file
4. **Monitor Usage**: During presentation
5. **Reset After**: Clean up demo account

### **Fallback Plan:**
- Have your personal token as backup
- Prepare demo without LLM if needed
- Focus on object detection and email features

## 📝 **Setup Instructions for Judges**

### **With Demo Token:**
```bash
# 1. Run setup script
python setup_for_judges.py

# 2. Edit .env file (demo token pre-configured)
# HUGGINGFACE_TOKEN=hf_demo_token_here

# 3. Launch application
python app.py
```

### **Without Token (Fallback):**
```bash
# 1. Run setup script
python setup_for_judges.py

# 2. Leave HUGGINGFACE_TOKEN empty in .env
# HUGGINGFACE_TOKEN=

# 3. Launch application (object detection only)
python app.py
```

## 🔄 **Post-Demo Cleanup**

### **If Using Demo Account:**
- Delete demo account after presentation
- Revoke all tokens
- Clear any stored data

### **If Using Your Token:**
- Monitor for unusual activity
- Consider rotating token
- Update usage tracking

---

**Bottom Line**: For a professional demo, create a dedicated demo account with limited permissions. This protects your personal account while ensuring reliable access for judges. 