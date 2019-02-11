import sys
import os
sys.path.append(os.getcwd())
from fetchLyrics import scrape_lyrics, cleanup_lyrics
import csv

top_tracks = []

with open('regional-us-daily-latest.csv', 'rb') as top_tracks_file:
    tracks_reader = csv.reader(top_tracks_file)
    tracks_reader.next() # skip header row
    for row in tracks_reader:
        top_tracks.append({'title': unicode(row[0].decode('utf-8')), 'artist': unicode(row[1].decode('utf-8'))})

with open('usa_top_tracks_lyrics.txt', 'w') as lyrics_file:
    for track in top_tracks:
        raw_lyrics = scrape_lyrics(track['title'], track['artist'])
        if not raw_lyrics:
            continue # Skip songs that don't have lyrics (or couldn't be found on Genius)
        cleaned_lyrics = cleanup_lyrics(raw_lyrics.encode('utf-8'))
        lyrics_file.write(cleaned_lyrics)
        lyrics_file.write('\n\n') # leave a blank line between songs
