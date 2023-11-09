import json
import os
import requests 
import base64
import json

# =========================================================================

# This gets the track features for each of the artists' songs. Track features are requested in batches of 100. 

# =========================================================================

# Spotify API Set Up ------------------------------------------------------

client_id = "ENTER client_id HERE"
client_secret = "ENTER client_secret HERE"

url = 'https://accounts.spotify.com/api/token'

headers = {}
data = {}

message = f"{client_id}:{client_secret}" 
message_bytes = message.encode('ascii')
base64bytes = base64.b64encode(message_bytes)
base64message = base64bytes.decode('ascii')

headers['Authorization'] = f"Basic {base64message}"
data['grant_type'] = "client_credentials"

r = requests.post(url, headers=headers, data=data)

token = r.json()['access_token']

headers = {
    "Authorization": "Bearer " + token
}

base_url = "https://api.spotify.com/v1/"

# ----------------------------------------------------------------------------

path_json = 'data/track_ids_by_artist/'
#get all JSON file names as a list
json_files = [filename for filename in os.listdir(path_json) if filename.endswith('.json')]

track_ids = []
search_lists = []

# ------------------------------------------------------------------------------------------

#Get track_ids from each artist file

for json_file_name in json_files:
    with open(os.path.join(path_json, json_file_name)) as json_file:
        json_load = json.load(json_file)
        for track_id in json_load['tracks']:
            track_ids.append(track_id)

# ------------------------------------------------------------------------------------------

#Split track ids into groups of 50, and convert to comma separated string for API Call

def split(my_list, chunk_size):

    for i in range(0, len(my_list), chunk_size):
        yield my_list[i:i + chunk_size]

chunk_size = 100
track_ids_split = list(split(track_ids, chunk_size))

for section in track_ids_split:
    section_joined = ",".join(section)
    search_lists.append(section_joined)

# ------------------------------------------------------------------------------------------

print(f"Getting data for {len(track_ids)} tracks in {len(track_ids_split)} batches.")
print(len(track_ids))

# # API call to retrieve track data and track features 
features_url = f"{base_url}audio-features"

track_features = {}

batch_counter = 1

for search in search_lists:
    print(f"{batch_counter}/{len(search_lists)}")
    print(f"Length of Search Ids: {len(search)}")
    print("----------------------------------")

    params = {
        "ids" : search
    }
        
    features_res = requests.get(url=features_url, headers=headers, params=params)
    features_json = features_res.json()

    for track in features_json['audio_features']:
        try:
            track_id = track['id']
            print(track_id)
            track_features[track_id] ={
                "danceability" : track['danceability'],
                "energy" : track['energy'],
                "key" : track['key'],
                "instrumentalness" : track['instrumentalness'],
                "liveness" : track['liveness'],
                "loudness" : track['loudness'],
                "mode" : track['mode'],
                "speechiness" : track['speechiness'],
                "tempo" : track['tempo'],
                "time_signature" : track['time_signature'],
                "valence" : track['valence'],
            }
        except: 
            print(track)
            break
    
    json.dump(track_features, open('all_track_features.json', 'w'), indent=2)
    
    batch_counter += 1
