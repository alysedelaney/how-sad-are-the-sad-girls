import json
import os

# =========================================================================

# Combines the track data and track features into one compiled JSON file. 

# =========================================================================

artist_path = 'data/track_ids_by_artist/'
artist_id_files = [filename for filename in os.listdir(artist_path) if filename.endswith('.json')]

track_ids = []

for json_file_name in artist_id_files:
    with open(os.path.join(artist_path, json_file_name)) as json_file:
        json_load = json.load(json_file)
        for track_id in json_load['tracks']:
            track_ids.append(track_id)

#Need to make unique list because some artists might be on the same song
unique_track_ids = []
for track_id in track_ids:
    if track_id not in unique_track_ids:
        unique_track_ids.append(track_id)

features_file = open('data/all_track_features.json')
features_json = json.load(features_file)
metadata_file = open('data/all_track_data.json')
metadata_json = json.load(metadata_file)

compiled_track_data = []
failed_features_ids = []

print(len(unique_track_ids))

counter = 1
for key in unique_track_ids:
    try:        
        track_dict = {
            "track_id" : key,
            "title" : metadata_json[key]['title'],
            "artists" : metadata_json[key]['artists'],
            "popularity" : metadata_json[key]['popularity'],
            "explicit" : metadata_json[key]['explicit'],
            "spotify_url" : metadata_json[key]['spotify_url'],
            "preview_url" : metadata_json[key]['preview_url'],
            "duration_ms" : metadata_json[key]['duration_ms'],
            "danceability" : features_json[key]['danceability'],
            "energy": features_json[key]['energy'],
            "key": features_json[key]['key'],
            "instrumentalness": features_json[key]['instrumentalness'],
            "liveness": features_json[key]['liveness'],
            "loudness": features_json[key]['loudness'],
            "mode": features_json[key]['mode'],
            "speechiness": features_json[key]['speechiness'],
            "tempo": features_json[key]['tempo'],
            "time_signature": features_json[key]['time_signature'],
            "valence": features_json[key]['valence']
      }
        compiled_track_data.append(track_dict)
        # print(track_dict)
        print(counter)
    except:
        failed_features_ids.append(key)
    counter += 1

with open('data/compiled_track_data.json', 'w') as write_file:
    json.dump(compiled_track_data, write_file, indent=2)

features_file.close()
metadata_file.close()