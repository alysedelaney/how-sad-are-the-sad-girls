import json
import os
import requests 
import base64
import json

# =========================================================================

# This gets the track data from Spotify for every one of the artists' songs. Track data is requested in batches of 50.  

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

chunk_size = 50
track_ids_split = list(split(track_ids, chunk_size))

for section in track_ids_split:
    section_joined = ",".join(section)
    search_lists.append(section_joined)

# ------------------------------------------------------------------------------------------

print(f"Getting data for {len(track_ids)} tracks in {len(track_ids_split)} batches.")
print(len(track_ids))

# # API call to retrieve track data and track features 

tracks_url = f"{base_url}tracks"
# features_url = f"{base_url}audio-features"

track_data = {}
# track_features = {}

batch_counter = 1

for search in search_lists:
    print(f"{batch_counter}/{len(search_lists)}")
    print(f"Length of Search Ids: {len(search)}")
    print("----------------------------------")

    params = {
        "ids" : search
    }

    # # Get track metadata via Get Several Tracks endpoint
    tracks_res = requests.get(url=tracks_url, headers=headers, params=params)
    tracks_json = tracks_res.json()
    
    for track in tracks_json['tracks']:

        track_id = track['id']
        print(track_id)
        artists =[]

        for artist in track['artists']:
            artist_name = artist['name']
            artist_id = artist['id']
            artist_dict = {
                "name" : artist_name,
                "id" : artist_id
            }
            artists.append(artist_dict)

        track_data[track_id] = {
            "title" : track['name'],
            "artists" : artists,
            "popularity" : track['popularity'],
            "explicit" : track['explicit'],
            "spotify_url" : track['external_urls']['spotify'],
            "preview_url" : track['preview_url'],
            'duration_ms' : track['duration_ms']
        }

    json.dump(track_data, open("data/all_tracks_data.json", 'w'), indent=2)
    print(f"{batch_counter} added to file ---------------------------\n")
    
    batch_counter += 1
    
