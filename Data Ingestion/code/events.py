import pandas as pd
from datetime import datetime

from serpapi import GoogleSearch

params = {
  "api_key": "4040378d372e7d863af3811b19de34149fad33254c776cc2bff1b6071a8a87f9",
  "engine": "google_events",
  "q": "Events in Gurgaon",
   "api_key":"4040378d372e7d863af3811b19de34149fad33254c776cc2bff1b6071a8a87f9"
}


search = GoogleSearch(params)
results = search.get_dict()
def extract_events(results):
    events = []
    for event in results.get('events_results', []):
        event_data = {
            'title': event.get('title'),
            'start_date': event.get('date', {}).get('start_date'),
            'when': event.get('date', {}).get('when'),
            'address': ', '.join(event.get('address', [])),
            'link': event.get('link'),
            'description': event.get('description'),
            'venue_name': event.get('venue', {}).get('name'),
            'venue_rating': event.get('venue', {}).get('rating'),
            'venue_reviews': event.get('venue', {}).get('reviews')
        }
        events.append(event_data)
    return events

def main(results):
    events = extract_events(results)
    df = pd.DataFrame(events)
    
    # Get today's date for the filename
    date_tdy = datetime.now().strftime('%Y-%m-%d')
    
    # Save the DataFrame to a CSV file
    filename = f"../Staging/events_{date_tdy}.csv"
    df.to_csv(filename, index=False)
    print(f"Events have been saved to {filename}")

# You would call the main function with your API results like this:
main(results)