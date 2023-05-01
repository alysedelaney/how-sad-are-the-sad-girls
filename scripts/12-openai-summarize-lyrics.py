import openai
import os
import json

# ====================================================================

# This script uses the OpenAI Chat Completion tool to generate a summary of each of the artists' Top 10 Tracks based on their lyrics. 

# ====================================================================

openai.api_key = os.environ["OPENAI_API_KEY"]
system_setting = "You are learning about song lyrics."

lyrics_file = open('../data/compiled/compiled_genius_top_10_LYRICS.json')
lyrics_json = json.load(lyrics_file)

gpt_summaries = {}
errors = []

for artist in lyrics_json:
    
    artist_name = artist['artist_name']
    print(f"++++ {artist_name} ++++++++++++++++++++++++++++++")
    artist_id = artist['spotify_id']

    song_summaries = []
    
    for song in artist['songs']:
        
        song_title = song['title']
        print(f"---- {song_title} ----")
        song_id = song['spotify_id']
        
        substring = "New Music Friday"
        song_lyrics = song['lyrics']
        
        if substring not in song_title: 
            try:
                prompt = f"Tell me what this song is about, in 75 words or less. Lyrics:{song_lyrics}"
                res = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                            {"role":"system", "content": system_setting},
                            {"role":"user", "content": prompt}
                            ]
                        )
                
                gpt_summary = res.choices[0].message.content
                print(f"SUMMARY: {gpt_summary}")

                song_dict = {
                    "song_title" : song_title,
                    "track_id" : song_id,
                    "gpt_summary" : gpt_summary
                }

                song_summaries.append(song_dict)
            except:
                print(f"Error retrieving {song_title}.")
                errors.append(song_id)

    gpt_summaries[artist_id] = song_summaries

    with open('../data/compiled/gpt-summaries-2.json', 'w') as write_file:
        json.dump(gpt_summaries, write_file, indent=2)

print(f"ALL DONE!!!! These ids were unsuccessful: {errors}")

