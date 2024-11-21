import streamlit as st
from langchain_nvidia_ai_endpoints import ChatNVIDIA
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
    .feedback-button {
        background-color: #4CAF50; 
        color: white; 
        padding: 10px 20px; 
        text-align: center; 
        text-decoration: none; 
        display: inline-block; 
        font-size: 14px; 
        margin: 4px 2px; 
        cursor: pointer;
        border: none;
        border-radius: 8px;
    }
    .feedback-container {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# Initialize NVIDIA ChatNVIDIA client
client = ChatNVIDIA(
    model="mistralai/mistral-7b-instruct-v0.3",
    api_key=st.secrets["api_key"],  # Ensure the API key is set in Streamlit secrets
    temperature=0.2,
    top_p=0.7,
    max_tokens=1024
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

def generate_documentation_with_langchain(code_content):
    """
    Function to generate documentation using ChatNVIDIA model.
    """
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
    
    response = ""
    for chunk in client.stream([{"role": "user", "content": f"{prompt}\n\nHere's the code to document:\n\n{code_content}"}]):
        response += chunk.content
    return response

# User Interface
code_input = st.text_area("Enter your code here:", height=300)
uploaded_file = st.file_uploader("Or upload a code file:", 
                                 type=["pdf", "py", "java", "c", "cpp", "js", "html", "css", "txt"])

# Feedback section
feedback_container = st.container()
with feedback_container:
    st.markdown("""
    <div class="feedback-container" style="margin-top: 20px;">
        <a href="https://forms.gle/rTrFC4rwqfJ9B6mE9" target="_blank">
            <button class="feedback-button" style="margin-top: 20px;">
                Open Feedback Form
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)


# Main logic
if st.button("Generate Documentation"):
    with st.spinner("Generating documentation using the ChatNVIDIA model..."):
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

        # Generate documentation
        documentation = generate_documentation_with_langchain(code_content)

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
st.markdown("Created with ❤️ by Ankit")
