import lyricsgenius
import json
import time
import re

# ========================================================================

# After narrowing down the previous list of related artists, this script gets the Genius artist information for each one. The list of artists to search is manually populated from the list of artists retrieved in the Unique Related Artists files, but the script could be re-written to pull directly from the JSON file. 
 
# ========================================================================

#--API Setup------------------------------------------

user_token = "USER TOKEN HERE"
genius = lyricsgenius.Genius(user_token,sleep_time=0.5,timeout=5, retries=3)

#--*** Search Input Here ***--------------------------

all_artist_names = ["Claud", "MUNA", "Leith Ross", "Haley Blais", "Sidney Gish", "The Japanese House", "Ethel Cain", "Lizzy McAlpine", "quinnie", "Suki Waterhouse", "Delaney Bailey", "Lady Lamb", "Caroline Rose", "Miya Folick", "Liza Anne", "Faye Webster", "Penelope Scott", "Rio Romeo", "Stella Donnelly", "Lala Lala", "Hazel English", "Hatchie", "illuminati hotties", "St. Vincent", "Tanukichan", "Okay Kaya", "Hand Habits", "Bedouine", "Gia Margaret", "Free Cake For Every Creature", "Jessica Pratt", "Katy Kirby", "Skullcrusher", "Aldous Harding", "Alice Phoebe Lou", "Molly Burch", "Cate Le Bon", "U.S. Girls", "Hurray For The Riff Raff", "Jenny Lewis", "Nilüfer Yanya", "Black Belt Eagle Scout", "Long Beard", "Fazerdaze", "Barrie", "Vagabon", "P.S. Eliot", "Laura Stevenson", "Bully", "Jen Cloher", "Demi Lovato", "Selena Gomez", "Alessia Cara", "Katy Perry", "Camila Cabello", "Halsey", "Meghan Trainor", "Fifth Harmony", "Selena Gomez & The Scene", "Ariana Grande", "Little Mix", "Sabrina Carpenter", "MARINA", "Lykke Li", "Azealia Banks", "Grimes", "FKA twigs", "Isabel LaRosa", "Fiona Apple", "Alexandra Savior", "Sky Ferreira", "King Princess", "Gracie Abrams", "Charli XCX", "Rina Sawayama", "Zella Day", "Maude Latour", "Mallrat", "Melanie Martinez", "Ellise", "Julia Michaels", "Bea Miller", "Ashe", "Tate McRae", "Madison Beer", "Noah Cyrus", "Nessa Barrett", "Lauren Spencer Smith", "Ruth B.", "Olivia O'Brien", "Sia", "Jessie J", "Kelly Clarkson", "P!nk", "Birdy", "Jess Glynne", "Christina Perri", "Emeli Sandé", "Ellie Goulding", "Lady Gaga", "Ella Henderson", "Christina Aguilera", "Kali Uchis", "H.E.R.", "Kehlani", "Alina Baraz", "Kiana Ledé", "Sabrina Claudio", "Jorja Smith", "Jhené Aiko", "Ella Mai", "Chloe x Halle", "Tinashe", "Doja Cat", "Summer Walker", "Victoria Monét", "Solange", "awfultune", "dodie", "Cavetown", "Tessa Violet", "chloe moriondo", "Beach Bunny", "Addison Grace", "Chevy", "Flower Face", "GRLwood", "carpetgarden", "Tommy Lefroy", "Annie DiRusso", "spill tab", "girlhouse", "Boyish", "fanclubwallet", "Devon Again", "Emily James", "Taylor Bickett", "Cate", "ROSIE", "Haley Joelle", "Grace Gaustad", "Lauren Weintraub", "NERIAH", "Alexa Cappelli", "Ashley Kutcher", "Maddie Zahm", "Avery Lynch", "JESSIA", "Rosie Darling", "Sody", "Jillian Rossi", "Whatever", "Dad", "Lauren Aquilina", "Greta Isaac", "Matilda Mann", "Olive Klug", "Baby Queen", "ella jane", "Emma Blackery", "Daisy the Great", "Gatlin", "FLETCHER", "Maisie Peters", "Lexi Jayde", "Zolita", "Chappell Roan", "Katie Gregson-MacLeod", "Lauren Sanderson", "Lennon Stella", "Squirrel Flower", "Blu DeTiger", "Hope Tala", "BENEE", "Dreamer Isioma", "Tkay Maidza", "Orion Sun", "MIA GLADSTONE", "Rico Nasty", "Ravyn Lenae", "Doechii", "Tierra Whack", "Raveena", "Coco & Clair Clair", "Bree Runway", "UMI", "Pip Millett", "Joy Crookes", "Biig Piig", "Lava La Rue", "JGrrey", "Cleo Sol", "Charlotte Day Wilson", "Madison McFerrin", "Yazmin Lacey", "Mereba", "Abby Sage", "Hana Vu", "Empress Of", "Tirzah", "Sudan Archives", "ML Buch", "Discovery Zone", "Sassy 009", "FELIVAND", "Freak Slug", "Salami Rose Joe Louis", "Helena Deland", "Jess Williamson", "Lydia Luce", "Shannon Lay", "Rosie Carney", "Erin Rae", "Andrea von Kampen", "Madeline Kenney", "Courtney Marie Andrews", "Caroline Spence", "Joy Williams", "Aoife O'Donovan", "Samantha Crain", "Hey Cowboy!", "Allie Crow Buckley", "Laura Elliott", "girlpuppy", "Rosie Tucker", "Miel", "Kississippi", "Allison Ponthier", "Esmé Patterson", "Oh Pep!", "Palehound", "Fenne Lily", "Ira Wolf", "The Staves", "The Wild Reeds", "Charlotte Cornfield", "Mia Joy", "Indigo Sparke", "Tenci", "Cassandra Jenkins", "Jana Horn", "Buzzy Lee", "Kelsey Lu", "Mega Bog", "SASAMI", "Hannah Cohen", "Betty Who", "The Aces", "VÉRITÉ", "Jack River", "Alex the Astronaut", "Alex Lahey", "Tia Gostelow", "Ruby Fields", "Kita Alexander", "E^ST", "Gretta Ray", "Meg Mac", "Eves Karydas", "Julia Holter", "Eleanor Friedberger", "Caitlin Rose", "Your Smith", "Holly Humberstone", "Caroline Polachek", "Shura"]

failed = []

counter = 1
total_search = len(all_artist_names)

for artist in all_artist_names:
    try: 
        artist_info = []
        artist_file = re.sub('[^A-Za-z0-9]+', '', artist).lower()

        print(f"------------ {counter}/{total_search} ------------------------------------")
        #--Setting up the request-----------------------------
        song_limit = 1 #just to verify this is the correct artist, check against pulled songs, can increase or decrease
        artist_data = genius.search_artist(artist,max_songs=song_limit)

        if artist_data is not None:

            #--Create Dictionary from results---------------------
            artist_dict = artist_data.to_dict()
            alt_name = artist_dict['alternate_names']
            desc = artist_dict['description']
            artist_id = artist_dict['id']
            artist_image_url = artist_dict['image_url']
            insta = artist_dict['instagram_name']
            name = artist_dict['name']

            artist_dict_short = {
                "name" : name,
                "id" : artist_id,
                "instagram_name": insta,
                "alternate_names" : alt_name,
                "description" : desc,
                "image_url" : artist_image_url,
            }

            artist_info.append(artist_dict_short)
            time.sleep(1)
    except:
        failed.append(artist)
    
    with open(f"../data/raw/genius_bios/{artist_file}.json", "w") as write_file:
        json.dump(artist_info, write_file, indent=2)

    print(f"========== {artist} file written. ==========")

    counter += 1

print(f"These artists failed: {failed}")