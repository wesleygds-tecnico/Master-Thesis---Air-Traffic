import pandas as pd
import numpy as np
from tqdm import tqdm

# Load your datasets
# Load the CSV files as the datasets
df_main = pd.read_csv("C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\2024-01-01_2024-01-01_lon_min_-45_lon_max_45_lat_min_30_lat_max_70_flight_id_sample_one_processed.csv", low_memory=False)  # Replace with the actual file path
# df1     = pd.read_csv("C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\2024-01-01_2024-01-01_lon_min_-45_lon_max_45_lat_min_30_lat_max_70_flight_id_sample_two_processed.csv", low_memory=False)
# df2     = pd.read_csv("C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\2024-01-01_2024-01-01_lon_min_-45_lon_max_45_lat_min_30_lat_max_70_flight_id_sample_three_processed.csv", low_memory=False)
# df3     = pd.read_csv("C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\2024-01-01_2024-01-01_lon_min_-45_lon_max_45_lat_min_30_lat_max_70_flight_id_sample_four_processed.csv", low_memory=False)
# df4     = pd.read_csv("C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\2024-01-01_2024-01-01_lon_min_-45_lon_max_45_lat_min_30_lat_max_70_flight_id_sample_five_processed.csv", low_memory=False)
# df5     = pd.read_csv("C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\2024-01-01_2024-01-01_lon_min_-45_lon_max_45_lat_min_30_lat_max_70_flight_id_sample_six_processed.csv", low_memory=False)
# 
# # Get unique flight IDs for each dataset
# flight_ids = {
#     "Dataset1": set(df1["flight_id"].unique()),
#     "Dataset2": set(df2["flight_id"].unique()),
#     "Dataset3": set(df3["flight_id"].unique()),
#     "Dataset4": set(df4["flight_id"].unique()),
#     "Dataset5": set(df5["flight_id"].unique()),
# }
# 
# # Find the common flight IDs across all datasets
# common_flight_ids = set.intersection(*flight_ids.values())
# 
# # Print results
# print(f"Number of common flight IDs across all datasets: {len(common_flight_ids)}")
# 
# # Find flights not in common for each dataset
# not_in_common = {}
# for dataset_name, ids in flight_ids.items():
#     # Flights in other datasets but not in the current one
#     other_ids = set.union(*(flight_ids[name] for name in flight_ids if name != dataset_name))
#     not_in_common[dataset_name] = other_ids - ids
# 
# # Print results for flights not in common
# print("\nNumber of flights not in common per dataset:")
# for dataset_name, not_found in not_in_common.items():
#     print(f"  Not in {dataset_name}: {len(not_found)} flights")
# 
# # Optional: Print details of flight IDs not in common
# # Uncomment if needed
# for dataset_name, not_found in not_in_common.items():
#     print(f"\nFlights not in {dataset_name}: {not_found}")

# Loop through each unique flight_id
# Step 1: Extract rows with global min and max times for each flight_id

# Step 1: Group by 'flight_id' to calculate min and max times efficiently
grouped = df_main.groupby("flight_id")

# Find rows corresponding to the global min and max times for each flight_id
#min_times = grouped["time"].idxmin()
max_times = grouped["time"].idxmax()

# Extract the rows corresponding to the global min and max times
#min_rows = df_main.loc[min_times]
max_rows = df_main.loc[max_times]

# Combine the results and drop duplicates
min_max_df = pd.concat([max_rows]).drop_duplicates(subset=["flight_id", "time"]).reset_index(drop=True)

# Step 2: Process each dataset
dataset_paths = [
    "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\2024-01-01_2024-01-01_lon_min_-45_lon_max_45_lat_min_30_lat_max_70_flight_id_sample_two_processed.csv", 
    "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\2024-01-01_2024-01-01_lon_min_-45_lon_max_45_lat_min_30_lat_max_70_flight_id_sample_three_processed.csv",
    "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\2024-01-01_2024-01-01_lon_min_-45_lon_max_45_lat_min_30_lat_max_70_flight_id_sample_four_processed.csv", 
    "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\2024-01-01_2024-01-01_lon_min_-45_lon_max_45_lat_min_30_lat_max_70_flight_id_sample_five_processed.csv", 
    "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\2024-01-01_2024-01-01_lon_min_-45_lon_max_45_lat_min_30_lat_max_70_flight_id_sample_six_processed.csv",
]  # Paths to the datasets

for dataset_path in tqdm(dataset_paths, desc="Processing datasets", unit="dataset"):
    # Load the dataset
    df = pd.read_csv(dataset_path, low_memory=False)

    # Concatenate with min_max_df
    df = pd.concat([min_max_df, df]).drop_duplicates(subset=["flight_id", "time"]).sort_values(
        by=["flight_id", "time"]
    ).reset_index(drop=True)
    
    # Export the updated dataset as a CSV
    df.to_csv(dataset_path, index=False)
    
    # Delete the DataFrame to free up memory
    del df

print("Processing complete. Updated datasets exported as CSV files.")