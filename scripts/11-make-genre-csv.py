import json
import csv

# ====================================================================

# Compiles a csv with artists' genres by row for visualization in Tableau. 

# ====================================================================

genres_csv = open('../data/csv_files_for_analysis/genres_by_artist.csv', 'w')
genres_writer = csv.writer(genres_csv)

headers = {
    "artist_name": "artist_name",
    "artist_id": "artist_id",
    "genre": "genre",
}

genres_writer.writerow(headers.values())

#artist list to check against featured artists when compiling CSV
artists = []

with open('../data/compiled/compiled_ARTIST.json') as artist_file:
    artist_json = json.load(artist_file)

    for artist in artist_json:
        artist_name = artist['spotify_artist_name']
        artist_id = artist['spotify_id']
        for genre in artist['spotify_genres']:
            write_dict = {
                "artist_name" : artist_name,
                "artist_id" : artist_id,
                "genre" : genre
            }
            genres_writer.writerow(write_dict.values())
            
genres_csv.close()