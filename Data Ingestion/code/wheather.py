import http.client
import json
import pandas as pd
from datetime import datetime

# Step 1: Establish a connection
conn = http.client.HTTPSConnection("www.weatherunion.com")

# Step 2: Set the headers
headers = { 
    'X-Zomato-Api-Key': "fd8535d885da18e73721f8002242fdff"
}

# Step 3: Make the request for Gurugram's coordinates
conn.request("GET", "/gw/weather/external/v0/get_weather_data?latitude=28.4595&longitude=77.0266", headers=headers)

# Step 4: Get the response and read the data
res = conn.getresponse()
data = res.read()

# Step 5: Decode the JSON data
weather_data = json.loads(data.decode("utf-8"))

# Step 6: Extract relevant fields
locality_weather = weather_data.get("locality_weather_data", {})
extracted_data = {
    "temperature": locality_weather.get("temperature"),
    "humidity": locality_weather.get("humidity"),
    "wind_speed": locality_weather.get("wind_speed"),
    "wind_direction": locality_weather.get("wind_direction"),
    "rain_intensity": locality_weather.get("rain_intensity"),
    "rain_accumulation": locality_weather.get("rain_accumulation")
}

# Step 7: Convert to DataFrame
df = pd.DataFrame([extracted_data])

# Step 8: Get today's date and format it
today_date = datetime.now().strftime("%Y-%m-%d")

# Step 9: Save to CSV with today's date in the filename
filename = f"../Staging/gurugram_weather_{today_date}.csv"
df.to_csv(filename, index=False)

print(f"Weather data saved to {filename}")
