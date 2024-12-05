from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint

from langchain.llms import VertexAI, AzureOpenAI, Bedrock
from google.oauth2.service_account import Credentials

app = Flask(__name__)
api = Api(app)

# Configuration (replace with your actual API keys and region information)
vertex_ai_key_file = "path/to/your/vertex_ai_keyfile.json"
vertex_ai_project_id = "YOUR_PROJECT_ID"
vertex_ai_location = "YOUR_LOCATION"

azure_openai_key = "YOUR_AZURE_OPENAI_KEY"
azure_openai_endpoint = "YOUR_AZURE_OPENAI_ENDPOINT"
azure_openai_deployment_name = "YOUR_DEPLOYMENT_NAME"

bedrock_model_id = "YOUR_BEDROCK_MODEL_ID"
bedrock_region = "YOUR_BEDROCK_REGION"

def get_llm(provider, model_id, **kwargs):
    if provider == "vertex_ai":
        creds = Credentials.from_service_account_file(vertex_ai_key_file)
        return VertexAI(
            project_id=vertex_ai_project_id,
            location=vertex_ai_location,
            credentials=creds,
            model_name=model_id
        )
    elif provider == "azure_openai":
        return AzureOpenAI(
            openai_api_key=azure_openai_key,
            deployment_name=azure_openai_deployment_name,
            endpoint=azure_openai_endpoint
        )
    elif provider == "bedrock":
        return Bedrock(
            model_id=bedrock_model_id,
            region=bedrock_region,
            **kwargs
        )
    else:
        return "Invalid provider"

class GenerateText(Resource):
    def post(self):
        data = request.get_json()
        provider = data.get('provider')
        model_id = data.get('model_id')
        prompt = data.get('prompt')

        llm = get_llm(provider, model_id)
        response = llm(prompt)
        return jsonify({'response': response})

api.add_resource(GenerateText, '/generate')

# Swagger UI Configuration
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={'app_name': "LLM API"}
)
app.register_blueprint(swaggerui_blueprint, SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)
