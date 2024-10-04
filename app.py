import streamlit as st
from openai import OpenAI
import fitz  # PyMuPDF

# Initialize OpenAI client
api_key = "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"  # Store your API key in Streamlit secrets
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

# Streamlit app title
st.title("Automated Code Documentation Generator")

# File uploader for PDF or text area for code
uploaded_file = st.file_uploader("Upload your code PDF file", type=["pdf"])
code_input = st.text_area("Or enter your code here:")
prompt = st.text_area("Enter your prompt for documentation generation:")
max_tokens = st.slider("Max tokens", min_value=100, max_value=2048, value=1024, step=100)

# Function to extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    pdf_document = fitz.open(file)
    for page in pdf_document:
        text += page.get_text()
    return text

if st.button("Generate Documentation"):
    # Check if code input is from PDF or text area
    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        code_input = extract_text_from_pdf(uploaded_file)

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
        st.error("Please provide either code or upload a PDF file and enter a prompt.")
