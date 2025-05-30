from datetime import datetime
import requests
import time
import json
import pandas as pd
import csv


def format_timestamp(date_str, date_format="%Y-%m-%d %H:%M:%S"):
    """
    Converts a date string into the required timestamp format.

    :param date_str: The date as a string (e.g., "2023-12-12 15:45:45")
    :param date_format: The format of the input date string (default: "%Y-%m-%d %H:%M:%S")
    :return: Dictionary with the timestamp in the required format
    """
    # Convert the string into a datetime object
    dt = datetime.strptime(date_str, date_format)

    # Convert to Unix timestamp
    timestamp = int(time.mktime(dt.timetuple()))

    # Return formatted dictionary
    return timestamp

# API URL (replace with actual API URL)
url = "https://fr24api.flightradar24.com/api/historic/flight-positions/full"

# Initial timestamp (replace with your desired start time)
initial_timestamp_str = '2025-01-31 05:20:00'
initial_timestamp = format_timestamp(initial_timestamp_str, date_format="%Y-%m-%d %H:%M:%S")  # Example starting timestamp
time_step = 300  # Number of seconds to increment per request
iterations = 10  # Number of API calls (adjust as needed)

# CSV Output File
csv_filename = "flightradar24_LIMC_31-01-2025.csv"

# Define CSV Header
csv_headers = ["timestamp", "fr24_id", "flight", "callsign", "lat", "lon",
                "track", "alt", "gspeed", "vspeed", "squawk", "source",
                  "hex", "type", "reg", "painted_as", "operating_as",
                    "orig_iat", "orig_icao", "dest_iata", "dest_icao", "eta"]

# Create CSV File and Write Header
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(csv_headers)

# API Headers/# API Token (replace with your actual token)
headers = {
    #"Accept": "application/json",
    "Authorization": "Bearer 9e1ca95d-dafd-4333-b5e3-be1c1cf8a6b5|toW9GbMihPmr18veDyuyiVKmAQxvSUC4tHAqnEnt0ca3f7a0",
    "Accept-Version": "v1",
}

# Loop to send multiple requests with different timestamps
for i in range(iterations):
    current_timestamp = initial_timestamp + (i * time_step)  # Increment timestamp
    params = {
        # "bounds": "75,18,51,-25",
        "timestamp": str(current_timestamp),  # Convert to string for API
        "flights": "EN8281"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        print(response.status_code, response.text)
        response.raise_for_status()
        data = response.json()

        # Convert response to JSON string for saving in CSV
        data_str = json.dumps(data)


        if response.status_code == 200:
            flight_data = response.json()

            # Extract waypoints (latitude, longitude, altitude, speed, timestamp)
            if "trail" in flight_data:
                waypoints = [
                {
                    "timestamp": point.get("ts", None),
                    "latitude": point.get("lat", None),
                    "longitude": point.get("lng", None),
                    "altitude_ft": point.get("alt", None),
                    "speed_knots": point.get("spd", None),
                    "vertical_speed": point.get("vs", None),
                    "track": point.get("trk", None),
                    "squawk": flight_data.get("squawk", None),
                    "source": flight_data.get("src", None),
                    "fr24_id": flight_data.get("id", None),
                    "flight": flight_data.get("flight", None),
                    "callsign": flight_data.get("callsign", None),
                    "hex": flight_data.get("hex", None),
                    "type": flight_data.get("type", None),
                    "registration": flight_data.get("reg", None),
                    "painted_as": flight_data.get("painted", None),
                    "operating_as": flight_data.get("operator", None),
                    "orig_iata": flight_data.get("airport", {}).get("origin", {}).get("iata", None),
                    "orig_icao": flight_data.get("airport", {}).get("origin", {}).get("icao", None),
                    "dest_iata": flight_data.get("airport", {}).get("destination", {}).get("iata", None),
                    "dest_icao": flight_data.get("airport", {}).get("destination", {}).get("icao", None),
                    "eta": flight_data.get("eta", None)
                }
                    for point in flight_data["trail"]
                ]

                # Convert to DataFrame
                df = pd.DataFrame(waypoints)

                # Display DataFrame
                print(df)

                print(f"Data for timestamp {current_timestamp} saved successfully.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred at timestamp {current_timestamp}: {http_err}")
    except Exception as err:
        print(f"An error occurred at timestamp {current_timestamp}: {err}")

    # Optional: Wait between requests to avoid hitting API rate limits
    time.sleep(1)

print(f"All data saved in {csv_filename}.")    