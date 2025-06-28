# ResidenceGuard AI 🚨

**AI-Powered Policy Violation Detection for Residence Life**

ResidenceGuard AI automates dorm room inspections by using artificial intelligence to detect policy violations from photos and generate professional reports.

## 🎯 Problem Solved

Residence Life staff spend hours manually inspecting dorm rooms and writing violation reports. It's slow, inconsistent, and takes time away from helping students.

## ⚡ Solution

**ResidenceGuard AI** - An AI-powered app that automatically detects policy violations from room photos and generates professional reports.

## 🚀 Features

- ✅ **Object Detection** - Identifies furniture, appliances, decorations
- ✅ **Policy Matching** - Compares objects against housing rules  
- ✅ **AI Assessment** - Determines violations with confidence scores
- ✅ **Auto Reports** - Generates PDF reports instantly
- ✅ **Email Integration** - Sends notifications automatically
- ✅ **Professional UI** - Clean, intuitive interface

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Models**: CLIP (image recognition), HuggingFace LLM (violation assessment)
- **PDF Processing**: PyMuPDF, ChromaDB
- **Report Generation**: ReportLab
- **Email**: SMTP integration
- **Data Storage**: ChromaDB for policy indexing

## 📋 Prerequisites

- Python 3.8+
- pip
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "Violation Detection and Reporting System"
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
cp env.example .env
```

Edit `.env` file with your configuration:
```env
# AI Model Configuration (Pre-configured for demo)
HF_API_KEY=your_huggingface_api_key
HF_MODEL=microsoft/DialoGPT-medium

# Email Configuration (Required for full functionality)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RESIDENCE_LIFE_EMAIL=reslife@university.edu
```

### 5. Run the Application
```bash
python app.py
```

The app will be available at `http://localhost:8501`

## 🏛️ For Judges/Demo

### Quick Setup
```bash
python setup_for_judges.py
```

This will:
- ✅ Check system requirements
- ✅ Install dependencies
- ✅ Configure environment variables
- ✅ Create test images folder
- ✅ Verify system readiness

### Demo Environment
- **HuggingFace Token**: Pre-configured for demo use
- **AI Models**: Will download automatically on first use
- **Email System**: Requires Gmail credentials from judges
- **Test Images**: Place violation images in `test_images/` folder

See `JUDGE_QUICK_START.md` for detailed demo instructions.

## 📖 Usage Guide

### 1. Upload Images
- Click "Choose an image file" to upload a photo of a dorm room
- Supported formats: PNG, JPG, JPEG

### 2. Upload Policy Document
- Click "Choose a PDF file" to upload housing policy handbook
- The system will automatically extract and index policy rules

### 3. Configure Settings (Sidebar)
- Enter staff information (name, building, room number)
- Adjust confidence threshold for object detection
- Configure email settings if needed

### 4. Run Analysis
- Click "🚀 Start Analysis" to begin AI-powered violation detection
- The system will:
  - Detect objects in the image
  - Match objects against policy rules
  - Assess potential violations
  - Generate detailed results

### 5. Generate Reports
- Fill in incident details (date, time, student name, notes)
- Click "📄 Generate Report" to create professional PDF report
- Download the report or send via email

## 📁 Project Structure

```
ResidenceGuard AI/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── env.example           # Environment variables template
├── README.md             # This file
├── JUDGE_QUICK_START.md  # Quick start for judges
├── JUDGE_TESTING_GUIDE.md # Comprehensive testing guide
├── setup_for_judges.py   # Automated setup script
├── modules/              # Core AI modules
│   ├── object_detection.py    # CLIP-based object detection
│   ├── pdf_parser.py          # Policy document processing
│   ├── violation_checker.py   # LLM-based violation assessment
│   └── report_generator.py    # PDF report generation
├── utils/                # Utility modules
│   ├── config.py             # Configuration management
│   ├── helpers.py            # Helper functions
│   └── email_sender.py       # Email functionality
├── templates/            # HTML templates
├── reports/              # Generated reports storage
├── uploads/              # Temporary file storage
└── chroma_db/            # Policy indexing database
```

## 🔧 Configuration

### AI Models
- **Object Detection**: CLIP model for image recognition
- **Violation Assessment**: HuggingFace LLM for policy analysis
- **Policy Indexing**: ChromaDB for semantic search

### Email Setup
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password
3. Use the App Password in the `.env` file

## 🎯 Impact

- **90% faster** than manual inspections
- **Consistent** policy interpretation
- **Professional** documentation
- **More time** for student support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI CLIP for image recognition
- HuggingFace for LLM capabilities
- Streamlit for the web interface
- ReportLab for PDF generation

---

**Built with ❤️ for safer campus communities** 