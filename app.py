from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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" # Replace with your actual API key
)

def generate_response(prompt):
    try:
        completion = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct-v0.3",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=True
        )

        response_text = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                response_text += chunk.choices[0].delta.content
        return response_text

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Example usage
prompt = "Write a limerick about the wonders of GPU computing."
limerick = generate_response(prompt)

if limerick:
    print("Generated Limerick:")
    print(limerick)
