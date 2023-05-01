import json
import csv

# =========================================================================

# Makes a CSV file from the compiled track data for visualization in Tableau. 

# =========================================================================

tracks_csv = open('../data/csv_files_for_analysis/track_data.csv', 'w')
tracks_writer = csv.writer(tracks_csv)

headers = {
    "track_id" : "track_id",
    "track_title" : "track_title",
    "artist_name" : "artist_name",
    "artist_id" : "artist_id",
    "track_popularity" : "track_popularity",
    "track_explicit" : "track_explicit",
    "spotify_url" : "spotify_url",
    "preview_url" : "preview_url",
    "duration_ms" : "duration_ms",
    "danceability": 'danceability',
    "energy": 'energy',
    "key": 'key',
    "instrumentalness": 'instrumentalness',
    "liveness": 'liveness',
    "loudness": 'loudness',
    "mode": 'mode',
    "speechiness": 'speechiness',
    "tempo": 'tempo',
    "time_signature": 'time_signature',
    "valence": 'valence'
}

tracks_writer.writerow(headers.values())

#artist list to check against featured artists when compiling CSV
artists = []

with open('../data/compiled/compiled_ARTIST.json') as artist_file:
    artist_json = json.load(artist_file)
    for artist in artist_json:
        artists.append(artist['spotify_id'])

with open('../data/compiled/compiled_ALL_TRACKS.json') as read_file: 
    read_json = json.load(read_file)

    for track in read_json:
        track_id = track['track_id']
        track_title = track['title']
        track_popularity = track['popularity']
        track_explicit = track['explicit']
        spotify_url = track['spotify_url']
        preview_url = track['preview_url']
        duration_ms = track['duration_ms']
        danceability= track['danceability']
        energy= track['energy']
        key= track['key']
        instrumentalness= track['instrumentalness']
        liveness= track['liveness']
        loudness= track['loudness']
        mode= track['mode']
        speechiness= track['speechiness']
        tempo= track['tempo']
        time_signature= track['time_signature']
        valence = track['valence']


        for artist in track['artists']:
            if artist['id'] in artists:
                write_dict = {
                    "track_id" : track_id,
                    "track_title" : track_title,
                    "artist_name" : artist['name'],
                    "artist_id" : artist['id'],
                    "track_popularity" : track_popularity,
                    "track_explicit" : track_explicit,
                    "spotify_url" : spotify_url,
                    "preview_url" : preview_url,
                    "duration_ms" : duration_ms,
                    "danceability": danceability,
                    "energy": energy,
                    "key": key,
                    "instrumentalness": instrumentalness,
                    "liveness": liveness,
                    "loudness": loudness,
                    "mode": mode,
                    "speechiness": speechiness,
                    "tempo": tempo,
                    "time_signature": time_signature,
                    "valence": valence
                }
                
                tracks_writer.writerow(write_dict.values())
            
tracks_csv.close()