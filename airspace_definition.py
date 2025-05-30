# =============================================================================
# Author: Wesley Gonçalves da Silva - IST1105271
# Purpose: This script generates a map visualization of predefined airspace 
#          regions over a section of the Americas using Cartopy and Matplotlib.
#
# Inputs:
#     - A dictionary named `regions`, where each key is a region identifier and 
#       each value is a list containing geographical boundaries in the format:
#       [minimum longitude, maximum longitude, maximum latitude, minimum latitude].
#
# Outputs:
#     - A map plot displaying each region as a labeled rectangle, including coastlines,
#       borders, land, and water features for context.
#     - Two image files saved to disk:
#         1. "airspace_definition.png" (high-resolution PNG format)
#         2. "airspace_definition.pdf" (PDF format for vector-quality print)
#
# Additional Comments:
#     - The projection used is PlateCarree (equidistant cylindrical).
#     - This script is useful for quick spatial validation or visual inspection of 
#       defined airspace regions for geographical or aeronautical purposes.
#     - Regions are drawn with `matplotlib.patches.Rectangle` and transformed to 
#       geographic coordinates.
#     - Gridlines and labels are added for better geospatial readability.
#     - Ensure that Cartopy and its dependencies (e.g., GEOS, PROJ, Shapely) are
#       properly installed before running the script.
# =============================================================================

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.patches as mpatches

# Define the airspace regions with the correct format [min lon, max lon, max lat, min lat]
regions = {
    "Area_1": [-100, -85, 30, 0],
    "Area_21": [-85, -55, 30, 10],
    "Area_22": [-55, -30, 15, -5],
    "Area_3": [-85, -55, -5, -20],
    "Area_4": [-85, -30, -20, -30],
    "Area_5": [-85, -55, 10, -5],
    "Area_6": [-55, -30, -5, -20],
}

# Set up the map
fig = plt.figure(figsize=(12, 10))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-100, -30, -30, 40], crs=ccrs.PlateCarree())

# Set water to blue and land to white
ax.add_feature(cfeature.OCEAN.with_scale("10m"), color="lightblue")
ax.add_feature(cfeature.LAND.with_scale("10m"), color="white", edgecolor="black")
ax.add_feature(cfeature.BORDERS.with_scale("10m"), linestyle=":", linewidth=1)
ax.add_feature(cfeature.COASTLINE.with_scale("10m"), linewidth=1)
ax.add_feature(cfeature.LAKES.with_scale("10m"), color="lightblue", alpha=1)

# Add gridlines with better precision
gl = ax.gridlines(draw_labels=True, color="gray", linestyle="--", linewidth=0.5)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {"size": 16}
gl.ylabel_style = {"size": 16}

# Plot each region as a red rectangle
for region, coords in regions.items():
    lon_min, lon_max, lat_max, lat_min = coords
    rect = mpatches.Rectangle(
        (lon_min, lat_min), lon_max - lon_min, lat_max - lat_min,
        fill=False, edgecolor="black", linewidth=1
    )
    ax.add_patch(rect)  # No transform here
    ax.patches[-1].set_transform(ccrs.PlateCarree())  # Apply transform separately

    # Add the label
    ax.text(
        (lon_min + lon_max) / 2, (lat_max + lat_min) / 2, region,
        transform=ccrs.PlateCarree(),
        ha="center", va="center", fontsize=14, color="black",
        bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white", alpha=1)
    )

# Save the figure with the highest resolution
plt.savefig("airspace_definition.png", dpi=600, bbox_inches="tight", format="png")
plt.savefig("airspace_definition.pdf", bbox_inches="tight", format="pdf")

# Show the plot
plt.show()