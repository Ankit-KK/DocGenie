import streamlit as st
from openai import OpenAI
import fitz  # PyMuPDF
import magic  # For file type detection

# Initialize OpenAI client
api_key = "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"  # Store your API key in Streamlit secrets
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

# Streamlit app title
st.title("Automated Code Documentation Generator")

# File uploader for code files (PDF and other text files)
uploaded_file = st.file_uploader("Upload your code file (PDF, .py, .java, .c, etc.)", 
                                   type=["pdf", "py", "java", "c", "cpp", "js", "html", "css", "txt"])
prompt = st.text_area("Enter your prompt for documentation generation:")
max_tokens = st.slider("Max tokens", min_value=100, max_value=2048, value=1024, step=100)

# Function to extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    pdf_document = fitz.open(file)
    for page in pdf_document:
        text += page.get_text()
    return text

# Function to read text from other code files
def read_text_from_file(file):
    text = file.read().decode("utf-8")  # Decode the byte stream to string
    return text

if st.button("Generate Documentation"):
    if uploaded_file is not None:
        # Read the first few bytes for magic detection
        uploaded_file_bytes = uploaded_file.read(2048)
        file_type = magic.from_buffer(uploaded_file_bytes, mime=True)
        uploaded_file.seek(0)  # Reset the file pointer to the beginning

        # Debugging statement to check the file type
        st.write(f"Detected file type: {file_type}")

        # Extract text based on file type
        if file_type == "application/pdf":
            code_input = extract_text_from_pdf(uploaded_file)
        elif file_type in [
            "text/x-python", 
            "text/x-script.python",  # Added this MIME type
            "text/x-java", 
            "text/x-c", 
            "text/x-c++", 
            "text/javascript", 
            "text/html", 
            "text/css", 
            "text/plain"
        ]:
            code_input = read_text_from_file(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a PDF or a text code file.")
            code_input = ""
    else:
        code_input = ""

    if code_input and prompt:
        try:
            # Call the OpenAI model
            completion = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct-v0.3",
                messages=[{"role": "user", "content": f"{prompt}\n\n{code_input}"}],
                temperature=0.2,
                top_p=0.7,
                max_tokens=max_tokens
            )

            # Extract and display the response
            if completion.choices:
                documentation = completion.choices[0].message.content  # Corrected access
                st.subheader("Generated Documentation:")
                st.write(documentation)
            else:
                st.error("No documentation generated.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please upload a valid code file and enter a prompt.")
