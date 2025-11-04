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
    }
    
    .main-header h1 {
        font-size: 3.2rem !important;
        color: #4485ff !important;
        font-weight: 700 !important;
        margin: 0 0 0.5rem 0 !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Ensure main header is not affected by general stMarkdown styling */
    div.main-header h1 {
        font-size: 3.2rem !important;
        color: #4485ff !important;
        font-weight: 700 !important;
    }
    
    .main-header p {
        color: #4b5563 !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }
    
    /* History section styling */
    .history-section {
        max-height: 60vh;
        overflow-y: auto;
        scroll-behavior: smooth;
        margin-bottom: 2rem;
    }
    
    /* Input section styling */
    .input-section {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 2rem;
        border: 2px solid #e9ecef;
        position: sticky;
        bottom: 0;
        z-index: 100;
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
        .main-header h1,
        div.main-header h1,
        .main-header .stMarkdown h1 {
            font-size: 2.2rem !important;
        }
        
        .main-header p {
            font-size: 0.95rem !important;
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
    
    /* Agent response styling - consistent small font with bold headings */
    .stMarkdown {
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    /* Style for agent response headers only, not main header */
    .stMarkdown h1:not(.main-header h1), 
    .stMarkdown h2, 
    .stMarkdown h3, 
    .stMarkdown h4, 
    .stMarkdown h5, 
    .stMarkdown h6 {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        margin: 0.75rem 0 0.5rem 0 !important;
        color: #949494 !important;
    }
    
    /* Additional specificity for main header */
    .main-header .stMarkdown h1,
    div.main-header h1 {
        font-size: 3.2rem !important;
        color: #4485ff !important;
        font-weight: 700 !important;
        margin: 0 0 0.5rem 0 !important;
    }
    
    /* Specific styling for h2 headings */
    .stMarkdown h2 {
        font-size: 18px !important;
        font-weight: 600 !important;
        margin: 0.75rem 0 0.5rem 0 !important;
        color: #949494 !important;
    }
    
    .stMarkdown p {
        font-size: 0.9rem;
        margin: 0.4rem 0;
    }
    
    .stMarkdown ul, .stMarkdown ol {
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    
    .stMarkdown li {
        margin: 0.2rem 0;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'api_key_loaded' not in st.session_state:
        st.session_state.api_key_loaded = False
    if 'clear_input' not in st.session_state:
        st.session_state.clear_input = False


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
        ## 🎯 Purpose
        This tool analyzes your HTML, CSS, and JavaScript code for:
        - **Accessibility** compliance (WCAG guidelines)
        - **Security** vulnerabilities
        - **Performance** optimizations
        - **Best practices** recommendations

        ---

        ## 📋 Instructions

        ### Step 1: Add Your Code
        1. Paste your HTML/CSS/JS code in the text area below
        2. You can submit a snippet or paste entire file
        3. Supports HTML, CSS, and JavaScript code only
        
        ### Step 2: Analyze & Review
        1. Click the "Validate Code" button
        2. Wait for the AI analysis (typically 10-30 seconds)
        3. Review your personalized compliance checklist
        
        ### Step 3: Improve Your Code
        1. Follow the recommendations provided
        2. Submit updated code for re-analysis
        3. Track your improvements over time

        ---
        
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

        ---
        
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

        ---
        
        ## 🚨 Troubleshooting
        
        ### Common Issues:
        - **"Not code snippet"**: Ensure you're pasting actual code
        - **"API Error"**: Check internet connection and API quota
        - **Slow response**: GPT-4 analysis takes time, please wait
        
        ### Need Help?
        - Check that your code contains recognizable patterns
        - Ensure proper formatting and syntax
        - Try shorter code snippets if timeout occurs

        ---
        
        ## 🔄 Version Info
        - **Framework**: Streamlit + LangChain
        - **AI Model**: GPT-4 (OpenAI)
        - **Developed**: November 2025
        """)


def render_history():
    """Render the chat-like history of validations."""
    if not st.session_state.history:
        return
    
    st.markdown(f"## � Conversation History ({len(st.session_state.history)} analysis{'es' if len(st.session_state.history) != 1 else ''})")
    
    # Display history in reverse order (newest first)
    for i, entry in enumerate(reversed(st.session_state.history)):
        # Add a subtle conversation separator
        # Parse the timestamp and format as "3 Nov, 21:46"
        try:
            timestamp_obj = datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S")
            formatted_time = timestamp_obj.strftime("%d %b, %H:%M").lstrip('0')  # Remove leading zero from day
        except:
            # Fallback to original format if parsing fails
            formatted_time = entry['timestamp'].split(' ')[1][:5]  # Just HH:MM
        
        st.markdown(f"""
        <div style="border-bottom: 1px solid #e9ecef; padding-bottom: 0.5rem; margin: 0.5rem 0;">
            <small style="color: #888; font-weight: 400; font-size: 0.75rem;">
                Conversation #{len(st.session_state.history) - i} • {formatted_time}
            </small>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            # Create two columns for chat-like appearance
            col1, col2 = st.columns([1, 1])
            
            with col2:  # User code (right side)
                st.markdown("""
                <div style="text-align: right; margin-bottom: 0.5rem;">
                    <span style="background: #e3f2fd; padding: 0.25rem 0.5rem; border-radius: 10px; color: #1976d2; font-size: 0.8rem;">
                        🧑‍💻 <strong>You</strong>
                    </span>
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
                st.markdown("""
                <div style="margin-bottom: 0.5rem;">
                    <span style="background: #e8f5e8; padding: 0.25rem 0.5rem; border-radius: 10px; color: #2e7d32; font-size: 0.8rem;">
                        🛡️ <strong>Compliance Agent</strong>
                    </span>
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
    
    # History section (at the top)
    st.markdown('<div class="history-section">', unsafe_allow_html=True)
    render_history()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Clear input if flag is set
    if st.session_state.clear_input:
        st.session_state.code_input = ""
        st.session_state.clear_input = False
    
    # Code input area with on_change callback
    code_input = st.text_area(
        label="Paste your HTML, CSS, or JavaScript code here:",
        placeholder="""Paste your code snippet here!""",
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
                
                # Clear input for next request
                st.session_state.clear_input = True
                
                # Show success message
                st.success("✅ Analysis complete! Ready for your next code snippet.")
                
                # Force rerun to show the new history and clear input
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
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem 0;">
        <small>
            Built with ❤️ using Streamlit and LangChain • 
            Powered by OpenAI GPT-4
        </small>
        <p>
            <small>Compliance Checklist Agent v1.0</small>
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()