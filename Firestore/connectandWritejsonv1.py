from google.cloud import firestore
from google.oauth2 import service_account

# Path to your service account key file
key_path = "path/to/your/serviceAccountKey.json"

# Load the credentials
credentials = service_account.Credentials.from_service_account_file(key_path)

# Project ID and database URL
project_id = "your-project-id"
database_url = "https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)".format(project_id=project_id)

# Initialize Firestore client with database URL
db = firestore.Client(project=project_id, credentials=credentials, database=database_url)

# Reference to your collection
collection_ref = db.collection('collect1')

# Data to write
data = {
    'field1': 'value1',
    'field2': 'value2',
    'field3': 123
}

# Add a new document with a generated ID
collection_ref.add(data)

print("Data written successfully.")