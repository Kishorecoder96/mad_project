import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib



# Create DataFrame
df = pd.read_csv('price_data.csv')

# Encode the categorical features into numerical values
label_encoder_location = LabelEncoder()
label_encoder_category = LabelEncoder()

df['Location'] = label_encoder_location.fit_transform(df['Location'])
df['Category'] = label_encoder_category.fit_transform(df['Category'])

# Features and Target
X = df[['Location', 'Category']]  # Input features
y = df['Price']  # Target variable

# Split data into training and testing sets (here using 80-20 split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the model and encoders
joblib.dump(model, 'model.pkl')
joblib.dump(label_encoder_location, 'location_encoder.pkl')
joblib.dump(label_encoder_category, 'category_encoder.pkl')

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Example prediction using the saved model
# Load the saved model and encoders
loaded_model = joblib.load('model.pkl')
loaded_location_encoder = joblib.load('location_encoder.pkl')
loaded_category_encoder = joblib.load('category_encoder.pkl')

# # Predict for a new input
# sample_input = [[loaded_location_encoder.transform(['Canada'])[0], loaded_category_encoder.transform(['Sketch'])[0]]]
# predicted_price = loaded_model.predict(sample_input)
# print(f'Predicted Price for Canada, Sketch: {predicted_price[0]}')
