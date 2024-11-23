import firebase_admin
from firebase_admin import credentials, firestore
import time
import joblib
import numpy as np

# Initialize Firestore
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Firestore collection name and document ID

# Store the last fetched document
last_fetched_doc = None

# Load the trained linear regression model and encoders
model = joblib.load('model.pkl')
label_encoder_location = joblib.load('location_encoder.pkl')
label_encoder_category = joblib.load('category_encoder.pkl')

# Countries and categories
countries = ["USA", "Canada", "UK", "Germany", "France", "Italy", "Spain", "Australia", "Japan", "India"]
categories = ["Painting", "Sketch", "NFT"]

def fetch_latest_document():
    """Fetch the latest document from the Firestore collection."""
    docs = db.collection("request").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(1).stream()
    for doc in docs:
        return doc.to_dict()
    return None

def update_price_in_firestore(predicted_price):
    """Update the predicted price in the Firestore document."""
    try:
        # Update the 'price' field in the specific document
        db.collection('reply').document('Tmw0QLgSltOkqVD3xOPA').update({
            "price": str(int(predicted_price))
        })
        print(f"Price updated in Firestore: {predicted_price}")
    except Exception as e:
        print(f"Error updating price in Firestore: {e}")

def predict_price():
    """Fetch the latest document and make a prediction using the trained model."""
    global last_fetched_doc
    latest_doc = fetch_latest_document()

    if not latest_doc:
        print("No document found.")
        return
    
    # Check if the fetched document is new
    if latest_doc == last_fetched_doc:
        print("Same document. Skipping prediction.")
        return
    
    # Update the last fetched document
    last_fetched_doc = latest_doc
    print("New document:", latest_doc)
    
    # Extract 'location' and 'category'
    location = latest_doc.get("location")
    category = latest_doc.get("category")
    
    if location is None or category is None:
        print("Missing required fields in the document.")
        return
    
    # Encode the 'location' and 'category' using the saved label encoders
    try:
        location_encoded = label_encoder_location.transform([location])[0]
        category_encoded = label_encoder_category.transform([category])[0]
    except ValueError as e:
        print(f"Error encoding values: {e}")
        return
    
    # Prepare the input feature array
    input_features = np.array([[location_encoded, category_encoded]])
    print(f"Encoded input features: {input_features}")

    # Make the prediction
    try:
        predicted_price = model.predict(input_features)
        print(f"Predicted Price: {predicted_price[0]}")

        # Update the price in Firestore
        update_price_in_firestore(predicted_price[0])
        
    except Exception as e:
        print("Prediction failed:", e)

# Check the database every second and make predictions if a new document is found
while True:
    predict_price()
    time.sleep(1)  # Wait for 1 second before checking again
