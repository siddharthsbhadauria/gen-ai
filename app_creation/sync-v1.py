import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Assuming you have LLMTestCase defined elsewhere
class LLMTestCase:
  # ... your LLMTestCase class definition ...

def get_output(prompt):
  # Implement your logic to generate output for the given prompt
  # This could involve calling an LLM model or any other method
  # Replace this with your actual implementation
  output = "This is a placeholder output for prompt: " + prompt
  return output

# Initialize Firebase app with credentials
cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Get a Firestore database client
db = firestore.client()

# Reference the specific collection (eval_jobs)
collection_ref = db.collection('eval_jobs')

# Create a query to filter documents with "execution_type" as "ready"
query = collection_ref.where('execution_type', '==', 'ready')

# Get all matching documents
try:
  documents = query.get()
  for doc in documents:
    doc_data = doc.to_dict()  # Get document data as a dictionary
    eval_id = doc_data.get('eval_id')  # Get value for 'eval_id' field (if it exists)
    job_id = doc_data.get('job_id')  # Get value for 'job_id' field (if it exists)
    
    # Check if both IDs are present before using them
    if eval_id and job_id:
      print(f'Document ID: {doc.id}')
      print(f'eval_id: {eval_id}')
      print(f'job_id: {job_id}')

      # Reference the test cases collection based on eval_id
      test_cases_ref = db.collection('eval_testcases').where('eval_id', '==', eval_id)

      # Get all matching test cases
      test_cases = test_cases_ref.get()

      # Process test cases (if any)
      if test_cases:
        print('Test Cases:')
        tests = []  # Initialize an empty list to store test cases
        for test_case in test_cases:
          test_case_data = test_case.to_dict()  # Get document data
          nested_test_cases = test_case_data.get('test_cases')  # Get nested test cases data

          # Check if nested test cases exist
          if nested_test_cases:
            # Loop through each nested test case using item (key, value) pairs
            for key, nested_case in nested_test_cases.items():
              prompt = nested_case.get('prompt')
              expected_output = nested_case.get('expected_output')
              context = nested_case.get('context')  # Assuming context is present

              # Get actual output using the function
              output = get_output(prompt)

              # Create LLMTestCase object and append to the list
              test_case_obj = LLMTestCase(prompt, output, expected_output, context=context)
              tests.append(test_case_obj)
          else:
            print(f'Test case document {test_case.id} has no "test_cases" field.')

        # Print all test cases using your defined method (assuming it exists)
        print_test_cases(tests)  # Replace with your method to print test cases

      else:
        print('No test cases found for this eval_id.')

      print('---')  # Add a separator between documents
    else:
      print(f'Document ID: {doc.id} - Missing required fields (eval_id or job_id)')

except Exception as e:
  print(f'Error fetching documents: {e}')
