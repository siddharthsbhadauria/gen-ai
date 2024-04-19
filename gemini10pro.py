import requests
from deepeval.metrics import Relevancy

# Replace 'API_URL' with the actual URL provided for Gemini 1.0 Pro
API_URL = "https://api.google.com/gemini/v1/pro"

def generate_text(prompt):
    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        # Add any other required headers
    }
    data = {
        "prompt": prompt,
        # Include any other required fields
    }
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()  # Or however the response is structured
    else:
        return f"Error: {response.status_code}, {response.text}"

# Example usage
question = "What is the capital of France?"
generated_answer = generate_text(question)

# Define the Answer Relevancy metric
answer_relevancy = Relevancy()
relevancy_score = answer_relevancy.evaluate(generated_answer, "Paris")

print(f"Question: {question}")
print(f"Generated Answer: {generated_answer}")
print(f"Relevancy Score: {relevancy_score}")
