# ========================================================================================================================
# Author: Wesley Gonçalves da Silva - IST1105271
# Purpose:
#     This script retrieves historical air traffic data from the OpenSky Network API
#     for predefined geographical areas over specified time intervals. It collects
#     flight information such as position, altitude, velocity, and heading, filters
#     flights above 5000 feet altitude, and saves the combined data incrementally to
#     a CSV file.
#
# Inputs:
#     - Predefined geographic bounding boxes (longitude and latitude limits) for
#       multiple airspace areas.
#     - Start and end timestamps defining the time range for data retrieval.
#     - Output CSV filename to store retrieved flight data.
#
# Outputs:
#     - CSV file containing the filtered air traffic data for all specified areas and
#       time intervals, with columns including icao24, callsign, timestamp, latitude,
#       longitude, barometric altitude, geometric altitude, vertical rate, velocity,
#       and heading.
#
# Additional Comments:
#     - The script resumes data retrieval from the last recorded timestamp if the
#       output file exists and is not empty, enabling incremental data updates.
#     - It uses 10-minute intervals to partition the data requests for manageable
#       retrieval.
#     - Error handling is included to catch and report API request issues per area.
#     - Flights below 5000 ft altitude are filtered out to focus on relevant traffic.
#     - The "traffic" package's OpenSky interface is required for API access.
#     - The code contains commented out alternative area definitions and timing
#       settings for flexibility.
#     - The tqdm import is present but not used; it could be integrated for progress
#       bars in future enhancements.
#     - The final plt.show() is called but no matplotlib plots are defined; this can
#       be removed or replaced with actual visualization code.
# ========================================================================================================================

import os
import pandas as pd
from tqdm import tqdm
from traffic.data import opensky

# Define the geographical areas bounds | (lon_min, lat_min, lon_max, lat_max) Necessariamente nessa ordem

# areas = {
#     "AREA_1": [lon_min = -25, lon_max = -11, lat_max = 40, lat_min = 18],
#     "AREA_2": [lon_min = -11, lon_max =  33, lat_max = 53, lat_min = 25], # (lon_min, lon_max, lat_max, lat_min)
#     "AREA_3": [lon_min = -25, lon_max = -11, lat_max = 75, lat_min = 40],
#     "AREA_4": [lon_min = -11, lon_max =  33, lat_max = 75, lat_min = 53],
#     "AREA_5": [lon_min =  33, lon_max =  51, lat_max = 48, lat_min = 30],
#     "AREA_6": [lon_min =  33, lon_max =  42, lat_max = 53, lat_min = 48],
# }

# Order to retrieve the proper geographfical domain - (lon_min, lat_min, lon_max, lat_max)
areas = {
    "AREA_1":   (-25, 18, -11, 40,),
    "AREA_2_1": (-11, 25,  11, 53,),
    "AREA_2_2": (11, 25,  33, 53,),
    "AREA_3":   (-25, 40, -11, 75,),
    "AREA_4":   (-11, 53,  33, 75,),
    "AREA_5":   ( 33, 30,  51, 48,),
    "AREA_6":   ( 33, 48,  42, 53,),    
}

## Define the airspace regions with the correct format [min lon, max lon, max lat, min lat]
#areas = {
#    "Area_1":   [-100,  0,  -85,    30, ],
#    "Area_21":  [-85,   10 ,  -55,    30, ],
#    "Area_22":  [-55,   -5 ,  -30,    15, ],
#    "Area_3":   [-85,   -20,  -55,    -5, ],
#    "Area_4":   [-85,   -30,  -30,    -20,],
#    "Area_5":   [-85,   -5 ,  -55,    10, ],
#    "Area_6":   [-55,   -20,  -30,    -5, ],
#}

# Define the time interval for each assessment
time_interval = pd.Timedelta(minutes=10)

# Define the output filename
output_filename = "air_traffic_output_data_2025-01-14.csv"

# Check if the file exists and get the last registered time
if os.path.exists(output_filename) and os.path.getsize(output_filename) > 0:
    # Read the last row from the file
    last_row = pd.read_csv(output_filename, low_memory=False).tail(1)
    last_time = pd.to_datetime(last_row['timestamp'].iloc[0])  # Ensure the 'time' column exists
    current_start = last_time
    first_iteration = False
    print(f"Resuming from the last recorded time: {current_start}")
else:
    # File does not exist or is empty, set the starting time to the predefined time
    start_day = "2025-01-14"
    current_start = pd.Timestamp(f"{start_day}T00:00:00+00:00")
    print(f"Starting from {current_start}")

# File does not exist or is empty, set the starting time to the predefined time
# start_day = "2024-01-01"
# current_start = pd.Timestamp(f"{start_day}T11:10:00+00:00")    

first_iteration = False

end_day = "2025-01-15"
end_time = pd.Timestamp(f"{end_day}T00:00:00+00:00")

# Initialize loop variables
first_iteration = True

# Loop through the time intervals and regions
while current_start < end_time:
    current_stop = current_start + time_interval

    # Iterate over each area
    for area_name, bounds in areas.items():
        lon_min, lat_min, lon_max, lat_max = bounds

        print(f"Fetching data for {area_name} from {current_start} to {current_stop}...")

        # Fetch history for the current area and time interval
        try:
            traffic_data = opensky.history(
                start=current_start.isoformat(),
                stop=current_stop.isoformat(),
                bounds=(lon_min, lat_min, lon_max, lat_max),  # Use area-specific bounds
                selected_columns=[
                    "icao24", "callsign", "time", "lat", "lon",
                    "baroaltitude", "geoaltitude", "vertrate",
                    "velocity", "heading"
                ]
            )

            # Convert Traffic object to pandas DataFrame
            if traffic_data is not None and traffic_data.data is not None:
                history_df = traffic_data.data

                # Filter flights with aircraft altitude above 5000ft
                history_df = history_df[history_df["altitude"] > 5000]  # or "geoaltitude" if preferred           

                # Append results to the common output file if DataFrame is not empty
                if not history_df.empty:
                    history_df.to_csv(
                        output_filename,
                        mode="a",  # Append mode
                        header=first_iteration,  # Write header only on the first iteration
                        index=False
                    )
                    first_iteration = False                                   
                
                # else:
                #     print(f"No data available for {area_name} in the interval {current_start} to {current_stop}.")
            # else:
            #     print(f"No data available for {area_name} in the interval {current_start} to {current_stop}.")

        except Exception as e:
            print(f"An error occurred while fetching data for {area_name}: {e}")

    # Move to the next time interval
    current_start = current_stop

    # Wait before the next request
    # time.sleep(0.1)

print("Data retrieval complete.")