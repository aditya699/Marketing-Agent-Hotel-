from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

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

def generate_campaign_recommendation():
    Campaign_Manager = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    prompt = """
    As an AI marketing specialist for Royal Villas, an exclusive Indian hotel, provide recommendations for our social media campaign strategy.
    Consider the following constraints:
    - Total budget: 5000 rupees per campaign
    - Current occupancy rate is lower than desired
    - We want to increase bookings for the upcoming holiday season

    Please provide:
    1. Recommended number of days for the campaign
    2. Budget allocation per day
    3. A brief strategy for maximizing impact within these constraints

    Format your response as follows:
    Campaign Duration: [Number of days]
    Daily Budget: [Amount in rupees]
    Strategy: [2-3 sentences on maximizing impact]

    Return only the formatted response without any additional explanations.
    """

    try:
        response = Campaign_Manager.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"🚫 AI Campaign Manager: Error generating recommendation - {str(e)}")
        return "Unable to generate campaign recommendation at this time."

def generate_corporate_message(company_name, event_type, attendees, duration):
    Corporate_Message_Generator = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    prompt = f"""
    As the marketing manager for Royal Villas, an exclusive Indian hotel, craft a formal message for a corporate booking inquiry from {company_name}.
    Consider the following details:
    - Event type: {event_type}
    - Number of attendees: {attendees}
    - Duration: {duration} days

    The message should:
    1. Use a formal and professional tone
    2. Highlight our hotel's capabilities for hosting corporate events
    3. Mention any special amenities or services relevant to corporate bookings
    4. Provide a brief overview of our conference facilities
    5. Suggest setting up a call or meeting to discuss further details

    Return only the message content, without any additional explanations.
    """

    try:
        response = Corporate_Message_Generator.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"🚫 Corporate Message Generator: Error generating message - {str(e)}")
        return "Unable to generate corporate booking message at this time."

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
            'messages': [],
            'prev_roas': 4.0,
            'target_roas': 3.5
        }

        OCCUPANCY_THRESHOLD = 0.75

        if occupancy_rate < OCCUPANCY_THRESHOLD:
            results['messages'].append("⚠️ Low occupancy detected. Initiating marketing campaign protocols.")
            
            top_campaigns = analyze_previous_campaigns("Data Ingestion/Staging/prev_campaign.csv")
            if not top_campaigns.empty:
                results['top_campaigns'] = top_campaigns.to_dict()
            
            weather = get_weather("Data Ingestion/Staging/gurugram_weather_2024-10-09.csv")
            results['weather'] = weather
            
            events_data = events("Data Ingestion/Staging/events_2024-10-09.csv")
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

            # Generate campaign recommendation
            campaign_recommendation = generate_campaign_recommendation()
            results['campaign_recommendation'] = campaign_recommendation

            # Generate corporate booking message
            corporate_message = generate_corporate_message(
                company_name="TechCorp Inc.",
                event_type="Annual Conference",
                attendees=150,
                duration=3
            )
            results['corporate_message'] = corporate_message

        else:
            results['messages'].append("✅ Occupancy rates are satisfactory. No immediate marketing action required.")

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)