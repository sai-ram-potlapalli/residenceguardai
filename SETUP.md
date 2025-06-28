# Setup Guide - AI-Powered Violation Detection System

This guide will help you set up and run the violation detection system on your local machine.

## 🚀 Quick Start

### Prerequisites

- **Python 3.8 or higher**
- **OpenAI API Key** (required for LLM functionality)
- **Internet connection** (for downloading AI models)
- **At least 4GB RAM** (recommended for smooth operation)

### Step 1: Clone and Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd violation-detection-system
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Configuration

1. **Create environment file**:
   ```bash
   cp env.example .env
   ```

2. **Edit the `.env` file** with your settings:
   ```env
   # Required: Your OpenAI API key
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Optional: Model settings
   MODEL_NAME=gpt-4
   CLIP_MODEL_NAME=openai/clip-vit-base-patch32
   
   # Optional: Application settings
   DEBUG=True
   HOST=0.0.0.0
   PORT=8000
   STREAMLIT_PORT=8501
   ```

3. **Get an OpenAI API Key**:
   - Go to [OpenAI Platform](https://platform.openai.com/)
   - Sign up or log in
   - Navigate to API Keys section
   - Create a new API key
   - Copy the key to your `.env` file

### Step 3: Test the System

1. **Run the test suite**:
   ```bash
   python test_system.py
   ```

2. **Verify all tests pass** before proceeding.

### Step 4: Run the Application

#### Option A: Streamlit Frontend (Recommended for beginners)

```bash
# Using the runner script
python run.py --mode streamlit

# Or directly with streamlit
streamlit run app.py
```

The application will be available at: `http://localhost:8501`

#### Option B: FastAPI Backend (For developers/API users)

```bash
# Using the runner script
python run.py --mode api

# Or directly with uvicorn
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`
API documentation at: `http://localhost:8000/docs`

#### Option C: Both Frontend and Backend

```bash
python run.py --mode both
```

## 📖 Usage Guide

### Using the Streamlit Interface

1. **Upload an Image**: Select a photo of the room/area to inspect
2. **Upload Policy PDF**: Provide the housing policy document
3. **Configure Settings**: Set staff info and detection threshold in sidebar
4. **Start Analysis**: Click "Start Analysis" to process the image
5. **Review Results**: Check the analysis tabs for detailed information
6. **Generate Report**: Add notes and generate an incident report
7. **Download Report**: Download the PDF report for documentation

### Using the API

#### Analyze an Image
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "image=@path/to/image.jpg" \
  -F "policy_pdf=@path/to/policy.pdf" \
  -F "staff_name=John Doe" \
  -F "room_number=101" \
  -F "building_name=North Hall"
```

#### Generate a Report
```bash
curl -X POST "http://localhost:8000/generate_report" \
  -H "Content-Type: application/json" \
  -d '{
    "image_path": "/path/to/image.jpg",
    "detected_objects": [...],
    "violation_assessment": {...},
    "policy_rules": [...],
    "staff_name": "John Doe"
  }'
```

## 🔧 Troubleshooting

### Common Issues

#### 1. OpenAI API Key Error
```
❌ Configuration error: OPENAI_API_KEY is required
```
**Solution**: Make sure you've set your OpenAI API key in the `.env` file.

#### 2. Model Download Issues
```
Error loading CLIP model: ...
```
**Solution**: 
- Check your internet connection
- Try running the application again (models are cached after first download)
- Ensure you have sufficient disk space

#### 3. Memory Issues
```
CUDA out of memory
```
**Solution**:
- Close other applications to free up memory
- The system will automatically use CPU if GPU memory is insufficient
- Consider reducing the confidence threshold

#### 4. Port Already in Use
```
Address already in use
```
**Solution**:
- Change the port in your `.env` file
- Or kill the process using the port:
  ```bash
  # Find the process
  lsof -i :8501
  # Kill it
  kill -9 <PID>
  ```

### Performance Optimization

1. **GPU Acceleration**: If you have a CUDA-compatible GPU, the system will automatically use it for faster processing.

2. **Model Caching**: Models are downloaded once and cached locally. Subsequent runs will be faster.

3. **Confidence Threshold**: Adjust the confidence threshold in the sidebar to balance accuracy vs. detection sensitivity.

## 📁 File Structure

```
violation-detection-system/
├── app.py                 # Streamlit frontend
├── main.py               # FastAPI backend
├── run.py                # Application runner
├── test_system.py        # System tests
├── requirements.txt      # Python dependencies
├── env.example          # Environment template
├── .env                 # Your environment config (create this)
├── README.md            # Project documentation
├── SETUP.md             # This setup guide
├── modules/             # Core AI modules
│   ├── object_detection.py
│   ├── pdf_parser.py
│   ├── violation_checker.py
│   └── report_generator.py
├── utils/               # Utility functions
│   ├── config.py
│   └── helpers.py
├── templates/           # Report templates
├── uploads/             # Temporary file storage
├── reports/             # Generated reports
└── chroma_db/          # Vector database (created automatically)
```

## 🔒 Security Considerations

1. **API Key Security**: Never commit your `.env` file to version control
2. **File Uploads**: All uploaded files are processed locally and not stored permanently
3. **Network Access**: The system runs locally by default for security
4. **Data Privacy**: No data is sent to external services except OpenAI API calls

## 🚀 Deployment

### Local Network Deployment

To make the system available on your local network:

1. **Update the host setting** in `.env`:
   ```env
   HOST=0.0.0.0
   ```

2. **Configure firewall** to allow connections on the specified ports

3. **Access from other devices** using your computer's IP address:
   ```
   http://YOUR_IP_ADDRESS:8501
   ```

### Production Deployment

For production deployment, consider:

1. **Reverse Proxy**: Use nginx or Apache as a reverse proxy
2. **Process Manager**: Use systemd or supervisor for process management
3. **SSL/TLS**: Configure HTTPS for secure connections
4. **Database**: Use a production database instead of local files
5. **Monitoring**: Add logging and monitoring capabilities

## 📞 Support

If you encounter issues:

1. **Check the logs** for error messages
2. **Run the test suite** to identify component issues
3. **Verify your configuration** matches the requirements
4. **Check the troubleshooting section** above

For additional support, please refer to the project documentation or create an issue in the repository.

## 🎯 Next Steps

After successful setup:

1. **Test with sample images** to familiarize yourself with the system
2. **Upload your institution's policy documents** for accurate violation detection
3. **Train staff** on using the system effectively
4. **Customize the violation categories** if needed for your specific policies
5. **Set up regular backups** of generated reports

---

**Happy detecting! 🚨✨** 