# ========================================================================================================================
# Author: Wesley Gonçalves da Silva - IST1105271
# Purpose:
#     This script processes multiple flight data CSV files from a specified folder,
#     combines them into a single DataFrame, cleans and converts some data columns,
#     assigns unique flight IDs using the Traffic library, and finally saves the 
#     processed data into a new CSV file.
# 
# Inputs:
#     - folder_path: Path to the folder containing multiple CSV files with flight data.
#     Each CSV file is expected to have columns including 'timestamp' and 'altitude'.
#     
# Outputs:
#     - A single CSV file combining all input CSV files, with cleaned and standardized data,
#       and with unique flight IDs assigned, saved at the specified output_file path.
# 
# Additional Comments:
#     - The 'timestamp' column is converted to pandas datetime format for consistency.
#     - The 'altitude' values are converted from feet to meters by multiplying by 0.3048.
#     - The Traffic library (from traffic.core) is used to assign unique IDs to individual flights.
#     - This script assumes all CSV files in the folder are compatible and have consistent structure.
#     - The print statement references a variable 'new_file_name' which should be updated to 'output_file' to avoid errors.
#     - The plt.show() at the end is included but no plot is generated in this code snippet; it may be unnecessary.
# ========================================================================================================================


from traffic.core import Traffic  # Assuming you're using the `traffic` library
import pandas as pd
import os

# Set the folder path containing your .csv files
folder_path = "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\data\\2025\\2025_01_01-2025_01_07-LA\\flightradar24"  # change this to your folder path
output_file = "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\data\\2025\\2025_01_01-2025_01_07-LA\\flightradar24\\2025_01_01-2025_01_07_LA_flight_id.csv"  # change this to your folder path

# Get all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Initialize an empty list to store individual dataframes
df_list = []

# Loop through each file and read it into a DataFrame
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    df_list.append(df)

# Combine all DataFrames into one
combined_df = pd.concat(df_list, ignore_index=True)

# Display the combined DataFrame
print(combined_df.head())

# Convert the timestamp column to datetime - OpenSky
combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'])

combined_df['altitude'] = combined_df['altitude']*0.3048

# Create a Traffic object
traffic_data = Traffic(combined_df)

# Assign unique IDs to flights - OpenSky
traffic_data = traffic_data.assign_id().eval()

# Save the combined DataFrame to a new .csv file
traffic_data.to_csv(output_file, index=False)

