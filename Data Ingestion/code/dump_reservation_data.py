import pyodbc
import pandas as pd
import os
from datetime import date

# Database connection function
def create_connection():
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=DESKTOP-KLL45AE\SQLEXPRESS;'
                          'Database=ADITYADB;'
                          'Trusted_Connection=yes;')
    return conn

# Function to fetch all records from the HotelReservation table
def fetch_all_records(conn):
    query = "SELECT * FROM HotelReservation"
    df = pd.read_sql(query, conn)
    return df

# Function to save the data to a CSV file
def save_to_csv(df, folder_path):
    today = date.today().strftime('%Y-%m-%d')
    file_name = f"HotelReservation_dump_{today}.csv"
    file_path = os.path.join(folder_path, file_name)
    df.to_csv(file_path, index=False)
    return file_path

# Main function
def main():
    # Specify the folder path where you want to save the CSV file
    folder_path = '../Staging/'

    conn = create_connection()
    data = fetch_all_records(conn)
    conn.close()

    # Create folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = save_to_csv(data, folder_path)
    print(f"Data has been successfully dumped to {file_path}")

if __name__ == "__main__":
    main()
