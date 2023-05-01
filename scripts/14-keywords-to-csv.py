import json
import csv

# ====================================================================

# Makes a CSV file from the compiled keywords for visualization in Tableau. The resulting CSV file is cleaned using OpenRefine to merge common keywords and reconcile redundancy. 

# ====================================================================

keywords_csv = open('../data/csv_files_for_analysis/keywords.csv', 'w')
key_writer = csv.writer(keywords_csv)

headers = {
    "artist_id" : "artist_id",
    "keyword" : "keyword"
}

key_writer.writerow(headers.values())

with open('../data/compiled/keywords.json') as read_file:
    keywords_json = json.load(read_file)

    artist_ids = list(keywords_json.keys())
    print(artist_ids)

    for artist in artist_ids:
        for keyword in keywords_json[artist]:
            write_dict = {
                "artist_id" : artist,
                "keyword" : keyword,
            }

            key_writer.writerow(write_dict.values())
