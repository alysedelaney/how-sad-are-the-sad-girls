import requests 
import base64
import json
import os
import time

# =========================================================================

# This merges the spotify data and genius data for each artist into one compiled file. It pulls additional information for the artists' top tracks (NOTE: The full data including attributes for the Top Tracks no longer needs to be pulled in this script, as it will be retrieved later on in the project. All that is needed is the top track name and ID to be used in the next script). 

# =========================================================================

# Spotify API Set Up ------------------------------------------------------

client_id = "5bae1e05720d486a8bef2310f63cdb05"
client_secret = "8a701744762d47ae801d7bebf730e489"

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

#-----------------------------------------------------------------

compiled_artist_info = []

path_json = 'data/artist_info/'
#get all JSON file names as a list
json_files = [filename for filename in os.listdir(path_json) if filename.endswith('.json')]

num_files = len(json_files)
file_tracker = 1

for json_file_name in json_files:
    with open(os.path.join(path_json, json_file_name)) as json_file:
        json_load = json.load(json_file)

        print(f"\nFile {file_tracker}/{num_files} ---------------------------")

        genius_artist_id = json_load[0]['id']
        genius_artist_name = json_load[0]['name']
        genius_artist_instagram = json_load[0]['instagram_name']
        genius_artist_description = json_load[0]['description']['plain']
        genius_artist_image_url = json_load[0]['image_url']

        print(f"{genius_artist_name}")
        # print(json_file_name)

        search_url = f"https://api.spotify.com/v1/search/"
        search_params = {
            "q" : genius_artist_name,
            "type" : "artist",
            "limit" : 1
        }

        search_res = requests.get(url=search_url, headers=headers, params=search_params)
        search_json = search_res.json()  
        time.sleep(.5)

        spotify_genres = search_json['artists']['items'][0]['genres']
        spotify_artist_name = search_json['artists']['items'][0]['name']
        spotify_popularity = search_json['artists']['items'][0]['popularity']
        spotify_id = search_json['artists']['items'][0]['id']
        spotify_artist_link = search_json['artists']['items'][0]['external_urls']['spotify']

        print("\nFinding top tracks...")
        top_tracks_url = f"https://api.spotify.com/v1/artists/{spotify_id}/top-tracks"
        top_tracks_params = {
            "market" : "US"
        }
        top_tracks_res = requests.get(url=top_tracks_url, headers=headers, params=top_tracks_params)
        top_tracks_json = top_tracks_res.json()
        time.sleep(.5)

        track_counter = 1
        spotify_top_track_list = []
        for track in top_tracks_json['tracks']:
            track_name = track['name']
            track_id = track['id']
            #track_url = track['external_urls']['spotify']
            #track_irsc = track['external_ids']['isrc']
            #track_duration = track['duration_ms']
            #track_popularity = track['popularity']

            #This is not needed here anymore, as a later script pulls all audio features for each artist
            # audio_features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
            # audio_features_res = requests.get(url=audio_features_url, headers=headers)
            # audio_features_json = audio_features_res.json()

            print(f"{track_counter}: {track_name}")

            track_dict = {
                "number" : track_counter,
                "track_name" : track_name,
                "track_id" : track_id,
                #"track_irsc" : track_irsc,
                #"track_duration_ms" : track_duration,
                #"track_popularity" : track_popularity,
                #"track_url" : track_url,
                # "audio_features" : {
                #     "acousticness" : audio_features_json['acousticness'],
                #     "danceability" : audio_features_json['danceability'],
                #     "energy" : audio_features_json['energy'],
                #     "instrumentalness" : audio_features_json['instrumentalness'],
                #     "key" : audio_features_json['key'],
                #     "liveness" : audio_features_json['liveness'],
                #     "loudness" : audio_features_json['loudness'],
                #     "mode" : audio_features_json['mode'],
                #     "speechiness" : audio_features_json['speechiness'],
                #     "tempo" : audio_features_json['tempo'],
                #     "time_signature" : audio_features_json['time_signature']
                # }
            }

            spotify_top_track_list.append(track_dict)
            track_counter += 1
            time.sleep(.5)

        artist_data = {
            "spotify_artist_name" : spotify_artist_name,
            "genius_artist_name" : genius_artist_name,
            "instagram_handle" : genius_artist_instagram,
            "spotify_id" : spotify_id,
            "genius_id" : genius_artist_id,
            "genius_bio" : genius_artist_description,
            "spotify_genres" : spotify_genres,
            "spotify_artist_link" : spotify_artist_link,
            "genius_artist_image" : genius_artist_image_url,
            "spotify_popularity" : spotify_popularity,
            "spotify_top_tracks" : spotify_top_track_list
        }

        compiled_artist_info.append(artist_data)
        print(f"\n{spotify_artist_name} added to dictionary.")
        file_tracker += 1

with open("data/compiled_artist_info.json", "w") as write_file:
    json.dump(compiled_artist_info, write_file, indent=2)