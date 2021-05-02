import spotipy
import string
import spotipy.oauth2 as oauth2
import spotipy.util as util
import json
import webbrowser
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read,user-read-currently-playing,user-read-playback-state,user-read-private"
client_id = ''
client_secret = ''
redirect_uri = ''
bannedsymbols = '!,.@&)('

sp = spotipy.Spotify(auth_manager=SpotifyOAuth( client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
yo2 = sp.current_playback()

songdump = json.dumps(yo2,indent=4)
data = json.loads(songdump)

for i in data['item']['album']['artists']:
   bandname= i['name']

songname = data['item']['name']
songname = songname.replace(" ", "")
bandname = bandname.replace(" ", "")
songname = songname.lower()
bandname = bandname.lower()
for c in songname:
    for c in bannedsymbols:
        songname = songname.replace(c, "")

webbrowser.open_new("https://www.azlyrics.com/lyrics/" + bandname + "/" + songname + ".html")
