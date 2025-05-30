# ===============================================================================================================
# Author: Wesley Gonçalves da Silva - IST1105271
# Purpose:
#     This script processes ADS-B flight trajectory data to clean, validate, and prepare it for further analysis. 
#     It focuses on removing noise and outliers in key flight parameters such as altitude, vertical rate, and groundspeed, 
#     as well as filtering flights based on duration and timestamp integrity.
# 
# Inputs:
#     - CSV file containing ADS-B flight data with the following expected columns:
#       ['flight_id', 'timestamp', 'latitude', 'longitude', 'altitude', 'vertical_rate', 'groundspeed']
#     - Input path is defined by the variable `folder_path`
# 
# Outputs:
#     - Cleaned and validated DataFrame (`cleaned_df`) ready for further use.
#     - This DataFrame is optionally saved or returned for further use (e.g., through export or traffic library operations).
# 
# Key Processing Steps:
#     1. **Load Data**: Reads the data from a single CSV file (code includes commented-out logic for reading multiple files).
#     2. **Timestamp Conversion**: Ensures timestamps are in datetime format and filters out rows with invalid timestamps.
#     3. **Flight Filtering**: Only includes flights that last at least 10 minutes.
#     4. **Coordinate and Altitude Validation**: Identifies and removes physically invalid latitude, longitude, and altitude values.
#     5. **Outlier Detection**: Applies multiple passes of peak detection to identify outliers in altitude, vertical rate, and groundspeed using `scipy.signal.find_peaks`.
#     6. **Interpolation**: Replaces detected outliers with NaNs and then applies linear interpolation to fill missing values.
#     7. **Sorting**: Ensures data is time-ordered per flight ID for accuracy.
# 
# Additional Notes:
#     - Uses both peak detection and distance-based criteria for robust outlier removal.
#     - Makes heavy use of pandas for data handling and NumPy for numerical operations.
#     - Placeholder and commented sections for future integration with the `Traffic` library from pyModeS or traffic libraries.
#     - Code is designed for batch processing and scalable for larger datasets.
#     - Visualization (plotting) sections are included but currently commented out.
# 
# Caution:
#     - Some file paths are hard-coded and specific to the author’s local system.
#     - Future warnings from pandas are suppressed for clarity.
#     - Output saving is not included in the final cleaned version (you may export `cleaned_df` manually).
# ===============================================================================================================


import os
import pandas as pd
from geopy.distance import geodesic
import numpy as np
from scipy.signal import find_peaks
import warnings

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

output_file = "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\data\\2025\\2025_01_01-2025_01_14\\2025-01-01_2025-01-14_flight_id_filtered_airframe_checked.csv"
folder_path = "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\data\\2025\\2025_01_01-2025_01_14\\2025-01-01_2025-01-14_flight_id_filtered_airframe.csv"

# Initialize an empty list to store dataframes
dataframes = []

# # Iterate over all files in the folder
# for file_name in os.listdir(folder_path):
#     
# 
#     ## Check if the file is a CSV
#     #if file_name.endswith(".csv"):
#     #    file_path = os.path.join(folder_path, file_name)  # Get the full file path
#     #    print(f"Processing file: {file_path}")
#     #    
#     #    # Read the CSV file into a pandas DataFrame
#     #    df = pd.read_csv(file_path, low_memory=False)
#     #    
#     #    # Append the dataframe to the list
#     #    dataframes.append(df)

combined_df = pd.read_csv(folder_path, low_memory=False)
print(f"Processing file: {folder_path}")

print('Data extraction concluded! \n')

# # Concatenate all dataframes into a single DataFrame
# combined_df = pd.concat(dataframes, ignore_index=True)

# Ensure timestamp is in datetime format
combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'], errors='coerce')

# Calculate flight duration (assuming each row corresponds to a flight event)
flight_durations = combined_df.groupby("flight_id")["timestamp"].agg(["min", "max"])
flight_durations["duration"] = (flight_durations["max"] - flight_durations["min"]).dt.total_seconds() / 60  # Convert to minutes

# Keep flights with a duration >= 10 minutes
valid_flights = flight_durations[flight_durations["duration"] >= 10].index  

# Filter the original DataFrame to keep only valid flights
filtered_df = combined_df[combined_df["flight_id"].isin(valid_flights)]

# Reset index (optional)
combined_df = filtered_df.reset_index(drop=True)

# Identify and display rows with invalid timestamps
invalid_rows = combined_df[combined_df['timestamp'].isna()]
if not invalid_rows.empty:
    print("Invalid timestamp rows:")
    print(invalid_rows)

# Remove rows with invalid timestamps
combined_df = combined_df.dropna(subset=['timestamp'])

# Optional: Reset the index after dropping rows
combined_df.reset_index(drop=True, inplace=True)

# # Create a Traffic object
# traffic_data = Traffic(combined_df)

# # Assign unique IDs to flights
# combined_df = traffic_data.assign_id().eval()

# # Resample data
# combined_df = combined_df.resample(rule='5s')

# # Transform the Traffic object back to a pandas DataFrame
# combined_df = combined_df.data

# Sort the DataFrame by 'flight_id' and 'timestamp'
print('Sort the DataFrame by flight_id and timestamp \n')
combined_df = combined_df.sort_values(by=["flight_id", "timestamp"]).reset_index(drop=True)

# Initialize a list to store inconsistent flight_ids
inconsistent_flight_ids = set()  # Use a set to avoid duplicates

# # Check for missing values
# missing_values = combined_df.isnull().sum()
# if missing_values.any():
#     print("Missing values:\n", missing_values)
#     combined_df.loc[combined_df.isnull().any(axis=1), :] = combined_df.loc[combined_df.isnull().any(axis=1), :].fillna(np.nan)

# Check for invalid latitude and longitude values
print('Check for invalid latitude and longitude values \n')
invalid_lat = (combined_df['latitude'] < -90) | (combined_df['latitude'] > 90)
invalid_lon = (combined_df['longitude'] < -180) | (combined_df['longitude'] > 180)

combined_df.loc[invalid_lat, 'latitude'] = np.nan
combined_df.loc[invalid_lon, 'longitude'] = np.nan

if invalid_lat.any():
    print(f"Invalid latitude records corrected: {invalid_lat.sum()}")
if invalid_lon.any():
    print(f"Invalid longitude records corrected: {invalid_lon.sum()}")

# Check for invalid altitude values
invalid_altitude_low = combined_df['altitude'] < 0
invalid_altitude_high = combined_df['altitude'] > 14e+3

combined_df.loc[invalid_altitude_low | invalid_altitude_high, 'altitude'] = np.nan

if invalid_altitude_low.any() or invalid_altitude_high.any():
    print(f"Invalid altitude records corrected: {(invalid_altitude_low | invalid_altitude_high).sum()}")

# Define different distance thresholds for each attribute
print('Outliners identification and elimination \n')
distance_thresholds = {
    "altitude": 8,         # Adjust based on data behavior
    "vertical_rate": 1000,    # Adjust based on expected vertical rate peaks
    "groundspeed": 1000       # Adjust to detect meaningful peaks in speed
}

# Group by flight_id
grouped = combined_df.groupby("flight_id")

# Iterate through each flight_id
for flight_id, group in grouped:
    # Sort by timestamp
    group = group.sort_values(by="timestamp")

    # Iterate through each attribute and apply peak detection
    for column, distance_threshold in distance_thresholds.items():
        if column in group.columns:
            data = group[column].values

            # Find peaks (local maxima)
            # peaks_max, _ = find_peaks(data, distance=distance_threshold)

            # Find valleys (local minima) by inverting the data
            # peaks_min, _ = find_peaks(-data, distance=distance_threshold)

            # Find peaks (outliers) as before
            peaks_max1, _ = find_peaks(data,    prominence=5, width=1)
            peaks_min1, _ = find_peaks(-data,   prominence=5, width=1)
            
            # Criteria 2: Lower prominence and smaller width to catch subtler peaks
            peaks_max2, _ = find_peaks(data,    distance = distance_threshold)
            peaks_min2, _ = find_peaks(-data,   distance = distance_threshold)

            # Criteria 3: Even lower thresholds (if necessary)
            peaks_max3, _ = find_peaks(data,    prominence=5, width=1)
            peaks_min3, _ = find_peaks(-data,   prominence=5, width=1)            
            
            # Combine all detected indices
            all_peaks = np.concatenate((peaks_max1, peaks_min1, peaks_max2, peaks_min2, peaks_max3, peaks_min3))
            all_peaks = np.unique(all_peaks)  # Remove any duplicates and sort the indices

            # Plot the attribute with detected peaks and valleys
            # plt.figure(figsize=(10, 5))
            # plt.plot(group["timestamp"], data, label=f"{column} over time", marker='.')
            # plt.scatter(group["timestamp"].iloc[peaks_max1], data[peaks_max1], color='red', label="Max Peaks", zorder=3)
            # plt.scatter(group["timestamp"].iloc[peaks_min1], data[peaks_min1], color='blue', label="Min Peaks", zorder=3)
            # plt.scatter(group["timestamp"].iloc[peaks_max2], data[peaks_max2], color='red', label="Max Peaks", zorder=3)
            # plt.scatter(group["timestamp"].iloc[peaks_min2], data[peaks_min2], color='blue', label="Min Peaks", zorder=3)
            # plt.scatter(group["timestamp"].iloc[peaks_max3], data[peaks_max3], color='red', label="Max Peaks", zorder=3)
            # plt.scatter(group["timestamp"].iloc[peaks_min3], data[peaks_min3], color='blue', label="Min Peaks", zorder=3)            

            # plt.title(f"{column} peaks for Flight {flight_id}")
            # plt.xlabel("Timestamp")
            # plt.ylabel(column)
            # plt.legend()
            # plt.grid()
            # plt.xticks(rotation=45)
            # plt.show()

# Copy the original DataFrame to avoid modifying it directly
cleaned_df = combined_df.copy()

distance_thresholds = {
    "altitude": 2,         # Adjust based on data behavior
    "vertical_rate": 1000,    # Adjust based on expected vertical rate peaks
    "groundspeed": 1000       # Adjust to detect meaningful peaks in speed
}

# Group by flight_id
grouped = cleaned_df.groupby("flight_id")

# Iterate through each flight_id
for flight_id, group in grouped:
    # Sort by timestamp
    group = group.sort_values(by="timestamp")

    for column, distance_threshold in distance_thresholds.items():
        if column in group.columns:
            data = group[column].values

            # Find peaks (outliers) as before
            peaks_max1, _ = find_peaks(data,    prominence=5, width=1)
            peaks_min1, _ = find_peaks(-data,   prominence=5, width=1)
            
            # Criteria 2: Lower prominence and smaller width to catch subtler peaks
            peaks_max2, _ = find_peaks(data,    distance = distance_threshold)
            peaks_min2, _ = find_peaks(-data,   distance = distance_threshold)

            # Criteria 3: Even lower thresholds (if necessary)
            peaks_max3, _ = find_peaks(data,    prominence=5, width=3)
            peaks_min3, _ = find_peaks(-data,   prominence=5, width=3)            
            
            # Combine all detected indices
            all_peaks = np.concatenate((peaks_max1, peaks_min1, peaks_max2, peaks_min2, peaks_max3, peaks_min3))
            all_peaks = np.unique(all_peaks)  # Remove any duplicates and sort the indices

            # Replace outlier values with NaN
            cleaned_df.loc[group.index[all_peaks], column] = np.nan

    # Interpolate missing values
    cleaned_df.loc[group.index] = cleaned_df.loc[group.index].interpolate(method='linear', limit_direction='both')


for flight_id, group in cleaned_df.groupby("flight_id"):
    group = group.sort_values(by="timestamp")
    for column, distance_threshold in distance_thresholds.items():
        if column in group.columns:
            data = group[column].values
            # Here, we use a simpler criteria: detect any remaining peaks (both maxima and minima)
            # Find peaks (outliers) as before
            peaks_max1, _ = find_peaks(data,    prominence=2, width=2)
            peaks_min1, _ = find_peaks(-data,   prominence=2, width=2)
            
            # Criteria 2: Lower prominence and smaller width to catch subtler peaks
            peaks_max2, _ = find_peaks(data,    distance = 0.5*distance_threshold)
            peaks_min2, _ = find_peaks(-data,   distance = 0.5*distance_threshold)

            # Criteria 3: Even lower thresholds (if necessary)
            peaks_max3, _ = find_peaks(data,    prominence=2, width=3)
            peaks_min3, _ = find_peaks(-data,   prominence=2, width=3)            
            
            # Combine all detected indices
            all_peaks = np.concatenate((peaks_max1, peaks_min1, peaks_max2, peaks_min2, peaks_max3, peaks_min3))
            all_peaks = np.unique(all_peaks)  # Remove any duplicates and sort the indices
            
            # If any peaks are still detected, mark them as NaN
            if len(all_peaks) > 0:
                cleaned_df.loc[group.index[all_peaks], column] = np.nan
                
    # Interpolate once more to fill any gaps created in this second pass
    cleaned_df.loc[group.index] = cleaned_df.loc[group.index].interpolate(method='linear', limit_direction='both')

# For each flight_id, iterate over its groups and apply interpolation to replace outliers
for flight_id, group in cleaned_df.groupby('flight_id'):
    # Plotting the original attribute vs. timestamp for the flight_id
    for attribute, color, title, ylabel in [
        ('altitude', 'b', 'Altitude', 'Altitude (ft)'),
        ('vertical_rate', 'g', 'Vertical Rate', 'Vertical Rate (ft/min)'),
        ('groundspeed', 'r', 'Groundspeed', 'Groundspeed (kts)')
    ]:
        # # Plot the attribute
        # plt.figure(figsize=(10, 5))
        # plt.plot(group['timestamp'], group[attribute], label=f'{attribute}', color=color)

        # Highlight the detected peaks and valleys (outliers replaced with interpolated values)
        peaks = group[group[attribute].isna() == False][attribute]  # Ensure only valid points are included
        # plt.scatter(group['timestamp'], peaks, color='b', label='Interpolated Values', zorder=5, s=2)  # Smaller size points

        # Add titles, labels, and grid
        # plt.title(f'{title} for flight {flight_id}')
        # plt.xlabel("Timestamp")
        # plt.ylabel(ylabel)
        # plt.legend()
        # plt.grid(True)
 
        # Display the plot
        # plt.tight_layout()
        # plt.show()

# Check for invalid groundspeed values
invalid_groundspeed = (cleaned_df['groundspeed'] < 0) | (cleaned_df['groundspeed'] > 900)

cleaned_df.loc[invalid_groundspeed, 'groundspeed'] = np.nan

if invalid_groundspeed.any():
    print(f"Invalid groundspeed records corrected: {invalid_groundspeed.sum()}")

# Check for invalid callsigns
invalid_callsign = cleaned_df[cleaned_df['callsign'].str.match(r'^\s*$') | cleaned_df['callsign'].isnull()]
print("Invalid callsigns:\n", invalid_callsign)

if not invalid_callsign.empty:
    inconsistent_flight_ids.update(invalid_callsign['flight_id'].unique())

# Check for duplicate rows and drop them
duplicate_rows = cleaned_df.duplicated()

if duplicate_rows.any():
    print(f"Duplicate rows dropped: {duplicate_rows.sum()}")
    cleaned_df = cleaned_df[~duplicate_rows].reset_index(drop=True)

def replace_repeated_lat_lon_with_nan(df):
    """
    Identifies rows with repeated latitude and longitude values in consecutive rows
    and replaces the repeated values with NaN.

    Args:
        df (pd.DataFrame): The input dataframe with 'latitude' and 'longitude' columns.

    Returns:
        pd.DataFrame: The dataframe with repeated latitude and longitude values replaced by NaN.
    """
    # Check if 'latitude' and 'longitude' columns exist
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        raise ValueError("The dataframe must contain 'latitude' and 'longitude' columns.")
    
    # Identify rows where latitude or longitude is repeated compared to the previous row
    repeated_mask = (df['latitude'] == df['latitude'].shift(1)) & (df['longitude'] == df['longitude'].shift(1))

    # Replace repeated values with NaN
    df.loc[repeated_mask, ['latitude', 'longitude']] = np.nan

    return df

# Apply the function to replace repeated lat/lon with NaN
cleaned_df_cleaned = replace_repeated_lat_lon_with_nan(cleaned_df)

def interpolate_selected_fields(df, fields):
    """
    Interpolates missing fields for specified numeric columns in a dataframe.

    Args:
        df (pd.DataFrame): The input dataframe with missing fields.
        fields (list): List of column names to interpolate.

    Returns:
        pd.DataFrame: The dataframe with interpolated missing values for the specified fields.
    """
    # Ensure the fields provided exist in the dataframe and are numeric
    fields_to_interpolate = [field for field in fields if field in df.columns and pd.api.types.is_numeric_dtype(df[field])]
    
    if not fields_to_interpolate:
        print("No valid numeric fields provided for interpolation.")
        return df

    # Interpolate the specified numeric fields
    for field in fields_to_interpolate:
        df[field] = df[field].interpolate(method='linear', limit_direction='forward', axis=0)
        print(f"Interpolated missing values for column: {field}")

    return df

fields_to_interpolate = ['longitude','latitude','groundspeed', 'altitude']

cleaned_df_interpolated = interpolate_selected_fields(cleaned_df_cleaned, fields_to_interpolate)

def interpolate_large_distances(df):
    """
    Add interpolated rows between rows with distances larger than 40 km.
    Interpolated timestamps increase by 1 second from the previous row.

    Args:
        df (pd.DataFrame): DataFrame with 'flight_id', 'timestamp', 'latitude', 'longitude', and other attributes.

    Returns:
        pd.DataFrame: Modified DataFrame with no distances larger than 40 km.
    """
    # Sort the DataFrame by flight_id and timestamp
    df = df.sort_values(by=['timestamp', 'flight_id']).reset_index(drop=True)

    def add_interpolated_rows(group):
        """
        Interpolate rows for a single flight_id group.
        """
        new_rows = []  # Store new rows to add
        prev_row = None

        for i, row in group.iterrows():
            if prev_row is not None:
                # Compute geodesic distance
                coord1 = (prev_row['latitude'], prev_row['longitude'])
                coord2 = (row['latitude'], row['longitude'])
                distance_km = geodesic(coord1, coord2).kilometers

                # Calculate rates of change for each parameter
                time_diff = (row['timestamp'] - prev_row['timestamp']).total_seconds()
                if time_diff == 0:
                    continue  # Avoid division by zero

                rate_latitude = (row['latitude'] - prev_row['latitude']) / time_diff
                rate_longitude = (row['longitude'] - prev_row['longitude']) / time_diff
                rate_altitude = (row['altitude'] - prev_row['altitude']) / time_diff
                rate_vertical_rate = (row['vertical_rate'] - prev_row['vertical_rate']) / time_diff
                rate_groundspeed = (row['groundspeed'] - prev_row['groundspeed']) / time_diff

                # Continue adding interpolated points until distance is within 40 km
                while distance_km > 40:
                    # Compute new timestamp by adding 1 second to the previous timestamp
                    interpolated_timestamp = prev_row['timestamp'] + pd.Timedelta(seconds=1)

                    # Ensure the new timestamp is unique
                    if interpolated_timestamp in group['timestamp'].values:
                        break
                    
                    # Compute interpolated values using linear interpolation
                    interpolated_latitude = prev_row['latitude'] + rate_latitude
                    interpolated_longitude = prev_row['longitude'] + rate_longitude
                    interpolated_altitude = prev_row['altitude'] + rate_altitude
                    interpolated_vertical_rate = prev_row['vertical_rate'] + rate_vertical_rate
                    interpolated_groundspeed = prev_row['groundspeed'] + rate_groundspeed

                    # Create new interpolated row
                    midpoint = {
                        'icao24':           prev_row['icao24'],
                        'callsign':         prev_row['callsign'],
                        'flight_id':        prev_row['flight_id'],
                        'timestamp':        interpolated_timestamp,
                        'latitude':         interpolated_latitude,
                        'longitude':        interpolated_longitude,
                        'altitude':         interpolated_altitude,
                        'vertical_rate':    interpolated_vertical_rate,
                        'groundspeed':      interpolated_groundspeed,
                        # Add interpolation for other attributes as needed
                    }

                    # Add the new midpoint to new_rows
                    new_rows.append(midpoint)

                    # Update prev_row to the new midpoint and reassess the distance
                    prev_row = pd.Series(midpoint)
                    coord1 = (prev_row['latitude'], prev_row['longitude'])
                    distance_km = geodesic(coord1, coord2).kilometers

            # After processing, update prev_row to the current row
            prev_row = row

        # Add new rows to the group
        if new_rows:
            group = pd.concat([group, pd.DataFrame(new_rows)], ignore_index=True)

        # Sort the group by timestamp to ensure order
        return group.sort_values(by='timestamp').reset_index(drop=True)

    # Apply the interpolation logic to each flight_id group
    df = df.groupby('flight_id', group_keys=False).apply(add_interpolated_rows)

    # Sort the DataFrame by flight_id and timestamp
    df = df.sort_values(by=['timestamp', 'flight_id']).reset_index(drop=True)

    return df

# Example usage
# Assuming df is your DataFrame with 'flight_id', 'timestamp', 'latitude', 'longitude', etc.
df = interpolate_large_distances(cleaned_df_interpolated)

df.rename(columns={'timestamp': 'time'}, inplace=True)

# Identify duplicate timestamps within each flight_id group
duplicate_timestamps = df.duplicated(subset=['flight_id', 'time'], keep=False)

# Drop those rows
if duplicate_timestamps.any():
    print(f"Duplicate time dropped: {duplicate_timestamps.sum()}")
    df = df[~duplicate_timestamps].reset_index(drop=True)

# Convert altitude from feet to meters
#df['altitude'] = df['altitude'] * 0.3048 

# Assuming df is your DataFrame
df["heading"] = pd.to_numeric(df["heading"], errors='coerce')  # Convert non-numeric to NaN
df = df.dropna(subset=["heading"])  # Drop rows where heading is NaN

# Generate a data quality report
report = {
    #"missing_values":           missing_values.to_dict(),
    "invalid_latitude":         len(invalid_lat),
    "invalid_longitude":        len(invalid_lon),
    # "invalid_altitude_low":     len(invalid_altitude_low),
    # "invalid_altitude_high":    len(invalid_altitude_high),
    "unrealistic_groundspeed":  len(invalid_groundspeed),
    "duplicate_rows":           len(duplicate_rows),
}
print("Data Quality Report:\n", report)

# Display the list of inconsistent flight IDs
print("\nInconsistent Flight IDs:")
print(list(inconsistent_flight_ids))

# Create the new file name by appending "_checked" before the file extension
file_name, file_extension = os.path.splitext(output_file)  # Split the name and extension
new_file_name = f"{file_name}_checked.csv"

# Update the CSV with the cleaned data
df.to_csv(new_file_name, index=False)

# Optional: Print a message to confirm that the CSV has been updated
print(f"Cleaned data has been saved to {new_file_name}.")