# ===============================================================================================================
# Author: Wesley Gonçalves da Silva - IST1105271
# Purpose:
#     This script retrieves historical aircraft trajectory data from the OpenSky 
#     Network API using the `traffic` library. It specifically targets a user-defined 
#     geographical area and filters for flights with specific callsigns and a minimum 
#     altitude, saving the result into a CSV file.
#
# Inputs:
#     - Geographical bounding boxes defined in the `areas` dictionary.
#     - Specific flight callsigns in the `specific_callsign` list.
#     - Start and end timestamps for data collection.
#     - Time interval (in minutes) to iterate through for each data fetch window.
#
# Outputs:
#     - A CSV file named `VL2090_2025-01-24.csv` containing filtered flight data
#       that matches the specified callsigns and altitude requirements.
#
# Additional Comments:
#     - This script uses the `opensky.history()` method to pull historical ADS-B data.
#     - Only one area is currently active ("AREA_2") but others are listed for flexibility.
#     - The script supports restarting from a previously saved file (commented out in this version).
#     - It filters flights with altitude above 5000 ft to avoid irrelevant data on the ground.
#     - The `traffic` library must be installed, and OpenSky's rate-limiting should be considered 
#       for large-scale data collection.
#     - The final `plt.show()` line appears to be leftover or unused since no matplotlib plots
#       are generated in the current script and could be removed.
# ===============================================================================================================

import os
import time
import pandas as pd
from traffic.data import opensky

# Order to retrieve the proper geographfical domain - (lon_min, lat_min, lon_max, lat_max)
areas = {
    #"AREA_1": (-25, 18, -11, 40,),
    "AREA_2": (-11, 25,  33, 53,),
    #"AREA_3": (-25, 40, -11, 75,),
    #"AREA_4": (-11, 53,  33, 75,),
    #"AREA_5": ( 33, 30,  51, 48,),
    #"AREA_6": ( 33, 48,  42, 53,),    
}

specific_callsign = [
    'LHX2090', 
    'VL2090',
    # 'EN8281', # DLA2CF
    # 'DLA2CF',
    # 'LG6991',
    # 'LGL691M',
    # 'LG6991',
    # 'LGL691M'
]

time_interval = pd.Timedelta(minutes=10)
#loop_interval = 0.1  # Interval between API requests in seconds

# Initialize loop variables
first_iteration = True

# Define the output filename
output_filename = "VL2090_2025-01-24.csv"

# Check if the file exists and get the last registered time
# if os.path.exists(output_filename) and os.path.getsize(output_filename) > 0:
#     # Read the last row from the file
#     last_row = pd.read_csv(output_filename).tail(1)
#     last_time = pd.to_datetime(last_row['timestamp'].iloc[0])  # Ensure the 'time' column exists
#     current_start = last_time
#     first_iteration = False
#     print(f"Resuming from the last recorded time: {current_start}")
# else:
#     # File does not exist or is empty, set the starting time to the predefined time
#     start_day = "2024-01-01"
#     current_start = pd.Timestamp(f"{start_day}T00:00:00+00:00")
#     first_iteration = True
#     print(f"Starting from {current_start}")

start_day = "2025-01-24"
current_start = pd.Timestamp(f"{start_day}T06:30:00+00:00")    
first_iteration = True

# Define the end time (you can adjust this as needed)
end_day = "2025-01-24"
end_time = pd.Timestamp(f"{end_day}T08:00:00+00:00")

while current_start < pd.to_datetime(end_time):
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
                    "velocity"
                ]
            )
            # Convert Traffic object to pandas DataFrame
            if traffic_data is not None and traffic_data.data is not None:
                history_df = traffic_data.data.copy()  # Make a copy to avoid modifying the original object

                # Apply the callsign filter if needed
                if specific_callsign:
                    # Ensure specific_callsign is a list for filtering
                    if isinstance(specific_callsign, str):
                        specific_callsign = [specific_callsign]

                    # Filter the DataFrame based on callsign
                    filtered_df = history_df[history_df["callsign"].isin(specific_callsign)]

                    # Further filter flights with aircraft altitude above 5000 ft
                    filtered_df = filtered_df[filtered_df["altitude"] > 5000]  # or "geoaltitude" if preferred

                    # Check if filtered DataFrame is empty
                    if not filtered_df.empty:
                        # Write filtered data to the output file
                        filtered_df.to_csv(
                            output_filename,
                            mode="a",  # Append mode
                            header=first_iteration,  # Write header only on the first iteration
                            index=False
                        )
                        # Print success message
                        print(f"Filtered data for callsign(s) {specific_callsign} appended to {output_filename}.")
                    
                        # Update the flag to avoid writing headers multiple times
                        first_iteration = False

                    else:
                        # No data available for the given callsign or altitude threshold
                        print(f"No data available for callsign(s) {specific_callsign} above 5000 ft in the interval {current_start} to {current_stop}.")
            else:
                print("No specific callsign provided for filtering.")
        
        except Exception as e:
            print(f"An error occurred while fetching data for {area_name}: {e}")

    # Move to the next interval
    current_start = current_stop

    # Wait before the next request
    #time.sleep(loop_interval)

print("Data retrieval complete.")
