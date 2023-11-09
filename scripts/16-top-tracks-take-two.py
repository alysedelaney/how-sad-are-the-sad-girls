import requests 
import base64
import json
import csv

# ====================================================================

# Retrieves each of the artists' top 10 tracks at the given moment and compiles the data into a CSV file for analysis in Tableau. 

# ====================================================================

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

#-----------------------------------------------------------------

top_tracks_csv = open("../data/csv_files_for_analysis/top_tracks.csv", 'w')
top_writer = csv.writer(top_tracks_csv)

with open('../data/compiled/compiled_ARTIST.json') as read_file:
    artists_json = json.load(read_file)
    
    for artist in artists_json:
        artist_name = artist['spotify_artist_name']
        artist_id = artist['spotify_id']
        
        print('--------------------------------')
        print(artist_name)
        print(artist_id)

        top_tracks_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
        top_tracks_params = {
            "market" : "US"
        }
        top_tracks_res = requests.get(url=top_tracks_url, headers=headers, params=top_tracks_params)
        top_tracks_json = top_tracks_res.json()

        track_counter = 1
        spotify_top_track_list = []
        for track in top_tracks_json['tracks']:
            track_name = track['name']
            track_id = track['id']
            track_embed = f"https://open.spotify.com/embed/track/{track_id}?utm_source=generator&theme=0"

            top_dict = {
                "artist_name" : artist_name,
                "artist_id" : artist_id,
                "track_number" : track_counter,
                "track_name" : track_name,
                "track_id" : track_id,
                "track_embed" : track_embed
            }
            print(track_name)

            top_writer.writerow(top_dict.values())
            
            track_counter += 1

top_tracks_csv.close()