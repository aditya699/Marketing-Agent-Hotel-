import numpy as np
import pandas as pd
import os
from typing import Dict, List
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

def calculate_occupancy_rate(data: pd.DataFrame) -> float:
    total_reservations = len(data)
    if total_reservations == 0:
        return 0.0
    confirmed_reservations = len(data[data['ReservationStatus'] == 'Confirmed'])
    return confirmed_reservations / total_reservations

def analyze_previous_campaigns(file_path: str) -> pd.Series:
    try:
        data_prev_campaigns = pd.read_csv(file_path)
        if 'Campaign_Run_Timings' not in data_prev_campaigns.columns or 'Likes' not in data_prev_campaigns.columns:
            raise ValueError("CSV file does not contain required columns")
        grouped_prev_campaigns = data_prev_campaigns.groupby('Campaign_Run_Timings')['Likes'].sum()
        top_3_campaigns = grouped_prev_campaigns.sort_values(ascending=False).head(3)
        return top_3_campaigns
    except FileNotFoundError:
        print(f"📁 AI Data Analyst: Error accessing file {file_path}. Previous campaign data not found.")
        return pd.Series()
    except pd.errors.EmptyDataError:
        print(f"📊 AI Data Analyst: The file {file_path} contains no data. Unable to analyze previous campaigns.")
        return pd.Series()
    except ValueError as e:
        print(f"🚫 AI Data Analyst: Data format issue - {str(e)}")
        return pd.Series()

def competitor_analysis(file_path: str) -> pd.DataFrame:
    try:
        data = pd.read_csv(file_path)
        data = data[['name', 'price']]
        return data.head(10)
    except Exception as e:
        print(f"🚫 AI Data Analyst: Error in competitor analysis - {str(e)}")
        return pd.DataFrame()

def events(file_path: str) -> pd.DataFrame:
    try:
        data = pd.read_csv(file_path)
        data = data[['title', 'start_date', 'description']]
        return data.head(10)
    except Exception as e:
        print(f"🚫 AI Data Analyst: Error in events data - {str(e)}")
        return pd.DataFrame()

def get_weather(file_path: str) -> str:
    try:
        data = pd.read_csv(file_path)
        if data.empty:
            return "pleasant"
        
        weather_data = data.iloc[0]
        description = []
        
        if 'temperature' in weather_data:
            temp = weather_data['temperature']
            if temp < 15:
                description.append("cool")
            elif 15 <= temp < 25:
                description.append("mild")
            else:
                description.append("warm")
        
        if 'humidity' in weather_data:
            humidity = weather_data['humidity']
            if humidity > 70:
                description.append("humid")
            elif humidity < 30:
                description.append("dry")
        
        if 'wind_speed' in weather_data:
            wind = weather_data['wind_speed']
            if wind > 20:
                description.append("windy")
            elif wind < 5:
                description.append("calm")
        
        if 'rain_intensity' in weather_data:
            rain = weather_data['rain_intensity']
            if rain > 0:
                description.append("rainy")
        
        return " and ".join(description) if description else "pleasant"
    except Exception as e:
        print(f"🚫 AI Data Analyst: Error in weather data - {str(e)}. Using default.")
        return "pleasant"

def get_customer_data(file_path: str) -> pd.DataFrame:
    try:
        data = pd.read_csv(file_path)
        data = data.sample(3)  # Increased sample size for demonstration
        return data[['customer_name', 'customer_email']]
    except Exception as e:
        print(f"🚫 AI Data Analyst: Error in customer data - {str(e)}")
        return pd.DataFrame()

def generate_personalized_message(customer_name: str, weather: str, events: pd.DataFrame, competitor_prices: pd.DataFrame, our_price: float) -> str:
    Campaign_Manager = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    hotel_name = "Royal Villas"
    website_link = "https://www.royalvillas.com/special-offer"

    lowest_competitor_price = competitor_prices['price'].min() if not competitor_prices.empty else our_price * 1.2

    prompt = f"""
    As an AI marketing specialist for {hotel_name}, an exclusive Indian hotel, create a personalized email message for {customer_name}.
    Consider the following information:
    - Current weather: {weather}
    - Upcoming events: {events.to_dict(orient='records') if not events.empty else 'No upcoming events'}
    - Our hotel's special offer price: ₹{our_price:.2f}
    - Lowest competitor price: ₹{lowest_competitor_price:.2f}

    The email should:
    1. Address the customer by name and introduce {hotel_name}
    2. Mention the current {weather} weather and how it makes it a perfect time to visit
    3. Highlight one or two upcoming events (if available), emphasizing their exclusivity
    4. Emphasize our special offer price, stating it's a limited-time discount
    5. Subtly indicate that our price is lower than competitors without naming them
    6. Include a strong call to action to book now, with the website link: {website_link}
    7. Create a sense of urgency (e.g., "limited rooms available", "offer ending soon")
    8. Keep the tone luxurious, exclusive, and inviting

    Return only the email message, without any additional explanations or comments.
    """

    try:
        response = Campaign_Manager.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"🚫 AI Campaign Manager: Error generating message - {str(e)}")
        return f"Dear {customer_name}, enjoy a luxurious stay at {hotel_name} for just ₹{our_price:.2f}! Book now at {website_link} for this exclusive offer. We look forward to welcoming you!"

def generate_social_media_content(hotel_name: str, weather: str, events: pd.DataFrame, special_offer: float) -> str:
    Social_Media_Manager = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    prompt = f"""
    As a creative Social Media Manager for {hotel_name}, an exclusive Indian hotel, create unique and engaging content for Instagram/Twitter reels and posts.
    Consider the following information:
    - Current weather: {weather}
    - Upcoming events: {events.to_dict(orient='records') if not events.empty else 'No upcoming events'}
    - Special offer price: ₹{special_offer:.2f}

    Generate:
    1. 5 creative and unique reel ideas (short video concepts)
    2. 5 engaging post captions

    The content should:
    - Showcase the luxurious aspects of the hotel in innovative ways
    - Creatively highlight the current weather and how it enhances the stay
    - Mention upcoming events if available, presenting them in an exciting manner
    - Incorporate the special offer subtly and enticingly
    - Use relevant and trendy hashtags
    - Be highly engaging, shareable, and tailored to our upscale audience

    Format your response as follows:
    REELS:
    1. [Reel idea 1]
    2. [Reel idea 2]
    3. [Reel idea 3]
    4. [Reel idea 4]
    5. [Reel idea 5]

    POSTS:
    1. [Post caption 1]
    2. [Post caption 2]
    3. [Post caption 3]
    4. [Post caption 4]
    5. [Post caption 5]

    Be creative and avoid generic content. Each idea should be unique and captivating.
    """

    try:
        response = Social_Media_Manager.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"🚫 Social Media Manager: Error generating content - {str(e)}")
        return f"""
        REELS:
        1. Experience unparalleled luxury at {hotel_name} #LuxuryRedefined
        2. Sunset timelapse from our infinity pool #HeavenlyViews
        3. Chef's secret recipe reveal: Our signature dish #CulinaryMagic
        4. 360° tour: Presidential Suite extravaganza #RoyalLiving
        5. Local artisans at work: Handcrafted elegance #CulturalTreasures

        POSTS:
        1. Discover a new level of opulence at {hotel_name}. Limited time offer: ₹{special_offer:.2f} per night! #LuxuryEscape
        2. Bask in {weather} perfection. Your dream vacation at {hotel_name} awaits. #WeatherBliss
        3. Savor excellence: Our Michelin-starred chef's tasting menu will transport your senses. #GastronomicJourney
        4. Rejuvenation redefined: Experience our award-winning spa's signature treatment. #SpaHeaven
        5. Create timeless memories with our exclusive curated experiences. #UnforgettableMoments
        """

def main():
    print("🏨 Hotel AI Marketing System: Initializing...")

    try:
        print("📊 AI Data Analyst: Accessing current reservation data...")
        data = pd.read_csv("Data Ingestion/Staging/HotelReservation_dump_2024-09-02.csv")

        print("🧮 AI Occupancy Calculator: Analyzing current occupancy rates...")
        occupancy_rate = calculate_occupancy_rate(data)
        print(f'🏨 Current Hotel Occupancy Rate: {occupancy_rate:.2%}')

        OCCUPANCY_THRESHOLD = 0.75  # 75%

        if occupancy_rate < OCCUPANCY_THRESHOLD:
            print("⚠️ AI Alert System: Low occupancy detected. Initiating marketing campaign protocols.")
            
            top_campaigns = analyze_previous_campaigns("Data Ingestion/Staging/prev_campaign.csv")
            if not top_campaigns.empty:
                print("📈 AI Data Analyst: Top 3 Previous Campaigns by Engagement:")
                print(top_campaigns)
                Campaign_Manager = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    temperature=0,
                    max_tokens=None,
                    timeout=None,
                    max_retries=2,
                )
                prompt_1 = f'''As the AI Campaign Manager, determine the optimal time to run a new campaign. 
                Return only the hour (0 to 24) with no additional text.
                Base your decision on this data from our hotel's previous campaigns (Time | Engagement Metric):
                {top_campaigns}
                '''
                try:
                    timing_call = Campaign_Manager.invoke(prompt_1)
                    print(f"🕒 AI Campaign Manager: Optimal campaign launch time calculated: {timing_call.content}:00 hours")
                except Exception as e:
                    print(f"🚨 System Alert: AI Campaign Manager encountered an error: {str(e)}")
            else:
                print("📊 AI Data Analyst: Insufficient data on previous campaigns. Recommending default strategy.")

            print("🚀 AI Campaign Manager: Preparing to launch new marketing initiative.")

            # Get necessary data for personalized messages
            weather = get_weather("Data Ingestion/Staging/gurugram_weather_2024-09-02.csv")
            print(f"🌤️ Current weather: {weather}")
            events_data = events("Data Ingestion/Staging/events_2024-09-02.csv")
            competitor_prices = competitor_analysis("Data Ingestion/Staging/competitor_data.csv")
            customer_data = get_customer_data("Data Ingestion/Staging/historical_bookings.csv")

            if not customer_data.empty:
                # Generate and display personalized messages for each customer
                for _, customer in customer_data.iterrows():
                    our_price = np.random.uniform(3000, 5000)  # Random price between 3000 and 5000 INR
                    
                    message = generate_personalized_message(
                        customer['customer_name'],
                        weather,
                        events_data,
                        competitor_prices,
                        our_price
                    )
                    
                    print(f"\n📧 Personalized message for {customer['customer_name']} ({customer['customer_email']}):")
                    print(message)
                    print("-" * 50)
            else:
                print("🚨 System Alert: No customer data available for personalized messages.")

            print("\n🚀 Social Media Manager: Generating social media content...")
            social_media_content = generate_social_media_content(
                hotel_name="Royal Villas",
                weather=weather,
                events=events_data,
                special_offer=our_price
            )

            print("\n✅ Social Media Manager: Content generation complete.")
            print(social_media_content)
            print("\n✅ Social Media Manager: Content generation complete.")

        else:
            print("✅ AI Occupancy Monitor: Occupancy rates are satisfactory. No immediate marketing action required.")

    except FileNotFoundError:
        print("🚨 System Alert: Critical data file not found. Please check the data pipeline.")
    except pd.errors.EmptyDataError:
        print("🚨 System Alert: The reservation data file is empty. Verify data collection processes.")
    except Exception as e:
        print(f"🚨 System Alert: An unexpected error occurred in the AI Marketing System: {str(e)}")

    print("🏨 Hotel AI Marketing System: Analysis complete. Standing by for further instructions.")

if __name__ == "__main__":
    main()