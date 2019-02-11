import sys
import os
sys.path.append(os.getcwd())
from fetchTopSongs import get_tracks
from fetchLyrics import scrape_lyrics, cleanup_lyrics
import csv

top_tracks = get_tracks()

with open('user_top_tracks.csv', 'wb') as top_tracks_file:
    tracks_writer = csv.writer(top_tracks_file)
    tracks_writer.writerow(['Title', 'Artist'])
    for track in top_tracks:
        tracks_writer.writerow([track['title'].encode('utf-8'), track['artist'].encode('utf-8')])

with open('user_top_tracks_lyrics.txt', 'w') as lyrics_file:
    for track in top_tracks:
        raw_lyrics = scrape_lyrics(track['title'], track['artist'])
        if not raw_lyrics:
            continue # Skip songs that don't have lyrics (or couldn't be found on Genius)
        cleaned_lyrics = cleanup_lyrics(raw_lyrics.encode('utf-8'))
        lyrics_file.write(cleaned_lyrics)
        lyrics_file.write('\n\n') # leave a blank line between songs
