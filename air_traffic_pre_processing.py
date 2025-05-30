# ===============================================================================================================
# Author: Wesley Gonçalves da Silva - IST1105271
# Purpose:
#     This script processes raw air traffic data to clean invalid timestamps,
#     resample the data, assign unique flight IDs, and export the result to a new CSV file.
#     It supports data from OpenSky and FlightRadar24 (comment/uncomment as needed).
# 
# Inputs:
#     - A CSV file containing air traffic data, including flight identifiers, positions,
#       timestamps, and other flight parameters.
#       Input path:
#       "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\data\\2025\\2025_01_08-2025_01_14\\air_traffic_output_data_2025-01-14.csv"
# 
# Outputs:
#     - A resampled and cleaned CSV file, containing data with assigned flight IDs.
#       Output path:
#       "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\data\\2025\\2025_01_08-2025_01_14\\air_traffic_output_data_2025-01-14_flight_id.csv"
# 
# Additional Notes:
#     - The script uses the `traffic` Python library to manage air traffic data.
#     - Data can be toggled between OpenSky and FlightRadar24 sources by commenting/uncommenting
#       the appropriate sections (notably datetime conversions, ID assignments, and output columns).
#     - Invalid timestamp rows are filtered out before processing.
#     - Memory is managed efficiently by clearing intermediate objects.
#     - tqdm is used to visualize processing progress.
# ===============================================================================================================

import pandas as pd
from traffic.core import Traffic  # Assuming you're using the `traffic` library
from tqdm import tqdm

# Inputs and outputs
input_file = "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\data\\2025\\2025_01_08-2025_01_14\\air_traffic_output_data_2025-01-14.csv"
output_files = {
    "5s": "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\data\\2025\\2025_01_08-2025_01_14\\air_traffic_output_data_2025-01-14_flight_id.csv",
}

# Load the CSV file
print('Load the CSV file \n') 
df = pd.read_csv(input_file, low_memory=False)

# Attempt to convert the timestamp column to datetime, marking invalid rows as NaT - OpenSky
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# # Attempt to convert the timestamp column to datetime, marking invalid rows as NaT - Flight Radar 24
# df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Identify and display rows with invalid timestamps
invalid_rows = df[df['timestamp'].isna()]
if not invalid_rows.empty:
    print("Invalid timestamp rows:")
    print(invalid_rows)

# Remove rows with invalid timestamps
df = df.dropna(subset=['timestamp'])

# Convert the timestamp column to datetime - OpenSky
df['timestamp'] = pd.to_datetime(df['timestamp'])

# # Convert the timestamp column to datetime - Flight Radar 24
# df['timestamp'] = pd.to_datetime(df['timestamp'])

# Optional: Reset the index after dropping rows
df.reset_index(drop=True, inplace=True)

# Create a Traffic object
traffic_data = Traffic(df)

del df  # Clear memory

# Loop through each resampling rule
for rule, output_file in tqdm(output_files.items(), desc="Processing flights", unit="flight"):
    # Resample data - OpenSky
    resampled_traffic_data = traffic_data.resample(rule=rule)

    # Assign unique IDs to flights - OpenSky
    resampled_traffic_data = resampled_traffic_data.assign_id().eval()

    # # Assign unique IDs to flights - Flight Radar 24
    # resampled_traffic_data = traffic_data.assign_id().eval()    

    # Save to CSV - OpenSky
    resampled_traffic_data.data[['icao24', 'callsign', 'timestamp', 'latitude', 'longitude', 'altitude',
                                 'vertical_rate', 'groundspeed', 'flight_id', 'track']].to_csv(output_file, index=False)

    # # Save to CSV - Flight Radar 24
    # resampled_traffic_data.data[['icao24','timestamp','callsign','latitude','longitude',
    #                              'altitude','groundspeed','heading','altitude_m','pressure_hPa',
    #                              'u_wind','v_wind','heading_rad','GS_x','GS_y','true_airspeed', 
    #                              'flight_id']].to_csv(output_file, index=False)    

    # Clear memory for the current sample
    del resampled_traffic_data