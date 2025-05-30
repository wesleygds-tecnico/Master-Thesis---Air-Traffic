# ===============================================================================================================
# Author: Wesley Gonçalves da Silva - IST1105271
# Purpose: This script filters multiple air traffic CSV files by a specified list of aircraft ICAO24 identifiers 
#          and saves the filtered data into a single CSV output. It also performs a safety check by printing 
#          the unique dates associated with each ICAO24 in the filtered data.
# 
# Inputs:
#     - A folder containing one or more `.csv` files with air traffic data.
#     - Each CSV file is expected to contain at least the columns: 'icao24' and 'time'.
#     - A hardcoded list of ICAO24 identifiers (`icao24_to_keep`) which define which aircraft to retain.
# 
# Outputs:
#     - A single CSV file (`air_traffic_output_data_2025-01-14_flight_id_filtered_airframe.csv`) containing 
#       the filtered data, saved to the same input directory.
#     - Console printout of:
#         - The path of each file being processed.
#         - A safety check summary listing each retained ICAO24 and its associated unique flight dates.
# 
# Additional Comments:
#     - The script assumes a Windows-style file path and should be modified for other operating systems.
#     - It uses `pandas` for efficient data manipulation and assumes sufficient memory to handle the combined dataset.
#     - Timestamp parsing assumes that the 'time' column exists and can be converted to a standard datetime format.
#     - Duplicate ICAO24 values in the list are harmless but redundant.
#     - `plt.show()` is present at the end but not used; can be removed unless plotting is added later.
# ===============================================================================================================

import os
import pandas as pd

# Define the folder containing CSV files
input_folder = "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\data\\2025\\2025_01_01-2025_01_14"
#file_path = "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\data\\2025\\2025_01_01-2025_01_14\\air_traffic_output_data_2025-01-14_flight_id.csv"
output_file = os.path.join(input_folder, "air_traffic_output_data_2025-01-14_flight_id_filtered_airframe.csv")

# # List of icao24s to filter
icao24_to_keep = [
    "46b8a9", "46b8ad", "46b8b2", "46b8ac", "46b8a8", "46b8b2",
    "3444c3", "3453c1", "34604d", "346082", "346082", "34604d",
    "392ae9", "3944f2", "392ae7", "3991e0", "392ae8", "3991e7", "3991e0",
    "39e697", "39bda2", 
    "344297", "344217", "344297", "344217", "3453c1", "345215", "347309",
    "347309", "344446", "34750b", "344487", "347309", "3444c3", "3444c3",
    "39e685", "398577", "39bda8", "3950ce", "39e685", "39e685",
    "3986ed", "3986e7", "3986ed", "3986e2", "3986ed", "3986e3", "3986e9",
    "344459", "344446", "344446", "344487", "345218", "344217",
    "344217", "34745a", "347481", "34745a", "347306", "3453c1",
    "4baa8b", "4bb843", "4bc8c5", "4ca8db", "4cad3b", "4cadea"
]  # Replace with actual icao24s

# Create an empty DataFrame to store filtered data
filtered_data = pd.DataFrame()

# Iterate through all CSV files in the folder
for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):  
        file_path = os.path.join(input_folder, file_name)
        print(f"Processing file: {file_path}")

        # Load the CSV file
        df = pd.read_csv(file_path, low_memory=False)

        # Check if 'icao24' column exists
        if "icao24" in df.columns:
            # Filter the DataFrame based on the icao24s list
            filtered_df = df[df["icao24"].isin(icao24_to_keep)]

            # Append the filtered data to the main DataFrame
            filtered_data = pd.concat([filtered_data, filtered_df], ignore_index=True)

# Save the combined filtered data to a new CSV file
if not filtered_data.empty:
    filtered_data.to_csv(output_file, index=False)
    print(f"Filtered data saved to: {output_file}")
    
    # Safety Check: Extract unique icao24s and their respective timestamps (YYYY-MM-DD)
    if "icao24" in filtered_data.columns and "time" in filtered_data.columns:
        # Convert timestamp column to timestamptime format
        filtered_data["time"] = pd.to_datetime(filtered_data["time"], errors='coerce')

        # Extract only the year, month, and day
        filtered_data["time"] = filtered_data["time"].dt.strftime('%Y-%m-%d')

        # Group by icao24 and extract unique dates
        unique_icao24s = filtered_data.groupby("icao24")["time"].unique()

        print("\nSafety Check - icao24s and Their Dates:")
        for icao24, dates in unique_icao24s.items():
            # Convert NumPy array to a list of strings before joining
            date_strings = [str(date) for date in dates]
            print(f"{icao24}: {', '.join(date_strings)}")
    else:
        print("\nWarning: 'date' column not found in the output file.")
else:
    print("No matching icao24s found in the CSV files.")