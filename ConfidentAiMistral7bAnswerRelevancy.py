from google.cloud import aiplatform
from google.oauth2 import service_account
from deepeval.models.base_model import DeepEvalBaseLLM
from deepeval.metrics import Relevancy

# Define your custom model class by inheriting from DeepEvalBaseLLM
class Mistral7B(DeepEvalBaseLLM):
    def __init__(self, credentials, project_id, model_id, endpoint_id):
        self.credentials = credentials
        self.project_id = project_id
        self.model_id = model_id
        self.endpoint_id = endpoint_id
        self.client_options = {"api_endpoint": "us-central1-aiplatform.googleapis.com"}
        self.vertex_ai_client = None
        self.endpoint = None

    def load_model(self):
        # Initialize the Vertex AI client with your credentials
        self.vertex_ai_client = aiplatform.gapic.PredictionServiceClient(client_options=self.client_options, credentials=self.credentials)

        # Construct the full path of the endpoint
        self.endpoint = self.vertex_ai_client.endpoint_path(
            project=self.project_id, location='us-central1', endpoint=self.endpoint_id
        )

    def generate(self, prompt: str) -> str:
        # Generate text using the model
        # Make a prediction request to the Vertex AI endpoint
        payload = {
            "text": {
                "content": prompt
            }
        }
        response = self.vertex_ai_client.predict(endpoint=self.endpoint, instances=[payload])

        # Parse the prediction response
        if response.status_code == 200:
            return response.predictions[0]["generated_text"]
        else:
            return "Error: Unable to generate text."

    async def a_generate(self, prompt: str) -> str:
        # Async version of the generate method
        return self.generate(prompt)

    def get_model_name(self):
        return "Mistral 7B"

# Replace 'your-service-account.json' with your service account key file
credentials = service_account.Credentials.from_service_account_file(
    'your-service-account.json'
)

# Replace 'your-project-id', 'your-model-id', and 'your-endpoint-id' with your GCP project, model, and endpoint IDs
project_id = 'your-project-id'
model_id = 'your-model-id'
endpoint_id = 'your-endpoint-id'

# Instantiate your model with the necessary credentials
mistral_7b = Mistral7B(credentials=credentials, project_id=project_id, model_id=model_id, endpoint_id=endpoint_id)

# Load the model
mistral_7b.load_model()

# Define the Answer Relevancy metric
answer_relevancy = Relevancy()

# Example usage of the Answer Relevancy metric
question = "What is the capital of France?"
generated_answer = mistral_7b.generate(question)
relevancy_score = answer_relevancy.evaluate(generated_answer, "Paris")

print(f"Question: {question}")
print(f"Generated Answer: {generated_answer}")
print(f"Relevancy Score: {relevancy_score}")
