import requests
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Initialize Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)


def ingest_deltas():
    # 1. Fetch current status from Careem GBFS
    res = requests.get("https://careem.publicbikesystem.net/customer/gbfs/v3.0/station_information.json")
    data = res.json()
    print(data.get('data').get('stations')[0])
    current_stations = data['data']['stations']
    print(current_stations[0])

    # 2. Get the latest record for every station from Supabase to compare
    # Note: In a real DE pipeline, you might cache this in Redis or a local file
    existing_stations = supabase.table("dim_stations").select("station_id, station_name, longitude, latitude").execute()
    existing_station_id  = {item['station_id']: item for item in existing_stations.data}

    updates = []
    for station in current_stations:
        s_id = station['station_id']
        station_name = station['name'][0].get('text')
        longitude = station['lon']
        latitude = station['lat']
        address = station['address']
        capacity = station['capacity']
        
        if s_id not in existing_station_id:
            updates.append({
                "station_id": s_id,
                "station_name": station_name,
                "longitude": longitude,
                "latitude": latitude,
                "address": address,
                "capacity": capacity
            })

    # 4. Batch insert into Supabase
    if updates:
        supabase.table("dim_stations").insert(updates).execute()
        print(f"Stored {len(updates)} changes.")
    else:
        print("No changes detected.")

if __name__ == "__main__":
    ingest_deltas()
