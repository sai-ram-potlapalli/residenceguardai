# Deployment Guide for ResidenceGuard AI

This guide covers different deployment options for ResidenceGuard AI.

## 🚀 Local Development

### Prerequisites
- Python 3.8+
- Git
- Virtual environment

### Setup
```bash
git clone <repository-url>
cd "Violation Detection and Reporting System"
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
# Edit .env with your configuration
streamlit run app.py
```

## ☁️ Cloud Deployment Options

### 1. Streamlit Cloud (Recommended)

**Pros:**
- Free tier available
- Easy deployment
- Automatic updates from GitHub
- Built for Streamlit apps

**Steps:**
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set environment variables in Streamlit Cloud dashboard
5. Deploy!

**Environment Variables to Set:**
```
HF_API_KEY=your_huggingface_api_key
HF_MODEL=microsoft/DialoGPT-medium
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RESIDENCE_LIFE_EMAIL=reslife@university.edu
```

### 2. Heroku

**Steps:**
1. Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

3. Deploy:
```bash
heroku create your-app-name
heroku config:set HF_API_KEY=your_key
heroku config:set HF_MODEL=microsoft/DialoGPT-medium
git push heroku main
```

### 3. Railway

**Steps:**
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically

### 4. Google Cloud Platform

**Steps:**
1. Create a Cloud Run service
2. Build and deploy with Docker:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
```

### 5. AWS

**Using AWS App Runner:**
1. Create a Dockerfile (same as above)
2. Push to ECR
3. Deploy with App Runner

**Using AWS EC2:**
1. Launch EC2 instance
2. Install Python and dependencies
3. Use systemd service for auto-restart
4. Configure nginx as reverse proxy

## 🔧 Production Considerations

### Environment Variables
- **Never commit** `.env` files to version control
- Use platform-specific secret management
- Rotate API keys regularly

### Performance
- Consider using GPU instances for faster AI processing
- Implement caching for policy documents
- Use CDN for static assets

### Security
- Enable HTTPS
- Implement rate limiting
- Add authentication if needed
- Regular security updates

### Monitoring
- Set up logging
- Monitor API usage
- Track application performance
- Set up alerts for errors

## 📊 Scaling

### Horizontal Scaling
- Use load balancers
- Deploy multiple instances
- Use shared storage for files

### Vertical Scaling
- Increase CPU/memory
- Use GPU instances for AI processing
- Optimize database queries

## 🔍 Troubleshooting

### Common Issues

1. **Port Issues**
   - Ensure port is correctly configured
   - Check firewall settings

2. **Environment Variables**
   - Verify all required variables are set
   - Check for typos in variable names

3. **Dependencies**
   - Ensure all packages are in requirements.txt
   - Check for version conflicts

4. **File Permissions**
   - Ensure write permissions for reports/ and uploads/
   - Check ChromaDB directory permissions

### Logs
- Check application logs for errors
- Monitor system resources
- Review API response times

## 📞 Support

For deployment issues:
1. Check the platform's documentation
2. Review error logs
3. Test locally first
4. Open an issue on GitHub

---

**Happy Deploying! 🚀** 