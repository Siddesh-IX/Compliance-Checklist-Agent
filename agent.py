"""
Compliance Checklist Agent - Core Backend Logic
This module contains the LangChain-based agent that analyzes code snippets
and generates compliance checklists focusing on accessibility and security.
"""

import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def generate_checklist(code_snippet: str, api_key: str) -> str:
    """
    Generate a compliance checklist for the given code snippet using LangChain and OpenAI.
    
    Args:
        code_snippet (str): The code to analyze (HTML/CSS/JS)
        api_key (str): OpenAI API key
        
    Returns:
        str: Formatted markdown checklist with compliance recommendations
    """
    try:
        # Initialize the OpenAI model
        model = os.getenv('OPENAI_MODEL', 'gpt-4')
        temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.1'))
        
        llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=temperature
        )
        
        # Create the system prompt template
        system_prompt = """
        You are a senior web development compliance expert. Analyze code and provide practical, actionable recommendations.
        
        Guidelines:
        1. Focus on [Accessibility] and [Security] issues first
        2. Include [Performance] and [Best Practices] when relevant  
        3. Provide minimum 3 specific, actionable recommendations
        4. Each recommendation should be 1-2 sentences max
        5. Be direct and practical - avoid theoretical explanations
        6. Focus on "what to change" rather than "why it's important"
        7. Use simple, clear language
        
        Response Format:
        **Priority Level:**
        Select exactly ONE priority level based on the issues found:
        - Use 🔴 High for critical security/accessibility issues
        - Use 🟡 Medium for important improvements  
        - Use 🟢 Low for minor enhancements
        
        Output only the selected priority (example: 🔴 High)
        
        **Recommendations:**
        1. **[Category] Issue**: Quick fix description
        2. **[Category] Issue**: Quick fix description
        ...
        
        **Summary:**
        One sentence overview of main issues found.
        """
        
        # Create the human prompt template
        human_prompt = """
        Analyze this code for practical improvements:
        
        ```
        {code_snippet}
        ```
        
        Focus on specific fixes the developer can implement right now. Keep recommendations short and actionable.
        """
        
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", human_prompt)
        ])
        
        # Generate the response
        chain = prompt | llm
        response = chain.invoke({"code_snippet": code_snippet})
        
        return response.content
        
    except Exception as e:
        error_message = f"""
        # ❌ Error Generating Checklist
        
        **Error Type**: {type(e).__name__}
        
        **Error Message**: {str(e)}
        
        ## Possible Solutions:
        1. **[Configuration]** Verify your OpenAI API key is correct in the .env file
        2. **[Network]** Check your internet connection
        3. **[API Limits]** Ensure you have available API quota
        4. **[Model Access]** Verify you have access to the specified model (default: gpt-4)
        
        ## Troubleshooting Steps:
        - Double-check the OPENAI_API_KEY in your .env file
        - Ensure the .env file is in the project root directory
        - Try again in a few moments if this is a temporary API issue
        """
        return error_message


def validate_code_snippet(code_snippet: str) -> Dict[str, Any]:
    """
    Validate that the input appears to be a code snippet.
    
    Args:
        code_snippet (str): The input to validate
        
    Returns:
        Dict[str, Any]: Validation result with 'is_valid' boolean and 'message' string
    """
    if not code_snippet or not code_snippet.strip():
        return {
            'is_valid': False,
            'message': 'Please enter a code snippet to analyze.'
        }
    
    # Common code indicators
    code_indicators = [
        # HTML tags
        '<div', '<span', '<p', '<h1', '<h2', '<h3', '<h4', '<h5', '<h6',
        '<html', '<head', '<body', '<title', '<meta', '<link', '<script',
        '<form', '<input', '<button', '<img', '<a', '<ul', '<li', '<table',
        
        # CSS selectors and properties
        'class=', 'id=', 'style=', '{', '}', 'color:', 'background:', 'margin:',
        'padding:', 'font-', 'display:', 'position:', 'width:', 'height:',
        
        # JavaScript keywords
        'function', 'var ', 'let ', 'const ', 'if (', 'for (', 'while (',
        'return', 'document.', 'window.', 'console.', 'addEventListener',
        '=>', 'async', 'await', 'import ', 'export ', 'class ',
        
        # Common programming patterns
        '()', '[]', '==', '===', '!=', '!==', '&&', '||', '//', '/*', '*/',
    ]
    
    code_snippet_lower = code_snippet.lower()
    found_indicators = [indicator for indicator in code_indicators if indicator in code_snippet_lower]
    
    if not found_indicators:
        return {
            'is_valid': False,
            'message': 'The input doesn\'t appear to be a code snippet. Please enter HTML, CSS, or JavaScript code.'
        }
    
    # Additional check for minimum length
    if len(code_snippet.strip()) < 10:
        return {
            'is_valid': False,
            'message': 'Please enter a more substantial code snippet for analysis.'
        }
    
    return {
        'is_valid': True,
        'message': f'Code snippet detected with {len(found_indicators)} code indicators.'
    }