from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

def generate_response(prompt):
    try:
        # Request completion from the OpenAI API
        completion = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct-v0.3",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=True
        )

        response_text = ""
        # Collect the response chunks
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                response_text += chunk.choices[0].delta.content

        return response_text.strip()  # Strip any leading/trailing whitespace

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Define a prompt to explain a specific function
    prompt = "Explain the function `add_numbers` that adds two numbers."
    documentation = generate_response(prompt)

    if documentation:
        print("Generated Documentation:")
        print(documentation)  # Print only the relevant content
