import streamlit as st
from openai import OpenAI
import fitz  # PyMuPDF for PDF handling
import magic  # For file type detection
import tempfile
import os

# Configuration
st.set_page_config(page_title="Automated Code Documentation Generator", layout="wide")

# Initialize OpenAI client
api_key = "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"  # Store your API key in Streamlit secrets
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

# Streamlit app title and description
st.title("Automated Code Documentation Generator")
st.markdown("Generate detailed documentation for your code using AI. Enter your code or upload a file.")

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
    prompt = '''Provide detailed descriptions of the code, usage instructions, and any relevant explanations. 
    Ensure the documentation is clear, concise, and suitable for both developers and end-users.'''
    
    try:
        completion = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct-v0.3",
            messages=[{"role": "user", "content": f"{prompt}\n\n{code_content}"}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=max_tokens
        )
        return completion.choices[0].message.content if completion.choices else None
    except Exception as e:
        st.error(f"An error occurred while generating documentation: {str(e)}")
        return None

# User Interface
col1, col2 = st.columns(2)

with col1:
    code_input = st.text_area("Enter your code here:", height=300)

with col2:
    uploaded_file = st.file_uploader("Or upload a code file:", 
                                     type=["pdf", "py", "java", "c", "cpp", "js", "html", "css", "txt"])

max_tokens = st.slider("Max tokens for generated documentation", 
                       min_value=100, max_value=2048, value=1024, step=100)

# Main logic
if st.button("Generate Documentation"):
    with st.spinner("Generating documentation..."):
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
