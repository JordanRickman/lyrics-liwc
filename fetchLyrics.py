import ConfigParser
import requests
from bs4 import BeautifulSoup
import re

KEYS_FILE_LOCATION = 'KEYS.conf'

keys = ConfigParser.ConfigParser()
keys.read(KEYS_FILE_LOCATION)
access_token = keys.get('Genius', 'access_token')
if not access_token: raise Exception('No Genius access token specified in ' + KEYS_FILE_LOCATION)

def request_song_info(song_title, artist_name):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + access_token}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    return response

def get_song_url(song_title, artist_name):
    response = request_song_info(song_title, artist_name)
    json = response.json()
    remote_song_info = None

    for hit in json['response']['hits']:
        if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
            remote_song_info = hit
    if remote_song_info:
        return remote_song_info['result']['url']
    return None

def scrape_lyrics(song_title, artist_name):
    song_url = get_song_url(song_title, artist_name)
    if not song_url:
        return None # TODO debug log
    page = requests.get(song_url)
    html = BeautifulSoup(page.text, 'html.parser')
    return html.find('div', class_='lyrics').get_text()

def cleanup_lyrics(raw_lyrics):
    lines = raw_lyrics.split('\n')
    # remove (1) blank lines, and (2) markers like "[Intro]", "[Chorus]", "[Verse 2]"
    filtered_lines = [line for line in lines if (line and not re.match(r'\[.*\]', line))]
    return '\n'.join(filtered_lines)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        song_title = sys.argv[1]
        artist_name = sys.argv[2]
    else:
        print "Usage: %s 'song title' 'artist'" % (sys.argv[0],)
        sys.exit()

    raw_lyrics = scrape_lyrics(song_title, artist_name).encode('utf-8')
    print cleanup_lyrics(raw_lyrics)
