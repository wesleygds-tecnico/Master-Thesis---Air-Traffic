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
input_file = "C:\\Users\\wesle\\OneDrive\\Documentos\\Master\\traffic\\code1\\traffic\\2024-01-01_2024-01-07_raw_data_AIC129_checked.csv"
df = pd.read_csv(input_file)

# Ensure the timestamp column is in datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Extract the day from the timestamp
df['day'] = df['timestamp'].dt.date

# Set up the map with Cartopy
plt.figure(figsize=(15, 10))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-15, 50, 30, 65], crs=ccrs.PlateCarree())  # Adjust bounds as necessary

# Add map features for better fidelity
ax.add_feature(cfeature.LAND, color="lightgray")
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linestyle=":")

# Group the data by day and plot each day's flight paths
grouped = df.groupby('day')
for day, group in grouped:
    plt.plot(group['longitude'], group['latitude'], label=f"Day {day}", 
             transform=ccrs.PlateCarree(), alpha=1, linewidth=1)

# Add gridlines using Cartopy's GeoAxes
gl = ax.gridlines(draw_labels=True, linewidth=0.2, color="gray", alpha=0.5)
gl.top_labels = False  # Disable labels on the top
gl.right_labels = False  # Disable labels on the right

# Add labels and legend
plt.xlabel(r"Longitude [\degree]")
plt.ylabel(r"Latitude [\degree]")
plt.title(r"Flight Paths Grouped by Day")
plt.legend(loc='upper left', fontsize=8)

# Save and show the map
plt.savefig("Flight_paths_grouped_by_day.pdf", format="pdf")  # Save as PDF
plt.savefig("Flight_paths_grouped_by_day.png", format="png", dpi=300)  # Save as PNG with high resolution
plt.show()

# Plot altitude vs. time for each day
plt.figure(figsize=(10, 6))
for day, group in grouped:
    group['seconds_since_midnight'] = group['timestamp'].dt.hour * 3600 + group['timestamp'].dt.minute * 60 + group['timestamp'].dt.second
    plt.plot(group['seconds_since_midnight'], group['altitude'], label=f"Day {day}",marker='.')

# find_peaks scipy

plt.xlabel(r"Time (Seconds since midnight)")
plt.ylabel(r"Altitude [ft]")
plt.title(r"Altitude Over Time Grouped by Day")
plt.legend(fontsize=8)
plt.grid()

# Format x-axis to display time in HH:MM
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# Auto-adjust the x-axis labels for better readability
plt.gcf().autofmt_xdate()

plt.savefig("Altitude_time_grouped_by_day.pdf", format="pdf")  # Save as PDF
plt.savefig("Altitude_time_grouped_by_day.png", format="png", dpi=300)  # Save as PNG with high resolution
plt.show()

# Additional plots (e.g., vertical rate vs. time, groundspeed vs. time) can be modified similarly by grouping by 'day'.

# Plot altitude vs. time for each day
plt.figure(figsize=(10, 6))
for day, group in grouped:
    group['seconds_since_midnight'] = group['timestamp'].dt.hour * 3600 + group['timestamp'].dt.minute * 60 + group['timestamp'].dt.second
    plt.plot(group['seconds_since_midnight'], group['vertical_rate'], label=f"Day {day}")

plt.xlabel(r"Time (Seconds since midnight)")
plt.ylabel(r"Vertical Rate [m/s]")
plt.title(r"Vertical Rate Over Time")
plt.legend(fontsize=8)
plt.grid()

# Format x-axis to display time in HH:MM
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# Auto-adjust the x-axis labels for better readability
plt.gcf().autofmt_xdate()

plt.savefig("Vertical_rate_time_grouped_by_day.pdf", format="pdf")  # Save as PDF
plt.savefig("Vertical_rate_time_grouped_by_day.png", format="png", dpi=300)  # Save as PNG with high resolution
plt.show()

# Plot altitude vs. time for each day
plt.figure(figsize=(10, 6))
for day, group in grouped:
    group['seconds_since_midnight'] = group['timestamp'].dt.hour * 3600 + group['timestamp'].dt.minute * 60 + group['timestamp'].dt.second
    plt.plot(group['seconds_since_midnight'], group['vertical_rate'], label=f"Day {day}")

plt.xlabel(r"Time (Seconds since midnight)")
plt.ylabel(r"Vertical Rate [m/s]")
plt.title(r"Vertical Rate Over Time")
plt.legend(fontsize=8)
plt.grid()

# Format x-axis to display time in HH:MM
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# Auto-adjust the x-axis labels for better readability
plt.gcf().autofmt_xdate()

plt.savefig("Vertical_rate_time_grouped_by_day.pdf", format="pdf")  # Save as PDF
plt.savefig("Vertical_rate_time_grouped_by_day.png", format="png", dpi=300)  # Save as PNG with high resolution
plt.show()

# Plot altitude vs. time for each day
plt.figure(figsize=(10, 6))
for day, group in grouped:
    group['seconds_since_midnight'] = group['timestamp'].dt.hour * 3600 + group['timestamp'].dt.minute * 60 + group['timestamp'].dt.second
    plt.plot(group['altitude'], group['groundspeed'], label=f"Day {day}")

plt.xlabel(r"Altitude")
plt.ylabel(r"Groundspeed [m/s]")
plt.title(r"Groundspeed vs Altitude")
plt.legend(fontsize=8)
plt.grid()

# Auto-adjust the x-axis labels for better readability
plt.gcf().autofmt_xdate()

plt.savefig("Groundspeed_altitude_grouped_by_day.pdf", format="pdf")  # Save as PDF
plt.savefig("Groundspeed_altitude_grouped_by_day.png", format="png", dpi=300)  # Save as PNG with high resolution
plt.show()