import streamlit as st
from openai import OpenAI
import fitz  # PyMuPDF for PDF handling
import magic  # For file type detection
import tempfile
import os

# Configuration
st.set_page_config(page_title="Automated Code Documentation Generator", layout="wide")

# Custom CSS for better UI
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stTextInput, .stTextArea {
        background-color: #f0f0f0;
        border-radius: 5px;
        padding: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 5px;
    }
    h1 {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
api_key = "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"  # Store your API key in Streamlit secrets
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

# Streamlit app title and description
st.title("Automated Code Documentation Generator")
st.markdown("Generate detailed, presentation-style documentation for your code using AI. Enter your code or upload a file.")

# Functions
def extract_text_from_pdf(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file.getvalue())
        temp_file_path = temp_file.name

    text = ""
    try:
        with fitz.open(temp_file_path) as pdf_document:
            for page in pdf_document:
                text += page.get_text()
    finally:
        os.unlink(temp_file_path)
    return text

def read_text_from_file(file):
    return file.getvalue().decode("utf-8")

def get_file_type(file):
    file_bytes = file.getvalue()
    return magic.from_buffer(file_bytes, mime=True)

def generate_documentation(code_content, max_tokens):
    prompt = '''
    Imagine you're presenting this code to a mixed audience of developers and non-technical stakeholders. 
    Create a comprehensive, engaging documentation that explains the code as if you're giving a presentation. 
    Include the following sections:

    1. Introduction:
       - Briefly describe the purpose and functionality of the code.
       - Highlight any key features or innovations.

    2. Code Overview:
       - Break down the main components or functions of the code.
       - Explain the flow and logic in a way that's easy for non-developers to grasp.

    3. Key Concepts:
       - Identify and explain any important programming concepts used in the code.
       - Use analogies or real-world examples to illustrate complex ideas.

    4. Potential Applications:
       - Discuss possible use cases or scenarios where this code could be applied.
       - Highlight its relevance to different industries or problems it could solve.

    5. Technical Deep Dive (for developers):
       - Provide more detailed explanations of the code's implementation.
       - Discuss any algorithms, design patterns, or best practices used.

    6. Challenges and Solutions:
       - Identify any potential issues or limitations of the code.
       - Suggest improvements or ways to overcome these challenges.

    7. Conclusion:
       - Summarize the key points of the documentation.
       - Emphasize the value and potential impact of the code.

    Remember to use clear, concise language and maintain an engaging, presentation-like tone throughout the documentation.
    '''
    
    try:
        completion = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct-v0.3",
            messages=[{"role": "user", "content": f"{prompt}\n\nHere's the code to document:\n\n{code_content}"}],
            temperature=0.7,
            top_p=0.9,
            max_tokens=max_tokens
        )
        return completion.choices[0].message.content if completion.choices else None
    except Exception as e:
        st.error(f"An error occurred while generating documentation: {str(e)}")
        return None

# User Interface
col1, col2 = st.columns([2, 1])

with col1:
    code_input = st.text_area("Enter your code here:", height=300)

with col2:
    uploaded_file = st.file_uploader("Or upload a code file:", 
                                     type=["pdf", "py", "java", "c", "cpp", "js", "html", "css", "txt"])

max_tokens = st.slider("Max tokens for generated documentation", 
                       min_value=100, max_value=4096, value=2048, step=100)

# Main logic
if st.button("Generate Documentation"):
    with st.spinner("Generating presentation-style documentation..."):
        if uploaded_file:
            file_type = get_file_type(uploaded_file)
            st.info(f"Detected file type: {file_type}")
            
            if file_type == "application/pdf":
                code_content = extract_text_from_pdf(uploaded_file)
            elif file_type.startswith("text"):
                code_content = read_text_from_file(uploaded_file)
            else:
                st.error("Unsupported file type. Please upload a PDF or a text code file.")
                st.stop()
        elif code_input:
            code_content = code_input
        else:
            st.error("Please provide either code input or upload a valid code file.")
            st.stop()

        documentation = generate_documentation(code_content, max_tokens)

        if documentation:
            st.subheader("Generated Documentation:")
            st.markdown(documentation)
            
            # Option to download the documentation
            st.download_button(
                label="Download Documentation",
                data=documentation,
                file_name="generated_documentation.md",
                mime="text/markdown"
            )
        else:
            st.error("Failed to generate documentation. Please try again.")

# Footer
st.markdown("---")
st.markdown("Created with ❤️ by Your Name/Company")
