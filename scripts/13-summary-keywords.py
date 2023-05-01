import json
import os
import re
import openai

# ====================================================================

# This script uses a second round of OpenAI Chat completion to pull keywords from the previously generated song lyric summaries. 

# ====================================================================

summaries = {}

openai.api_key = os.environ["OPENAI_API_KEY"]
system_setting = "Retrieve keywords from the provided paragraph."

with open("../data/compiled/gpt-summaries.json") as read_file:
    summary_json = json.load(read_file)
    
    artist_ids = list(summary_json.keys())
    
    total = len(artist_ids)
    counter = 1
    for artist in artist_ids:
        summaries[artist] = []
        for song in summary_json[artist]:
            gpt_summary = song['gpt_summary']
            gpt_no_numbers = re.sub("([-\s]\d.\d)", "", gpt_summary)
            gpt_no_paren = re.sub("\(([^\)]+)\)", "", gpt_no_numbers)
            gpt_no_sent = re.sub("[sS]entiment score","",gpt_no_paren)
            gpt_no_song = re.sub("The song is about ","", gpt_no_sent)
            gpt_clean = res = re.sub(r'[^\w\s]', '', gpt_no_song)
            summaries[artist].append(gpt_clean)
        summaries[artist] = ' '.join(summaries[artist])

        prompt = f"Provide me with 20 keywords from this text:{summaries[artist]}. Please keyods the topics formatted in a json list. Ignore proper nounds and the words 'narrator', 'singer', 'positive', and 'negative'."
        res = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                    {"role":"system", "content": system_setting},
                    {"role":"user", "content": prompt}
                    ]
                )
        
        gpt_keywords = res.choices[0].message.content
        summaries[artist] = gpt_keywords
        json.dump(summaries, open("../data/compiled/keywords.json", "w"), indent=2)
        print(f"{counter}/{total} {artist}: {gpt_keywords}\n")
        counter += 1