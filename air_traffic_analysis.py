# ===============================================================================================================
# Author: Wesley Gonçalves da Silva - IST1105271
# Purpose:
#     This script is designed to process and visualize flight data using geographic and 
#     time-series plots. It focuses on a specific flight (callsign "AMX690") and generates 
#     multiple plots to analyze flight paths, altitude profiles, vertical rates, and speed 
#     variations over time.
#
# Inputs:
#     - A CSV file containing air traffic data with columns such as timestamp, longitude, 
#       latitude, altitude, vertical_rate, groundspeed, callsign, and flight_id.
#     - File path specified in `input_file`.
#
# Outputs:
#     - Geographic map showing the flight path.
#     - Time-series plots of:
#         * Altitude over time
#         * Vertical rate over time
#         * Groundspeed over time
#     - Scatter plots of:
#         * Altitude vs. callsign
#         * Groundspeed vs. altitude
#     - Each plot is saved as both PDF and PNG in the working directory.
#
# Additional Comments:
#     - Uses Cartopy for geographical plotting and Matplotlib for data visualization.
#     - Focuses on data associated with the callsign "AMX690".
#     - Time is processed into seconds since midnight to facilitate temporal plots.
#     - LaTeX rendering is disabled, but serif fonts are used for publication-ready visuals.
#     - Gridlines and map features are added for better clarity.
#     - This code assumes the structure of the input CSV is compatible with the data access 
#       pattern used (i.e., expected column names are present).
#     - Ensure all required libraries (pandas, matplotlib, cartopy) are installed.
# ===============================================================================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Enable LaTeX font rendering
plt.rcParams.update({
    "text.usetex": False,
    "font.family": "serif",
    "font.size": 12
})

# Load the data
input_file = "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\data\\2025\\2025_01_01-2025_01_07-LA\\air_traffic_output_data_LA_2025-01-01_flight_id.csv"

df = pd.read_csv(input_file)

# Ensure the timestamp column is in datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Extract time from the timestamp
df['time'] = df['timestamp'].dt.time

# Extract time from the timestamp and convert to seconds since midnight
df['seconds_since_midnight'] = df['timestamp'].dt.hour * 3600 + df['timestamp'].dt.minute * 60 + df['timestamp'].dt.second

df=df[df["callsign"]=="AMX690"]

# Group by flight_id
grouped = df.groupby('flight_id')

# Set up the map with Cartopy
plt.figure(figsize=(15, 10))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())  # Adjust bounds as necessary

# Add map features for better fidelity
ax.add_feature(cfeature.LAND, color="lightgray")
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linestyle=":")

# Group the data by flight_id and plot each flight path
grouped = df.groupby('flight_id')
for flight_id, group in grouped:
    plt.plot(group['longitude'], group['latitude'], label=f"Flight {flight_id}", 
             transform=ccrs.PlateCarree(), alpha=0.7, linewidth=1)

# Add gridlines using Cartopy's GeoAxes
gl = ax.gridlines(draw_labels=True, linewidth=0.2, color="gray", alpha=0.5)
gl.top_labels = False  # Disable labels on the top
gl.right_labels = False  # Disable labels on the right

# Add labels and legend
plt.xlabel(r"Longitude [\degree]")
plt.ylabel(r"Latitude [\degree]")
plt.title(r"Flight Paths on Geographic Map")
#plt.legend(loc='upper left', fontsize=8)
plt.savefig("Flight_paths_on_geographic_map.pdf", format="pdf")  # Save as PDF
plt.savefig("Flight_paths_on_geographic_map.png", format="png", dpi=300)  # Save as PNG with high resolution

# Plot altitude vs. time for each flight
plt.figure(figsize=(10, 6))
for flight_id, group in grouped:
    # Ensure `seconds_since_midnight` is a numeric column
    # Convert `seconds_since_midnight` to a pandas datetime starting from midnight
    group['seconds_since_midnight'] = pd.to_numeric(group['seconds_since_midnight'], errors='coerce') # it works
    group['time'] = pd.to_datetime(group['seconds_since_midnight'], unit='s', origin='1970-01-01')
    plt.plot(group['time'], group['altitude'], label=f"Flight {flight_id}")

plt.xlabel(r"Time (Seconds since midnight)")
plt.ylabel(r"Altitude [ft]")
plt.title(r"Altitude Over Time")
plt.legend(fontsize=8)
plt.grid()

# Format x-axis to display time in HH:MM
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# Auto-adjust the x-axis labels for better readability
plt.gcf().autofmt_xdate()

plt.savefig("altitude_time.pdf", format="pdf")  # Save as PDF
plt.savefig("altitude_time.png", format="png", dpi=300)  # Save as PNG with high resolution
plt.show()

# Plot vertical rate vs. time for each flight
plt.figure(figsize=(10, 6))
for flight_id, group in grouped:
    plt.plot(group['seconds_since_midnight'], group['vertical_rate'], label=f"Flight {flight_id}")
plt.xlabel(r"Time (Seconds since midnight)")
plt.ylabel(r"Vertical Rate [m/s]")
plt.title(r"Vertical Rate Over Time")
plt.legend(fontsize=8)
plt.grid()
plt.savefig("vertical_rate_time.pdf", format="pdf")  # Save as PDF
plt.savefig("vertical_rate_time.png", format="png", dpi=300)  # Save as PNG with high resolution
plt.show()

# Plot groundspeed vs. time for each flight
plt.figure(figsize=(10, 6))
for flight_id, group in grouped:
    plt.plot(group['seconds_since_midnight'], group['groundspeed'], label=f"Flight {flight_id}")
plt.xlabel(r"Time (Seconds since midnight)")
plt.ylabel(r"Groundspeed [m/s]")
plt.title(r"Groundspeed Over Time")
plt.legend(fontsize=8)
plt.grid()
plt.savefig("groundspeed_time.pdf", format="pdf")  # Save as PDF
plt.savefig("groundspeed_time.png", format="png", dpi=300)  # Save as PNG with high resolution
plt.show()

# Plot altitude vs. callsign for each flight
plt.figure(figsize=(10, 6))
for flight_id, group in grouped:
    plt.scatter(group['callsign'], group['altitude'], label=f"Flight {flight_id}", alpha=0.6)
plt.xlabel(r"Callsign")
plt.ylabel(r"Altitude [ft]")
plt.title(r"Altitude vs Callsign")
plt.legend()
plt.grid()
plt.savefig("altitude_callsign.pdf", format="pdf")  # Save as PDF
plt.savefig("altitude_callsign.png", format="png", dpi=300)  # Save as PNG with high resolution
plt.show()

# Plot groundspeed vs altitude for each flight
plt.figure(figsize=(10, 6))
for flight_id, group in grouped:
    plt.scatter(group['altitude'], group['groundspeed'], label=f"Flight {flight_id}", alpha=0.6)
plt.xlabel(r"Altitude")
plt.ylabel(r"Groundspeed [m/s]")
plt.title(r"Groundspeed vs Altitude")
plt.legend()
plt.grid()
plt.savefig("groundspeed_altitude.pdf", format="pdf")  # Save as PDF
plt.savefig("groundspeed_altitude.png", format="png", dpi=300)  # Save as PNG with high resolution
plt.show()
