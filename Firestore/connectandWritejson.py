import json
import google.auth
from firebase_admin import credentials, firestore

# Replace with your credentials file path
cred_path = "path/to/your/serviceAccountKey.json"

# Initialize credentials and Firestore client
credentials = credentials.Certificate(cred_path)
firebase_app = firestore.App(credentials=credentials)
db = firestore.client(firebase_app)

# Get data as a dictionary from DataFrame
data = df.to_dict(orient="records")

# Add data to Firestore collection
collection_ref = db.collection("your_collection_name")
for doc in data:
    collection_ref.add(doc)

print("Data successfully added to Firestore collection!")
