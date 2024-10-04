import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=st.secrets["API_KEY"]  # Use Streamlit secrets for API key
)

# Streamlit app title
st.title("Automated Code Documentation Generator")

# User input for code
user_code = st.text_area("Enter your code:", height=300)

# User input for additional instructions
instructions = st.text_input("Additional instructions for documentation:")

# Button to generate documentation
if st.button("Generate Documentation"):
    if user_code:
        # Prepare the prompt for the GenAI model
        prompt = f"Generate documentation for the following code:\n\n{user_code}\n\nInstructions: {instructions}"

        # Call the OpenAI model
        completion = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct-v0.3",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024
        )

        # Extract and display the response
        documentation = completion.choices[0].message['content']
        st.subheader("Generated Documentation:")
        st.write(documentation)
    else:
        st.error("Please enter some code to generate documentation.")
