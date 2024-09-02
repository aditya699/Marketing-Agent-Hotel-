import json
import pandas as pd
from typing import Dict, List

def extract_hotel_data(data: Dict) -> List[Dict]:
    hotels = []
    for property in data['properties']:
        hotel = {
            'name': property['name'],
            'price': property.get('rate_per_night', {}).get('lowest', None),
            'rating': property.get('overall_rating', None),
            'reviews': property.get('reviews', None),
            'hotel_class': property.get('hotel_class', None),
            'location_rating': property.get('location_rating', None)
        }
        hotels.append(hotel)
    return hotels

# Assuming you have the API response stored in a variable called 'results'
# If it's stored in a JSON file, you can load it like this:
# with open('api_response.json', 'r') as f:
#     results = json.load(f)


from serpapi import GoogleSearch

params = {
  "api_key": "4040378d372e7d863af3811b19de34149fad33254c776cc2bff1b6071a8a87f9",
  "engine": "google_hotels",
  "q": "Guragon Sector 14",
  "hl": "en",
  "gl": "in",
  "check_in_date": "2024-09-03",
  "check_out_date": "2024-09-04",
  "currency": "INR",
  "api_key":"4040378d372e7d863af3811b19de34149fad33254c776cc2bff1b6071a8a87f9"
}

search = GoogleSearch(params)
results = search.get_dict()
# Extract hotel data
hotels_data = extract_hotel_data(results)

# Create a pandas DataFrame
df = pd.DataFrame(hotels_data)

# Clean up the 'price' column by removing the currency symbol and commas, then converting to float
df['price'] = df['price'].replace('Not available', pd.NA)
df['price'] = df['price'].str.replace('₹', '').str.replace(',', '')
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Drop rows where price is NA
df = df.dropna(subset=['price'])

# Convert rating and location_rating to numeric, coercing errors to NaN
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['location_rating'] = pd.to_numeric(df['location_rating'], errors='coerce')

# Save to CSV
df.to_csv('../Staging/competitor_data.csv', index=False)
print("Data saved to hotels_data.csv")


# Display the first few rows of the DataFrame
print(df.head())

