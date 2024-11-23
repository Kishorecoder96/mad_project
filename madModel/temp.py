import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firestore
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def print_all_collections_and_documents():
    # Fetch all collections
    collections = db.collections()
    for collection in collections:
        print(f"Collection: {collection.id}")
        
        # Fetch all documents in the collection
        docs = collection.stream()
        for doc in docs:
            print(f"  Document ID: {doc.id}")
            print(f"  Data: {doc.to_dict()}")
        print("-" * 40)  # Separator for readability

try:
    print_all_collections_and_documents()
except Exception as e:
    print(f"Error: {e}")

from datetime import datetime

# Update the existing document to include a timestamp
doc_ref = db.collection("request").document("AIgn1qEBkQLjGqdnoGdl")
doc_ref.update({
    "timestamp": datetime.utcnow()
})
print("Timestamp added.")