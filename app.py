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

def competitor_analysis(file_path:str)->pd.DataFrame:
    data=pd.read_csv(file_path)
    data=data[['name','price']]
    print(data.head(10))
    return data.head(10)

def events(file_path:str)->pd.DataFrame:
    data=pd.read_csv(file_path)
    print(data.columns)
    data=data[['title','start_date','description']]
    print(data.head(10))
    return data.head(10)


def get_wheather(file_path:str)->pd.DataFrame:
    data=pd.read_csv(file_path)
    print(data)
    return data
def main():
    print("🏨 Hotel AI Marketing System: Initializing...")
    print("🤖 AI Concierge: Welcome to the Automated Marketing Campaign Management System.")

    try:
        print("📊 AI Data Analyst: Accessing current reservation data...")
        data = pd.read_csv("Data Ingestion/Staging/HotelReservation_dump_2024-09-02.csv")

        print("🧮 AI Occupancy Calculator: Analyzing current occupancy rates...")
        occupancy_rate = calculate_occupancy_rate(data)
        print(f'🏨 Current Hotel Occupancy Rate: {occupancy_rate:.2%}')

        OCCUPANCY_THRESHOLD = 0.75  # 75%

        if occupancy_rate < OCCUPANCY_THRESHOLD:
            print("⚠️ AI Alert System: Low occupancy detected. Initiating marketing campaign protocols.")
            
            print("🤖 AI Campaign Manager: Coming online. Preparing to analyze market trends and previous campaign data.")
            Campaign_Manager = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )
            print("🤖 AI Campaign Manager: Initialization complete. Beginning analysis of previous campaign performance.")

            top_campaigns = analyze_previous_campaigns("Data Ingestion/Staging/prev_campaign.csv")
            if not top_campaigns.empty:
                print("📈 AI Data Analyst: Top 3 Previous Campaigns by Engagement:")
                print(top_campaigns)
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

            print("🚀 AI Campaign Manager: Preparing to launch new marketing initiative. Awaiting final approval.")
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
    get_wheather("Data Ingestion/Staging/gurugram_weather_2024-09-02.csv")