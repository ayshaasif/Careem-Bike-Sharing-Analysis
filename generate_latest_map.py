import pandas as pd
import requests
from supabase import create_client
import os
import pandas as pd
from dotenv import load_dotenv


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
import plotly.express as px

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
