from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
import pandas as pd
import json
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Set up SerpApi key
API_KEY = os.getenv("SERPAPI_API_KEY")

def search_hotels(query, check_in_date=None, check_out_date=None, adults=2):
    if check_in_date is None:
        check_in_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    if check_out_date is None:
        check_out_date = (datetime.now() + timedelta(days=31)).strftime("%Y-%m-%d")

    params = {
        "engine": "google_hotels",
        "q": query,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "adults": str(adults),
        "currency": "USD",
        "gl": "us",
        "hl": "en",
        "api_key": API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    return results

def parse_hotel_results(results):
    hotels = []
    if 'hotels_results' in results:
        for hotel in results['hotels_results']:
            hotel_info = {
                "name": hotel.get("name", "N/A"),
                "price": hotel.get("price", "N/A"),
                "rating": hotel.get("rating", "N/A"),
                "reviews": hotel.get("reviews", "N/A"),
                "address": hotel.get("address", "N/A"),
                "description": hotel.get("description", "N/A")
            }
            hotels.append(hotel_info)
    return hotels

def main():
    query = "hotels in sector 14 gurgaon"
    
    print(f"Searching for {query}...")
    results = search_hotels(query)
    
    hotels = parse_hotel_results(results)
    
    if not hotels:
        print("No hotels found.")
        return
    
    # Create a pandas DataFrame
    df = pd.DataFrame(hotels)
    
    print("\nHotel Information:")
    print(df)
    
    # Save to CSV
    df.to_csv("hotels_data.csv", index=False)
    print("\nData saved to hotels_data.csv")
    
    # Save to JSON
    with open("hotels_data.json", "w") as f:
        json.dump(hotels, f, indent=2)
    print("Data saved to hotels_data.json")

    # Print some additional information from the results
    if 'search_metadata' in results:
        print(f"\nTotal results: {results['search_metadata'].get('total_results', 'N/A')}")
    if 'search_parameters' in results:
        print(f"Search parameters: {results['search_parameters']}")

if __name__ == "__main__":
    main()