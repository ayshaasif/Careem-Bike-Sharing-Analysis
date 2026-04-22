import pandas as pd
import requests
from supabase import create_client
import os
import pandas as pd
from dotenv import load_dotenv
import plotly.express as px
import geopandas as gpd
from shapely.geometry import Point

load_dotenv()


# Initialize Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)


existing_stations = supabase.table("dim_stations").select("station_id, station_name, longitude, latitude").execute()

station_info_df = pd.DataFrame(existing_stations.data)
station_info_df.info()
latest_station_status_df = pd.read_csv('station_status_latest_updates.csv')
latest_station_status_df['station_id'] = latest_station_status_df['station_id'].astype(str) # Ensure station_id is string for merging
latest_station_status_df.info()
merged_df = pd.merge(station_info_df, latest_station_status_df, on='station_id', how='inner')

print(merged_df.head())
print(merged_df.columns)
print(merged_df['num_bikes_available'].isna().sum())



import json

geojson = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in merged_df.iterrows():
    # Logic for color: Green if bikes available, Red if empty
    color = "#00ff00" if row['num_bikes_available'] > 0 else "#ff0000"
    
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row['longitude'], row['latitude']]
        },
        "properties": {
            # GitHub specific labels
            "title": f"Station: {row['station_name']}",
            "description": f"Available Bikes: {row['num_bikes_available']}",
            
            # GitHub specific styling (Simplestyle)
            "marker-color": color,
            "marker-symbol": "bicycle",
            "marker-size": "medium",
            
            # You can still keep your raw data here too
            "station_id": row['station_id']
        }
    }
    geojson["features"].append(feature)

with open("map.geojson", "w") as f:
    json.dump(geojson, f)


# Create the map
fig = px.scatter_map(
    merged_df, 
    lat="latitude", 
    lon="longitude", 
    size="num_bikes_available",           # Circle size based on bikes
    color="num_bikes_available",          # Color changes with volume
    hover_name="station_name",      # Show station name on hover
    color_continuous_scale=px.colors.cyclical.IceFire, 
    size_max=15, 
    zoom=11,
    map_style="carto-positron"
)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()
fig.write_html("latest_bike_availability_map.html")
print("Map has been saved as latest_bike_availability_map.html")
