# How Sad Are the Sad Girls?
Alyse Delaney, Pratt MSLIS '24<br>Final Project for INFO 664: Programming for Cultural Heritage

This project aims to debunk the "Sad Girl Indie Music" trope through data. Read more about the project [here]().

## Data
*(how-sad-are-the-sad-girls/data/...)*

Data is collected using Python scripts that pull from the Spotify, Genius, and OpenAI APIs. 

### ../compiled_jsons/
Raw data pulled from the APIs, formatted as JSON files. 

### ../csv_files_for_analysis/
CSV files for visualization in Tableau. These files include artist data (Spotify Artist information, Genius, biographies, Spotify top 10 tracks, and generated keywords/summaries) and full track data (Spotify track metadata and track attributes) for each artists' entire discography available on Spotify.  

### ../sample_development/
A JSON file containing all unique related artists for the artists in the preliminary sample list. 

### ../segmented_by_artist/
Data separated by artist including full Genius data for each artists' top ten tracks, artist information, and each artist's available Track ID's on Spotify. Data was segmented by artist in the event that a script failed while pulling from the APIs. The resulting data is compiled in *../compiled_jsons/*

## Python Scripts
*(how-sad-are-the-sad-girls/scripts/...)*

### 01-build-sample-list.py
A script to build my sample list. This uses a list of artists I manually chose, and pulls each of their related artists. After this script is run, artists who use she/her/they/them pronouns will be selected from the pool.

### 02-get-genius-artist-bios.py
After narrowing down the previous list of related artists, this script gets the Genius artist information for each one. The list of artists to search is manually populated from the list of artists retrieved in the Unique Related Artists files, but the script could be re-written to pull directly from the JSON file.

### 03-compile-artists.py
This merges the spotify data and genius data for each artist into one compiled file. It pulls additional information for the artists' top tracks (NOTE: The full data including attributes for the Top Tracks no longer needs to be pulled in this script, as it will be retrieved later on in the project. All that is needed is the top track name and ID to be used in the next script). 

### 04-search-song-data-genius.py
This pulls the complete song data, including production data, lyrics, and annotations, from the Genius API for each of the artists' top tracks. 

### 05-compile-songs.py
This merges the top track song data from the previous script into one JSON file, only including the relevant fields for analysis. 

### 06-get-all-track-ids-by-artist.py
Retreives all Track ID's for the artists listed in Compiled_Artist_Info.json. This list of Artist IDs is manually populated here, but could also be written to pull them directly from the JSON file.

Spotify does not have an API endpoint to retrieve all of an artist's tracks, so the script first retrieves all albums and singles for each artist, then retrieves the unique track IDs in each of these albums. The resulting data is dropped into a separate JSON file for each artist. This takes a while to run and it's easy to max out the API limits, so adjust list of artist ID's as necessary. Might have to do in several batches.

### 07-bulk-track-data-call.py
This gets the track data from Spotify for every one of the artists' songs. Track data is requested in batches of 50. 

### 08-bulk-track-features-call.py
This gets the track features for each of the artists' songs. Track features are requested in batches of 100. 

### 09-merge-track-data.py
Combines the track data and track features into one compiled JSON file. 

### 10-make-track-csv.py
Makes a CSV file from the compiled track data for visualization in Tableau. 

### 11-make-genre-csv.py
Compiles a csv with artists' genres by row for visualization in Tableau. 

### 12-openai-summarize-lyrics.py
This script uses the OpenAI Chat Completion tool to generate a summary of each of the artists' Top 10 Tracks based on their lyrics. 

### 13-summary-keywords.py
This script uses a second round of OpenAI Chat completion to pull keywords from the previously generated song lyric summaries. 

### 14-keywords-to-csv.py
Makes a CSV file from the compiled keywords for visualization in Tableau. The resulting CSV file is cleaned using OpenRefine to merge common keywords and reconcile redundancy. 

### 15-make-bios-csv.py
This script compiles the artist bios into a CSV file for analysis in Tableau. If an artist bio is not available, it creates a line "This artist doesn't have a bio yet! Stay tuned...". If the artist bio is over 500 characters long, the biography is summarized using the OpenAI Chat Completion tool. 

### 16-top-tracks-take-two.py
Retrieves each of the artists' top 10 tracks at the given moment and compiles the data into a CSV file for analysis in Tableau. 

