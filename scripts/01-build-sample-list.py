import requests 
import base64
import json
import time

# =========================================================================

# A script to build my sample list. This uses a list of artists I manually chose, and pulls each of their related artists. After this script is run, artists who use she/her/they/them pronouns will be selected from the pool. 

# =========================================================================

# API Set Up ------------------------------------------------------

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

#-------------------------------------------------------------

searches = ["Lucy Dacus", "Phoebe Bridgers", "Julien Baker", "Mitski", "Snail Mail", "Soccer Mommy", "Japanese Breakfast", "Adrienne Lenker", "Julia Jacklin", "Angel Olsen", "Sharon van Etten", "Jay Som", "Waxahatchee", "Courtney Barnett", "Taylor Swift", "Lana del Rey", "Lorde", "Billie Eilish", "Olivia Rodrigo", "Adele", "SZA", "Clairo", "mxmtoon", "girl in red", "beabadoobee", "Samia", "Wallice", "Blü Eyes", "Jordana", "Orla Gartland", "Renee Rapp", "Indigo De Souza", "Remi Wolf", "Willow", "Arlo Parks", "Dora Jar", "Frankie Cosmos", "Grace Ives", "Kate Bollinger", "Becca Mancari", "Wilma Laverne Miner", "Margaret Glaspy", "Jade Bird", "Ada Lea", "Cornelia Murr", "Maggie Rogers", "Angie McMahon", "Natalie Prass", "HAIM" ]

initial_artist_ids = []

related_unique_ids = []
related_unqiue_names = []

artist_list = []

print(f"\nRetrieving IDs for {len(searches)} artists...")

#search artist names for their spotify ids
counter = 1 
for search in searches:
    search_url = f"https://api.spotify.com/v1/search/"
    search_params = {
        "q" : search,
        "type" : "artist",
        "limit" : 1
    }

    search_res = requests.get(url=search_url, headers=headers, params=search_params)
    search_json = search_res.json() 

    artist_id = search_json['artists']['items'][0]['id']
    artist_name = search_json['artists']['items'][0]['name']
    # artist_followers = search_json['artists']['items'][0]['followers']['total']
    # artist_genres = search_json['artists']['items'][0]['genres']
    # artist_image = search_json['artists']['items'][0]['images'][0]['url']
    # artist_popularity = search_json['artists']['items'][0]['popularity']

    artist_info = {
        "name" : artist_name,
        "id" : artist_id,
        # "followers" : artist_followers,
        # "genres" : artist_genres,
        # "image" : artist_image,
        # "popularity" : artist_popularity
    }

    print(f"{counter}: {artist_name}")
    initial_artist_ids.append(artist_id)
    related_unique_ids.append(artist_id)
    related_unqiue_names.append(artist_name)
    artist_list.append(artist_info)
    time.sleep(.5)
    counter += 1

print(artist_list)
print(related_unqiue_names)

#use initial artist ids to compile the master list of all of their related artists
print(f"\nFinding these artists' related artists...")

for artist_id in initial_artist_ids:
    print(f"{artist_id}----------")
    related_url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    related_res = requests.get(url=related_url, headers=headers)
    related_json = related_res.json()

    for result in related_json['artists']:

        if result['id'] not in related_unique_ids:
            related_unique_ids.append(result['id'])
            related_unqiue_names.append(result['name'])
            print(result['name'])
            artist_info = {
                "name" : result['name'],
                "id" : result['id'],
                # "followers" : result['followers']['total'],
                # "genres" : result['genres'],
                # "image" : result['images'][0]['url'],
                # "popularity" : result['popularity']   
            }
            artist_list.append(artist_info)
            time.sleep(.5)

print(f"{len(artist_list)} related artists found:")

print(f"\n{related_unqiue_names}\n")

with open(f"../data/raw/spotify_all_artists.json", 'w') as write_file:
    json.dump(artist_list, write_file, indent=2)

print("File written.")