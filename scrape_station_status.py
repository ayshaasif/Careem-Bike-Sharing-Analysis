import requests
from supabase import create_client
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Initialize Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def ingest_deltas():
    # 1. Fetch current status from Careem GBFS
    res = requests.get("https://careem.publicbikesystem.net/customer/gbfs/v2/en/station_status.json")
    current_stations = res.json()['data']['stations']

    # 2. Get the latest record for every station from Supabase to compare
    # Note: In a real DE pipeline, you might cache this in Redis or a local file
    latest_states = supabase.table("station_snapshots").select("station_id, num_bikes_available").execute()
    last_known = {item['station_id']: item['num_bikes_available'] for item in latest_states.data}

    updates = []
    for station in current_stations:
        s_id = station['station_id']
        current_count = station['num_bikes_available']
        
        # 3. Delta Logic: Only append if the count has changed or it's a new station
        if s_id not in last_known or last_known[s_id] != current_count:
            updates.append({
                "station_id": s_id,
                "num_bikes_available": current_count,
                "num_docks_available": station['num_docks_available'],
                "is_renting": station['is_renting'],
                "reported_at": station['last_reported']
            })

    # 4. Batch insert into Supabase
    if updates:
        pd.DataFrame(updates).to_csv('station_status_latest_updates.csv', index=False) # Optional: Save updates to CSV for backup
        supabase.table("station_snapshots").insert(updates).execute()
        print(f"Stored {len(updates)} changes.")
    else:
        print("No changes detected.")

if __name__ == "__main__":
    ingest_deltas()

