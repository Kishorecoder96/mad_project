# Adjust the price distribution based on the location
import pandas as pd
import random

location_price_map = {
    "UK": (6000, 9000),
    "France": (4000, 7000),
    "Italy": (3500, 6500),
    "Spain": (3000, 6000),
    "USA": (3000, 6000),
    "Canada": (3000, 6000),
    "Germany": (2500, 5500),
    "Australia": (2500, 5500),
    "Japan": (2500, 5500),
    "India": (1000, 4000),
}

countries = ["USA", "Canada", "UK", "Germany", "France", "Italy", "Spain", "Australia", "Japan", "India"]

# Art categories
categories = ["Painting", "Sketch", "NFT"]
# Generate the data with location-based price range
data = []
for _ in range(1000):
    location = random.choice(countries)
    category = random.choice(categories)
    price_range = location_price_map[location]
    price = random.randint(price_range[0], price_range[1])
    data.append([location, category, price])

# Create a DataFrame
df = pd.DataFrame(data, columns=["Location", "Category", "Price"])
df.to_csv('price_data.csv', index=False)

# Display the first few rows
df.head()
