import json
import csv
import os
import openai

# ====================================================================

# This script compiles the artist bios into a CSV file for analysis in Tableau. If an artist bio is not available, it creates a line "This artist doesn't have a bio yet! Stay tuned...". If the artist bio is over 500 characters long, the biography is summarized using the OpenAI Chat Completion tool. 

# ====================================================================

openai.api_key = os.environ["OPENAI_API_KEY"]
system_setting = "Summarize musician biographies."

artist_bios_csv = open("../data/csv_files_for_analysis/artist-bio.csv", 'w')
bio_writer = csv.writer(artist_bios_csv)

headers = {
    "name" : "name",
    "id" : "id",
    "bio" : "bio",
}

bio_writer.writerow(headers.values())

with open("../data/compiled/compiled_ARTIST.json") as read_file:
    read_json = json.load(read_file)

    for artist in read_json: 
        artist_name = artist['spotify_artist_name']
        artist_id = artist['spotify_id']
        artist_bio = artist['genius_bio']
        image = artist['genius_artist_image']
        popularity = artist['spotify_popularity']
        embed_artist = f"https://open.spotify.com/embed/artist/{artist_id}?utm_source=generator&theme=0"
        if artist_bio == "?" :
            artist_bio = "This artist doesn't have a bio yet! Stay tuned..."
        elif len(artist_bio) > 500:
            prompt = f"Please summarize this biography, in 50 words or less: {artist_bio}"

            res = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                        {"role":"system", "content": system_setting},
                        {"role":"user", "content": prompt}
                        ]
                    )
            
            artist_bio = f"{res.choices[0].message.content} (Summarized by ChatGPT)"
        
        print(f"{artist_name} BIO: {artist_bio}\n")

        bio_dict = {
            "artist_name" : artist_name,
            "artist_id" : artist_id,
            "artist_bio" : artist_bio,
        }

        bio_writer.writerow(bio_dict.values())

artist_bios_csv.close()


