"""
Compliance Checklist Agent - Streamlit Frontend
A responsive web application for analyzing code snippets and generating
compliance checklists focused on accessibility and security.
"""

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
from agent import generate_checklist, validate_code_snippet

# Load environment variables
load_dotenv()

# Page configuration for responsiveness
st.set_page_config(
    page_title="Compliance Checklist Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced responsiveness and styling
st.markdown("""
<style>
    /* Main container responsive adjustments */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: none;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    
    /* Sidebar styling for mobile */
    .css-1d391kg {
        padding-top: 1rem;
    }
    
    /* Code input area styling */
    .stTextArea textarea {
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 14px;
        line-height: 1.5;
    }
    
    /* Button styling */
    .stButton button {
        width: 100%;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        border: none;
        border-radius: 8px;
        padding: 0.75rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    /* History card styling */
    .history-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #4ECDC4;
    }
    
    /* Responsive text sizing */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.5rem !important;
        }
        
        .stTextArea textarea {
            font-size: 12px;
        }
        
        .history-card {
            margin: 0.5rem 0;
            padding: 0.75rem;
        }
    }
    
    /* Success/Error message styling */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Hide anchor links next to headers */
    .stMarkdown h1 a,
    .stMarkdown h2 a,
    .stMarkdown h3 a,
    .stMarkdown h4 a,
    .stMarkdown h5 a,
    .stMarkdown h6 a {
        display: none !important;
    }
    
    /* Hide anchor link icons */
    .stMarkdown .anchor-link {
        display: none !important;
    }
    
    /* Remove hover effects on headers that might show links */
    .stMarkdown h1:hover a,
    .stMarkdown h2:hover a,
    .stMarkdown h3:hover a,
    .stMarkdown h4:hover a,
    .stMarkdown h5:hover a,
    .stMarkdown h6:hover a {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'api_key_loaded' not in st.session_state:
        st.session_state.api_key_loaded = False


def load_api_key():
    """Load and validate the OpenAI API key."""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key or api_key == 'your-api-key-here':
        st.error("""
        🚫 **API Key Not Found**
        
        Please set your OpenAI API key in the `.env` file:
        1. Open the `.env` file in the project root
        2. Replace `your-api-key-here` with your actual OpenAI API key
        3. Save the file and refresh this page
        
        **Need an API key?** Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
        """)
        return None
    
    st.session_state.api_key_loaded = True
    return api_key


def render_sidebar():
    """Render the sidebar with user manual and instructions."""
    with st.sidebar:
        st.markdown("""
        # 📖 User Manual & Instructions
        
        ## 🎯 Purpose
        This tool analyzes your HTML, CSS, and JavaScript code for:
        - **Accessibility** compliance (WCAG guidelines)
        - **Security** vulnerabilities
        - **Performance** optimizations
        - **Best practices** recommendations
        
        ## 🔧 How to Use
        
        ### Step 1: Setup
        1. Ensure your OpenAI API key is set in the `.env` file
        2. The key must be valid and have GPT-4 access
        
        ### Step 2: Input Code
        1. Paste your HTML/CSS/JS code in the text area
        2. The code can be a snippet or complete file
        3. Minimum 10 characters required
        
        ### Step 3: Validate
        1. Click "Validate Code" button
        2. Wait for the AI analysis (may take 10-30 seconds)
        3. Review the generated checklist
        
        ## 📱 Mobile Support
        - Fully responsive design
        - Sidebar accessible via hamburger menu
        - Optimized touch interactions
        - Readable on all screen sizes
        
        ## 🔍 What Gets Analyzed
        
        ### Accessibility [♿]
        - ARIA attributes and roles
        - Keyboard navigation support
        - Color contrast ratios
        - Screen reader compatibility
        - Focus management
        
        ### Security [🔒]
        - XSS vulnerabilities
        - Input validation
        - Content Security Policy
        - Secure coding practices
        - Data exposure risks
        
        ### Performance [⚡]
        - Loading optimization
        - Resource efficiency
        - Bundle size considerations
        - Caching strategies
        
        ### Best Practices [✅]
        - Code organization
        - Semantic HTML
        - CSS methodology
        - JavaScript patterns
        
        ## 🎨 Example Code Types
        
        **HTML Example:**
        ```html
        <div class="card">
          <h1>Welcome</h1>
          <button onclick="doSomething()">
            Click me
          </button>
        </div>
        ```
        
        **CSS Example:**
        ```css
        .card {
          background: #fff;
          border: 1px solid #ddd;
          padding: 20px;
        }
        ```
        
        **JavaScript Example:**
        ```javascript
        function doSomething() {
          document.getElementById('demo')
            .innerHTML = 'Hello World';
        }
        ```
        
        ## 🚨 Troubleshooting
        
        ### Common Issues:
        - **"API Key Not Found"**: Update your `.env` file
        - **"Not code snippet"**: Ensure you're pasting actual code
        - **"API Error"**: Check internet connection and API quota
        - **Slow response**: GPT-4 analysis takes time, please wait
        
        ### Need Help?
        - Check that your code contains recognizable patterns
        - Ensure proper formatting and syntax
        - Try shorter code snippets if timeout occurs
        
        ## 🔄 Version Info
        - **Framework**: Streamlit + LangChain
        - **AI Model**: GPT-4 (OpenAI)
        - **Updated**: November 2025
        """)


def render_history():
    """Render the chat-like history of validations."""
    if not st.session_state.history:
        return
    
    st.markdown("## 📋 Validation History")
    
    # Display history in reverse order (newest first)
    for i, entry in enumerate(reversed(st.session_state.history)):
        with st.container():
            # Create two columns for chat-like appearance
            col1, col2 = st.columns([1, 1])
            
            with col2:  # User code (right side)
                st.markdown(f"""
                <div style="text-align: right; margin-bottom: 0.5rem;">
                    <small style="color: #666;">
                        🧑‍💻 <strong>Your Code</strong> • {entry['timestamp']}
                    </small>
                </div>
                """, unsafe_allow_html=True)
                
                # Determine language for syntax highlighting
                code_lower = entry['code'][:100].lower()
                if '<' in code_lower and ('html' in code_lower or 'div' in code_lower):
                    language = 'html'
                elif '{' in code_lower and ('color:' in code_lower or 'margin:' in code_lower):
                    language = 'css'
                elif 'function' in code_lower or 'var ' in code_lower or 'const ' in code_lower:
                    language = 'javascript'
                else:
                    language = 'text'
                
                st.code(entry['code'][:500] + ('...' if len(entry['code']) > 500 else ''), 
                       language=language)
            
            with col1:  # Agent response (left side)
                st.markdown(f"""
                <div style="margin-bottom: 0.5rem;">
                    <small style="color: #666;">
                        🛡️ <strong>Compliance Agent</strong>
                    </small>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(entry['result'])
            
            # Add separator between entries
            if i < len(st.session_state.history) - 1:
                st.divider()


def main():
    """Main application function."""
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ Compliance Checklist Agent</h1>
        <p style="color: #666; margin: 0;">
            AI-powered code analysis for accessibility, security, and best practices
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load API key
    api_key = load_api_key()
    
    if not api_key:
        st.stop()
    
    # Main input section
    st.markdown("""
    <h3 style="margin-bottom: 1rem;">💻 Enter Your Code</h3>
    """, unsafe_allow_html=True)
    
    # Code input area
    code_input = st.text_area(
        label="Paste your HTML, CSS, or JavaScript code here:",
        placeholder="""Example:
<div class="card">
    <h1>Welcome to my website</h1>
    <button onclick="submitForm()">Submit</button>
    <img src="logo.png" />
</div>

<style>
.card { background: #fff; padding: 20px; }
button { color: blue; }
</style>

<script>
function submitForm() {
    document.getElementById('form').submit();
}
</script>""",
        height=300,
        key="code_input",
        help="Enter any HTML, CSS, or JavaScript code for compliance analysis"
    )
    
    # Validation button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        validate_button = st.button(
            "Validate Code",
            type="primary",
            use_container_width=True
        )
    
    # Handle validation
    if validate_button:
        # Input validation
        if not code_input.strip():
            st.error("⚠️ Please enter a code snippet to analyze.")
            st.stop()
        
        # Code validation
        validation_result = validate_code_snippet(code_input)
        if not validation_result['is_valid']:
            st.error(f"⚠️ {validation_result['message']}")
            st.stop()
        
        # Show processing spinner
        with st.spinner("Analyzing your code for compliance issues... This may take 10-30 seconds."):
            try:
                # Generate checklist
                result = generate_checklist(code_input, api_key)
                
                # Add to history
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.history.append({
                    'code': code_input,
                    'result': result,
                    'timestamp': timestamp
                })
                
                # Show success message
                st.success("✅ Analysis complete! Check the results below.")
                
                # Force rerun to show the new history
                st.rerun()
                
            except Exception as e:
                st.error(f"""
                ❌ **Error during analysis:**
                
                {str(e)}
                
                **Possible solutions:**
                - Check your internet connection
                - Verify your OpenAI API key and quota
                - Try again in a few moments
                """)
    
    # Show validation history
    render_history()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem 0;">
        <small>
            Built with ❤️ using Streamlit and LangChain • 
            Powered by OpenAI GPT-4 • 
            <strong>Compliance Checklist Agent v1.0</strong>
        </small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()