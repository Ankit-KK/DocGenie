import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
api_key = st.secrets["openai_api_key"]  # Store your API key in Streamlit secrets
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

# Streamlit app title
st.title("Automated Code Documentation Generator")

# User inputs
code_input = st.text_area("Enter your code here:")
prompt = st.text_area("Enter your prompt for documentation generation:")
max_tokens = st.slider("Max tokens", min_value=100, max_value=2048, value=1024, step=100)

if st.button("Generate Documentation"):
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

            # Debugging line: print the entire response
            st.write(completion)  # Print for debugging

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
        st.error("Please provide both code and a prompt.")
