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
os.environ["GOOGLE_API_KEY"] = "AIzaSyAWN2aWUnP_q8b8F9oIlSIKqjjqIyNbO3k"

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

def generate_realistic_sentiment_data():
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-03-31', freq='D')
    
    comments = [
        "The food at the restaurant was not up to par. Bland and overcooked.",
        "Room cleanliness was excellent, but the air conditioning wasn't working properly.",
        "Staff were incredibly friendly and helpful. Made our stay memorable!",
        "The pool area was overcrowded and not well-maintained.",
        "Bed was comfortable, but the room lacked basic amenities like a mini-fridge.",
        "Spectacular view from our room, absolutely worth the upgrade!",
        "Breakfast buffet had a wide variety, but the quality was inconsistent.",
        "Slow Wi-Fi connection made it difficult to work from the room.",
        "The spa services were top-notch, highly recommend the massage package.",
        "Noisy neighbors made it hard to sleep, and staff didn't address the issue promptly."
    ]
    
    df = pd.DataFrame({
        'Date': dates,
        'Sentiment': np.random.choice(['Positive', 'Neutral', 'Negative'], size=len(dates), p=[0.5, 0.3, 0.2]),
        'Score': np.clip(np.random.normal(loc=0.7, scale=0.2, size=len(dates)), 0, 1),
        'Source': np.random.choice(['Booking.com', 'TripAdvisor', 'Google Reviews', 'Facebook'], size=len(dates)),
        'Comment': np.random.choice(comments, size=len(dates))
    })
    
    return df

@app.route('/analyze_sentiment')
def analyze_sentiment():
    # Generate realistic sentiment data
    sentiment_data = generate_realistic_sentiment_data()
    
    # Prepare a summary of the sentiment data
    summary = f"""
    Total reviews: {len(sentiment_data)}
    Positive reviews: {sum(sentiment_data['Sentiment'] == 'Positive')}
    Neutral reviews: {sum(sentiment_data['Sentiment'] == 'Neutral')}
    Negative reviews: {sum(sentiment_data['Sentiment'] == 'Negative')}
    Average sentiment score: {sentiment_data['Score'].mean():.2f}
    """
    
    # Use Gemini to analyze and summarize the sentiment data
    Sentiment_Analyzer = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.2,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    prompt = f"""
    As an AI expert in hotel guest sentiment analysis, please provide insights based on the following summary of recent guest reviews:

    {summary}

    Additionally, here's a sample of 10 random reviews:

    {sentiment_data.sample(10)[['Date', 'Sentiment', 'Score', 'Source', 'Comment']].to_string(index=False)}

    Please provide:
    1. A brief overview of the general sentiment trend
    2. Key areas of strength based on positive reviews
    3. Main points of improvement from negative feedback
    4. Actionable recommendations for the hotel to improve guest satisfaction

    Format your response in markdown, using appropriate headers and bullet points.
    """

    try:
        response = Sentiment_Analyzer.invoke(prompt)
        analysis = response.content
    except Exception as e:
        print(f"🚫 Sentiment Analyzer: Error generating analysis - {str(e)}")
        analysis = "Unable to generate sentiment analysis at this time."

    return jsonify({
        'summary': summary,
        'analysis': analysis,
        'recent_reviews': sentiment_data.tail(5)[['Date', 'Sentiment', 'Score', 'Source', 'Comment']].to_dict('records')
    })

@app.route('/get_dashboard_data')
def get_dashboard_data():
    try:
        # Fetch the latest data
        data = pd.read_csv("Data Ingestion/Staging/HotelReservation_dump_2024-09-02.csv")
        occupancy_rate = calculate_occupancy_rate(data)
        weather = get_weather("Data Ingestion/Staging/gurugram_weather_2024-09-02.csv")
        top_campaigns = analyze_previous_campaigns("Data Ingestion/Staging/prev_campaign.csv")
        
        # Prepare the dashboard data
        dashboard_data = {
            'occupancy_rate': occupancy_rate,
            'weather': weather,
            'top_campaigns': [{'name': k, 'likes': v} for k, v in top_campaigns.items()],
            'prev_roas': 4.0,  # You might want to calculate this dynamically
            'target_roas': 3.5  # This could be a set target
        }
        
        return jsonify(dashboard_data)
    except Exception as e:
        print(f"Error in get_dashboard_data: {str(e)}")
        return jsonify({'error': 'Failed to fetch dashboard data'}), 500
if __name__ == '__main__':
    app.run(debug=True)