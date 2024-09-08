from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os

# Import all functions from your existing script
from app import (
    calculate_occupancy_rate, analyze_previous_campaigns, competitor_analysis,
    events, get_weather, get_customer_data, generate_personalized_message,
    generate_social_media_content
)

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_analysis')
def run_analysis():
    try:
        # Run the main analysis
        data = pd.read_csv("Data Ingestion/Staging/HotelReservation_dump_2024-09-02.csv")
        occupancy_rate = calculate_occupancy_rate(data)
        
        results = {
            'occupancy_rate': f'{occupancy_rate:.2%}',
            'messages': []
        }

        OCCUPANCY_THRESHOLD = 0.75

        if occupancy_rate < OCCUPANCY_THRESHOLD:
            results['messages'].append("⚠️ Low occupancy detected. Initiating marketing campaign protocols.")
            
            top_campaigns = analyze_previous_campaigns("Data Ingestion/Staging/prev_campaign.csv")
            if not top_campaigns.empty:
                results['top_campaigns'] = top_campaigns.to_dict()
            
            weather = get_weather("Data Ingestion/Staging/gurugram_weather_2024-09-02.csv")
            results['weather'] = weather
            
            events_data = events("Data Ingestion/Staging/events_2024-09-02.csv")
            competitor_prices = competitor_analysis("Data Ingestion/Staging/competitor_data.csv")
            customer_data = get_customer_data("Data Ingestion/Staging/historical_bookings.csv")

            if not customer_data.empty:
                personalized_messages = []
                for _, customer in customer_data.iterrows():
                    our_price = np.random.uniform(3000, 5000)
                    message = generate_personalized_message(
                        customer['customer_name'],
                        weather,
                        events_data,
                        competitor_prices,
                        our_price
                    )
                    personalized_messages.append({
                        'customer_name': customer['customer_name'],
                        'customer_email': customer['customer_email'],
                        'message': message
                    })
                results['personalized_messages'] = personalized_messages

            social_media_content = generate_social_media_content(
                hotel_name="Royal Villas",
                weather=weather,
                events=events_data,
                special_offer=our_price
            )
            results['social_media_content'] = social_media_content

        else:
            results['messages'].append("✅ Occupancy rates are satisfactory. No immediate marketing action required.")

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)