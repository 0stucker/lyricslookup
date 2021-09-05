import PySimpleGUI as sg
import spotipy
import string
import spotipy.oauth2 as oauth2
import spotipy.util as util
import json
import re
import webbrowser
from spotipy.oauth2 import SpotifyOAuth
#edge cases determined by how azlyrics formats urls and artist names
#doesn't work for artists that replace, '$uicideboy$', bands that start with 'the'
scope = "user-library-read,user-read-currently-playing,user-read-playback-state,user-read-private"
client_id = ''
client_secret = ''  #learn how credentials work for sharing script
redirect_uri = 'http://localhost:8080'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth( client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

def open_lyrics(bandname,songname):                 #genius api later? az missing tracks
    songname = re.sub('[\W_]+', '', songname)       #moving this here fixed display issues
    bandname = re.sub('[\W_]+', '', bandname)
    webbrowser.open_new("https://www.azlyrics.com/lyrics/" + bandname.lower() + "/" + songname.lower() + ".html") 

def songrefresh():
    currentsong = sp.current_playback()
    songdump = json.dumps(currentsong,indent=4)
    data = json.loads(songdump)
    for i in data['item']['album']['artists']:
         bandname= i['name']
    songname = data['item']['name']
    return [bandname, songname] 
            
bandname = '                                                  ' #text output matches this length
songname = '                                                              '
layout = [[sg.Text(bandname, key ='-BN-')], [sg.Text(songname, key='-SN-')],
          [sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Button('Open Lyrics'), sg.Button('Refresh'), sg.Button('Quit')]]

# Create the window
window = sg.Window('Lyric Lookup', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    elif event == 'Open Lyrics':
        open_lyrics(bandname,songname)
    elif event == 'Refresh':
        infolist = songrefresh()
        bandname = infolist[0]
        songname = infolist[1]
        window['-BN-'](infolist[0])
        window['-SN-'](infolist[1])

window.close()
