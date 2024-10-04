import streamlit as st
from openai import OpenAI
import fitz  # PyMuPDF for PDF handling
import magic  # For file type detection
import tempfile
import os

# Initialize OpenAI client
api_key ="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"  # Store your API key in Streamlit secrets
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

# Streamlit app configuration
st.set_page_config(page_title="Code Documentation Generator", layout="wide")

# Streamlit app title and description
st.title("Automated Code Documentation Generator")
st.markdown("""
This app generates detailed documentation for your code using AI. 
You can either paste your code directly or upload a file.
""")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    model = st.selectbox("Select AI Model", ["mistralai/mistral-7b-instruct-v0.3", "anthropic/claude-3-sonnet-20240229"])
    max_tokens = st.slider("Max tokens", min_value=100, max_value=4096, value=1024, step=100)
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
    top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.subheader("Input")
    code_input = st.text_area("Enter your code here:", height=300)
    uploaded_file = st.file_uploader("Or upload a file (.py, .java, .c, .cpp, .js, .html, .css, .txt, .pdf)", 
                                     type=["py", "java", "c", "cpp", "js", "html", "css", "txt", "pdf"])

with col2:
    st.subheader("Documentation Style")
    doc_style = st.radio("Choose documentation style:", 
                         ["Detailed", "Concise", "Developer-focused", "End-user focused"])
    custom_instructions = st.text_area("Additional instructions (optional):", 
                                       placeholder="E.g., Focus on performance considerations, Include usage examples, etc.")

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

def generate_prompt(code, style, custom_instructions):
    base_prompt = "Analyze the following code and provide documentation that is "
    style_prompts = {
        "Detailed": "comprehensive and thorough, covering all aspects of the code.",
        "Concise": "brief and to the point, highlighting only the most important elements.",
        "Developer-focused": "technical and in-depth, suitable for experienced programmers.",
        "End-user focused": "user-friendly and focused on how to use the code or application."
    }
    prompt = f"{base_prompt}{style_prompts[style]}\n\n"
    if custom_instructions:
        prompt += f"Additional instructions: {custom_instructions}\n\n"
    prompt += "Here's the code to document:\n\n```\n{code}\n```"
    return prompt

def generate_documentation(prompt, model, max_tokens, temperature, top_p):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Main logic
if st.button("Generate Documentation"):
    with st.spinner("Generating documentation..."):
        if uploaded_file:
            file_type = get_file_type(uploaded_file)
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

        prompt = generate_prompt(code_content, doc_style, custom_instructions)
        documentation = generate_documentation(prompt, model, max_tokens, temperature, top_p)

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
