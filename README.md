# 🛡️ Compliance Checklist Agent

A responsive single-page web application built with Streamlit and LangChain that analyzes code snippets and generates comprehensive compliance checklists focusing on accessibility, security, and best practices.

## ✨ Features

- **🔍 AI-Powered Analysis**: Uses GPT-4 via LangChain for intelligent code analysis
- **♿ Accessibility Focus**: WCAG compliance checking and recommendations
- **🔒 Security Auditing**: Identifies potential vulnerabilities and security issues
- **📱 Fully Responsive**: Works seamlessly on desktop, tablet, and mobile devices
- **💬 Chat-like Interface**: Interactive history display similar to ChatGPT
- **🎨 Modern UI**: Clean, professional design with smooth animations
- **🔐 Secure**: API key loaded from local .env file, never exposed to frontend

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- OpenAI API key with GPT-4 access

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd Compliance-Checklist-Agent

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

1. Copy the `.env` file and add your OpenAI API key:

```bash
# Edit .env file
OPENAI_API_KEY=your-actual-api-key-here
```

2. (Optional) Customize model settings:

```bash
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.1
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 How to Use

### Input Code

1. Paste your HTML, CSS, or JavaScript code in the text area
2. The application accepts code snippets or complete files
3. Minimum 10 characters required for analysis

### Get Analysis

1. Click "Validate Code" to start analysis
2. Wait 10-30 seconds for GPT-4 processing
3. Review the generated compliance checklist

### Review Results

- **Accessibility [♿]**: WCAG compliance issues and fixes
- **Security [🔒]**: Vulnerability identification and mitigation
- **Performance [⚡]**: Optimization recommendations
- **Best Practices [✅]**: Code quality improvements

## 🏗️ Project Structure

```
Compliance-Checklist-Agent/
├── app.py              # Main Streamlit application
├── agent.py            # LangChain backend logic
├── requirements.txt    # Python dependencies
├── .env               # API key configuration (create from template)
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🔧 Technical Details

### Backend (agent.py)

- **LangChain Integration**: Uses `langchain-openai` for GPT-4 communication
- **Error Handling**: Comprehensive error management and user feedback
- **Input Validation**: Smart code detection using pattern matching
- **Configurable**: Model and temperature settings via environment variables

### Frontend (app.py)

- **Streamlit Framework**: Modern web UI with responsive design
- **Session State**: Maintains conversation history across interactions
- **Custom CSS**: Mobile-first responsive styling
- **Security**: API key never exposed to browser/frontend

### Key Features Implementation

- **Responsive Design**: CSS media queries and Streamlit column layouts
- **Chat Interface**: Two-column layout mimicking popular AI chat apps
- **Code Highlighting**: Automatic language detection and syntax highlighting
- **History Management**: Persistent session state with timestamp tracking
- **Error Recovery**: Graceful handling of API failures and network issues

## 📱 Mobile Responsiveness

The application is fully optimized for mobile devices:

- **Adaptive Layout**: Content reflows naturally on narrow screens
- **Touch-Friendly**: Large buttons and touch targets
- **Readable Text**: Optimized font sizes and spacing
- **Accessible Sidebar**: Easy navigation on mobile devices
- **Fast Loading**: Efficient code structure for mobile networks

## 🛠️ Development

### Adding New Features

1. Backend logic goes in `agent.py`
2. UI components go in `app.py`
3. Update `requirements.txt` for new dependencies

### Customization Options

- **Model Selection**: Change `OPENAI_MODEL` in `.env`
- **Response Style**: Modify prompts in `agent.py`
- **UI Styling**: Update CSS in `app.py`
- **Validation Rules**: Enhance `validate_code_snippet()` function

## 🔒 Security Considerations

- **API Key Security**: Never commit `.env` file to version control
- **Input Sanitization**: Code validation before API calls
- **Error Handling**: No sensitive information in error messages
- **Rate Limiting**: Relies on OpenAI's built-in rate limiting

## 🐛 Troubleshooting

### Common Issues

**"API Key Not Found"**

- Ensure `.env` file exists in project root
- Check that `OPENAI_API_KEY` is set correctly
- Verify the key is not the placeholder text

**"Not a code snippet"**

- Input must contain recognizable code patterns
- Try adding HTML tags, CSS properties, or JS keywords
- Ensure minimum 10 characters

**API Errors**

- Check internet connection
- Verify OpenAI API quota and billing
- Ensure GPT-4 model access

**Performance Issues**

- GPT-4 responses can take 10-30 seconds
- Avoid very large code snippets (>2000 lines)
- Check system resources and network speed

## 📋 Requirements

### Python Dependencies

- `streamlit>=1.28.0` - Web application framework
- `langchain>=0.0.340` - AI/LLM framework
- `langchain-openai>=0.0.2` - OpenAI integration
- `openai>=1.3.0` - OpenAI API client
- `python-dotenv>=1.0.0` - Environment variable management

### System Requirements

- Python 3.8+
- 512MB RAM minimum (1GB+ recommended)
- Internet connection for API calls
- Modern web browser

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly (especially mobile responsiveness)
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Streamlit** - For the excellent web framework
- **LangChain** - For simplified LLM integration
- **OpenAI** - For the powerful GPT-4 model
- **Community** - For accessibility and security best practices

---

**Built with ❤️ for better web accessibility and security**
