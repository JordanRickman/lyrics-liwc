import spotipy
import spotipy.util as util
import ConfigParser
import sys

KEYS_FILE_LOCATION = 'KEYS.conf'

keys = ConfigParser.ConfigParser()
keys.read(KEYS_FILE_LOCATION)
access_token = keys.get('Spotify', 'access_token')
if not access_token: raise Exception('No Spotify access token specified in ' + KEYS_FILE_LOCATION)

def get_tracks():
    spotify = spotipy.Spotify(auth=access_token)
    top_tracks = spotify.current_user_top_tracks(limit=50, offset=0, time_range='medium_term')
    return [ {'title': item['name'], 'artist': item['artists'][0]['name']} for item in top_tracks['items'] ]

if __name__ == '__main__':
    top_tracks = get_tracks()
    for track in top_tracks:
        print u'"{}" by {}'.format(track['title'], track['artist'])
