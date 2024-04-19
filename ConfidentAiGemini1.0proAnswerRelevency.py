from google.cloud import aiplatform
from deepeval.models.base_model import DeepEvalBaseLLM
from deepeval.metrics import Relevancy

class Gemini1Pro(DeepEvalBaseLLM):
    def __init__(self, project_id, model_id, endpoint_id):
        self.project_id = project_id
        self.model_id = model_id
        self.endpoint_id = endpoint_id
        self.client_options = {"api_endpoint": "us-central1-aiplatform.googleapis.com"}
        self.vertex_ai_client = None
        self.endpoint = None

    def load_model(self):
        self.vertex_ai_client = aiplatform.gapic.PredictionServiceClient(client_options=self.client_options)
        self.endpoint = self.vertex_ai_client.endpoint_path(
            project=self.project_id, location='us-central1', endpoint=self.endpoint_id
        )

    def generate(self, prompt: str) -> str:
        payload = {
            "text": {
                "content": prompt
            }
        }
        response = self.vertex_ai_client.predict(endpoint=self.endpoint, instances=[payload])

        if response.status_code == 200:
            return response.predictions[0]["generated_text"]
        else:
            return "Error: Unable to generate text."

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self):
        return "Gemini 1.0 Pro"

# Replace with your actual project ID, model ID, and endpoint ID
project_id = 'your-project-id'
model_id = 'your-model-id'
endpoint_id = 'your-endpoint-id'

gemini_1_pro = Gemini1Pro(project_id=project_id, model_id=model_id, endpoint_id=endpoint_id)
gemini_1_pro.load_model()

# Define the Answer Relevancy metric
answer_relevancy = Relevancy()

# Example usage
question = "What is the capital of France?"
generated_answer = gemini_1_pro.generate(question)
relevancy_score = answer_relevancy.evaluate(generated_answer, "Paris")

print(f"Question: {question}")
print(f"Generated Answer: {generated_answer}")
print(f"Relevancy Score: {relevancy_score}")
