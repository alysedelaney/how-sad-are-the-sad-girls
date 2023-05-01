import lyricsgenius
import json
import re

# =========================================================================

# This pulls the complete song data, including production data, lyrics, and annotations, from the Genius API for each of the artists' top tracks. 

# =========================================================================

#--API Setup------------------------------------------

user_token = "HA_bejJPPswn7Oi-ehqP-q9Ka2kkqJDppHjWSuXC4eyaVUYkaYQyR-xV-6FJXTnj"
genius = lyricsgenius.Genius(user_token,sleep_time=0.5,timeout=5, retries=3, verbose=True)

#-----------------------------------------------------

#open the compiled artist file
with open('data/compiled_artist_info.json') as read_file:
    json_file = json.load(read_file)
    
    #index to keep track of the number entry for each artist, in case the script fails
    json_index = 0
    for artist in json_file:
        #print the list of artist entries to keep track of index numberss
        artist_name = artist['genius_artist_name']
        print(f"{json_index}: {artist_name}")

        #if the script fails, enter the index number of where it needs to pick up at here
        if json_index >= 217:
        
            compiled_song_info = []          

            artist_spotify_id = artist['spotify_id']

            for track in artist['spotify_top_tracks']:

                track_name = track['track_name']
                spotify_id = track['track_id']

                song = genius.search_song(title=track_name, artist=artist_name)

                if song is not None:
                    search_results = song.to_dict()
                    track_id = search_results['id']
                    song_data = genius.song(song_id=track_id)

                    if search_results['annotation_count'] > 0:
                        annotations = genius.song_annotations(song_id=track_id)
                        print("Annotations found.\n")
                    else: 
                        annotations = False
                        print("No annotations.\n")
                
                    song_data = {
                        "spotify_id" : spotify_id,
                        "search_results" : search_results,
                        "full_song_data" : song_data,
                        "annotations" : annotations
                    }

                    compiled_song_info.append(song_data)
                    # print(compiled_song_info)

            artist_songs = {
                "artist_name" : artist_name,
                "spotify_id" : artist_spotify_id,
                "songs" : compiled_song_info
            } 
            # print(artist_songs)
            # print(json.dumps(artist_songs, indent=2))

            artist_file = re.sub('[^A-Za-z0-9]+', '', artist['spotify_artist_name']).lower()

            with open(f"data/song_data_by_artist/{artist_file}_songs.json", 'w') as write_file:
                json.dump(artist_songs, write_file, indent=2)

            # if len(instrumental_songs) > 0:
            #     with open(f"data/lyrics/{artist_file}_instrumental.json", 'w') as write_file_2:
            #         json.dump(instrumental_songs, write_file_2, indent=2)
            
            print(f"==================== {artist_name} lyrics file written. ====================\n")

        json_index += 1
