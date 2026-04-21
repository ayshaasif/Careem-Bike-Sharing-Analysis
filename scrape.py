import requests
import json
import pandas as pd


response_station_info = requests.get('https://careem.publicbikesystem.net/customer/gbfs/v3.0/station_information.json') # get station information

data = response_station_info.json()
df = pd.DataFrame(data.get('data').get('stations'))
print(df.head())
print(df.columns)
df_copy = df[['name', 'lat', 'lon', 'capacity','station_id','address']].copy()
print(df_copy.head())
print(df_copy.columns)

response_station_status=requests.get('https://careem.publicbikesystem.net/customer/gbfs/v3.0/station_status.json') # get station status at the time of the request
data_station_status = response_station_status.json()
df_status = pd.DataFrame(data_station_status.get('data').get('stations'))
print(data_station_status.get('data').get('stations')[0])
# print(df_status.head())
# print(df_status.columns)

df_status_copy = df_status[["station_id",    "num_vehicles_available",    "num_vehicles_disabled",   "num_docks_available","num_docks_disabled","last_reported","is_installed","is_renting","is_returning"]]
# print(df_status_copy.head())
# print(df_status_copy.columns)



