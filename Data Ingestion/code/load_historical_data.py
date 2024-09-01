'''
Author - Aditya Bhatt 9:58 AM 01-09-2024

TODO : Moving Raw Data To Staging Container

NOTE : Can we make the code better?

BUG :
'''
import pandas as pd
import os

def move_data(source_filepath, filepath):
    
    # Read the CSV file
    data = pd.read_csv(source_filepath)
    
    # Generate the output filename   
    output_filepath = filepath
    
    # Write the data to the staging directory
    data.to_csv(output_filepath, index=False)
    
    print(f"Data moved successfully to {output_filepath}")
    return output_filepath

# Example usage
source_file = "../Raw/Raw_Data_Hotel_Bookings.csv"
file_path = "../Staging/historical_bookings.csv"

moved_file = move_data(source_file, file_path)