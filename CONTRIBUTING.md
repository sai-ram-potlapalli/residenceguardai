# Contributing to ResidenceGuard AI

Thank you for your interest in contributing to ResidenceGuard AI! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 1. Fork the Repository
1. Go to the main repository page
2. Click the "Fork" button in the top right
3. Clone your forked repository locally

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes
- Write clean, well-documented code
- Follow the existing code style
- Add tests for new features
- Update documentation as needed

### 4. Test Your Changes
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py

# Test your changes thoroughly
```

### 5. Commit Your Changes
```bash
git add .
git commit -m "feat: add new feature description"
```

### 6. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📋 Development Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment

### Local Development
```bash
# Clone your fork
git clone https://github.com/your-username/residenceguard-ai.git
cd residenceguard-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your configuration

# Run the application
streamlit run app.py
```

## 🏗️ Project Structure

```
ResidenceGuard AI/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
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

## 📝 Code Style Guidelines

### Python
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Use type hints where appropriate

### Example
```python
def detect_objects(image_path: str, confidence_threshold: float = 0.3) -> List[Dict[str, Any]]:
    """
    Detect objects in an image using CLIP model.
    
    Args:
        image_path: Path to the image file
        confidence_threshold: Minimum confidence score for detection
        
    Returns:
        List of detected objects with confidence scores
    """
    # Implementation here
    pass
```

### Commit Messages
Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=modules
```

### Writing Tests
- Create test files in `tests/` directory
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies

## 📚 Documentation

### Code Documentation
- Add docstrings to all functions and classes
- Include type hints
- Provide examples for complex functions

### User Documentation
- Update README.md for user-facing changes
- Add screenshots for UI changes
- Update deployment guide if needed

## 🐛 Bug Reports

When reporting bugs, please include:
1. **Description** of the issue
2. **Steps to reproduce**
3. **Expected behavior**
4. **Actual behavior**
5. **Environment details** (OS, Python version, etc.)
6. **Screenshots** if applicable

## 💡 Feature Requests

When suggesting features:
1. **Describe the problem** you're trying to solve
2. **Explain your proposed solution**
3. **Provide examples** of how it would work
4. **Consider the impact** on existing functionality

## 🔒 Security

If you discover a security vulnerability:
1. **Do not** create a public issue
2. Email the maintainers directly
3. Provide detailed information about the vulnerability
4. Allow time for the issue to be addressed

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation is updated
- [ ] No sensitive data is included
- [ ] Changes are tested locally

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Other (please describe)

## Testing
- [ ] Tests pass locally
- [ ] Manual testing completed
- [ ] No breaking changes

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No sensitive data included
```

## 🏷️ Labels

We use labels to categorize issues and pull requests:
- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `question` - Further information is requested

## 📞 Getting Help

If you need help:
1. Check existing issues and discussions
2. Read the documentation
3. Ask questions in issues or discussions
4. Join our community channels (if available)

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

---

**Thank you for contributing to ResidenceGuard AI! 🚨✨** 