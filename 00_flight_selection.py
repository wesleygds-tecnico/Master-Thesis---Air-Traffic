# ======================================================================================================================================
# Author: Wesley Gonçalves da Silva - IST1105271
# Purpose:
#     This script filters flight tracking data from multiple CSV files within a specified folder, retaining only the records 
#     corresponding to a predefined list of callsigns (representing specific flights of interest).
# 
# Inputs:
#     - A folder path (`input_folder`) containing raw CSV flight data files.
#     - A list of `callsigns_to_keep`, representing the target flights for analysis.
# 
# Outputs:
#     - A single CSV file (`output_file`) named "2025_01_01-2025_01_07_flight_id_filtered.csv" that consolidates all filtered
#       records matching the callsigns of interest.
#     - Console logs including a safety check that displays each unique callsign and the respective dates of its data entries.
# 
# Additional Comments:
#     - This script assumes that each CSV file contains a column named 'callsign'. If the column is missing, that file is skipped.
#     - It also performs a safety check by extracting and printing the dates (in YYYY-MM-DD format) for each retained callsign, 
#       provided the column 'time' is available and in a parseable format.
#     - Useful for tracking, auditing, or analyzing a specific subset of flights in a large dataset.
#     - Be sure to install required packages (`pandas`, etc.) and adjust the path to match your environment.
# =======================================================================================================================================

import os
import pandas as pd

# Define the folder containing CSV files
input_folder = "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\data\\2025\\2025_01_01-2025_01_07-LA"
output_file = os.path.join(input_folder, "2025_01_01-2025_01_07_flight_id_filtered.csv")

# # List of callsigns to filter
# callsigns_to_keep = [
#     "AEA14ZM",
#     "AEA15HY",
#     "AEA16UE",
#     "AEA53HU",
#     "AEA49NA",
#     "AEE6BR",
#     "AFR11FF",
#     "AFR1751",
#     "AFR1795",
#     "AFR32QV",
# ]  # Replace with actual callsigns

callsigns_to_keep = [
    "DM6777", "DW1677",
    "AV103", "AVA103",
    "LA8113", "LAN8113",
    "G37749", "GLO7749",
    "LA4048", "LAN4048",
    "AV102", "AVA102",
    "JJ3455",
    "AD4729", "AZU4729",
    "AV185", "AVA185",
    "G31748", "GLO1748",
    "AD8706", "AZU8706",
    "AM412", "AMX412",
    "VB2272", "VIV2272",
    "AM690", "AMX690",
    "AA411", "AAL411",
    "H85583",
    "AD8708", "AZU8708",
    "JJ8126",
    "G31749", "GLO1749",
    "AD4577", "AZU4577",
    "LP2386",
    "AV160", "AVA160",
    "CM358", "CMP358",
    "AV93", "AVA93",
    "DL269", "DAL269",
    "AD4787", "AZU4787",
    "AD2462", "AZU2462",
    "JJ3403",
    "DL227", "DAL227",
    "LA4902", "LAN4902",
    "AV49", "AVA49",
    "DM6765", "DWI6765",
    "LA500", "LAN500",
    "AD8708", "AZU8708",
    "AD4074", "AZU4074",
    "AA907", "AAL907",
    "UA129", "UAL129",
    "AD8713", "AZU8713",
    "AV235", "AVA235",
    "LP2402",
    "AV112", "AVA112",
    "Y43912", "VOI3912",
    "AV268", "AVA268",
    "CM260", "CMP260",
    "AD4598", "AZU4598",
    "OB762", "BOV762",
    "AD8722", "AZU8722",
    "AV256", "AVA256",
    "AV220", "AVA220",
    "CM816", "CMP816",
    "AV24", "AVA24",
    "AD8703", "AZU8703",
    "AD2423", "AZU2423",
    "G31150", "GLO1150",
    "AD2925", "AZU2925",
    "AD2928", "AZU2928",
    "AV25", "AVA25",
    "AD8712", "AZU8712",
    "AV98", "AVA98",
    "LA575", "LAN575",
    "AD2437", "AZU2437",
    "AD2569", "AZU2569",
    "2K8392",
    "LP2459",
    "LA2450", "LPE2450",
    "AV54", "AVA54",
    "AV647", "LRC647",
    "LP2471",
    "G37716", "GLO7716",
    "LP2411",
    "H85554",
    "AD4577", "AZU4577",
    "AD2576", "AZU2576",
    "JJ4680",
    "AD4163", "AZU4163",
    "G37718", "GLO7718",
    "AD4084", "AZU4084",
    "AD4070", "AZU4070",
    "AD8703", "AZU8703",
    "AD4681", "AZU4681",
    "G31761", "GLO1761",
    "AD4076", "AZU4076",
    "G31548", "GLO1548",
    "JJ3865",
    "JJ3207",
    "AD2458", "AZU2458",
    "5Y57", "GTI057",
    "H85141",
    "LA2012", "LPE2012",
    "JJ3014",
    "AD4013", "AZU4013",
    "AV197", "AVA197",
    "H85581",
    "AV95", "AVA95",
    "AV7", "AVA7",
    "LA4228", "LAN4228",
    "UA1675", "UAL1675",
    "DM6086", "DWI6086",
    "LA3807", "TAM3807",
    "AD4013", "AZU4013"
]

# Create an empty DataFrame to store filtered data
filtered_data = pd.DataFrame()

# Iterate through all CSV files in the folder
for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):  
        file_path = os.path.join(input_folder, file_name)
        print(f"Processing file: {file_path}")

        # Load the CSV file
        df = pd.read_csv(file_path, low_memory=False)

        # Check if 'callsign' column exists
        if 'callsign' in df.columns:
            # Filter the DataFrame based on the callsigns list
            filtered_df = df[df["callsign"].isin(callsigns_to_keep)]

            # Append the filtered data to the main DataFrame
            filtered_data = pd.concat([filtered_data, filtered_df], ignore_index=True)

# Save the combined filtered data to a new CSV file
if not filtered_data.empty:
    filtered_data.to_csv(output_file, index=False)
    print(f"Filtered data saved to: {output_file}")
    
    # Safety Check: Extract unique callsigns and their respective timestamps (YYYY-MM-DD)
    if "callsign" in filtered_data.columns and "time" in filtered_data.columns:
        # Convert timestamp column to timestamptime format
        filtered_data["time"] = pd.to_datetime(filtered_data["time"], errors='coerce')

        # Extract only the year, month, and day
        filtered_data["time"] = filtered_data["time"].dt.strftime('%Y-%m-%d')

        # Group by callsign and extract unique dates
        unique_callsigns = filtered_data.groupby("callsign")["time"].unique()

        print("\nSafety Check - Callsigns and Their Dates:")
        for callsign, dates in unique_callsigns.items():
            # Convert NumPy array to a list of strings before joining
            date_strings = [str(date) for date in dates]
            print(f"{callsign}: {', '.join(date_strings)}")
    else:
        print("\nWarning: 'date' column not found in the output file.")
else:
    print("No matching callsigns found in the CSV files.")