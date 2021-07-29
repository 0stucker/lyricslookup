import PySimpleGUI as sg
import spotipy
import string
import spotipy.oauth2 as oauth2
import spotipy.util as util
import json
import webbrowser
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read,user-read-currently-playing,user-read-playback-state,user-read-private"
client_id = ''
client_secret = '' #py2exe credentials?
redirect_uri = 'http://localhost:8080'
bannedsymbols = '!,.@&)('
sp = spotipy.Spotify(auth_manager=SpotifyOAuth( client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

def open_lyrics(bandname,songname): #genius api later? az missing tracks
    webbrowser.open_new("https://www.azlyrics.com/lyrics/" + bandname + "/" + songname + ".html") 

def songrefresh():
    currentsong = sp.current_playback()
    songdump = json.dumps(currentsong,indent=4)
    data = json.loads(songdump)
    for i in data['item']['album']['artists']:
         bandname= i['name']
    songname = data['item']['name']
    songnameBEFORE = songname
    bandnameBEFORE = bandname
    songname = songname.replace(" ", "")
    bandname = bandname.replace(" ", "")
    bandname = bandname.replace(bannedsymbols, "") #less lines 
    songname = songname.lower()
    bandname = bandname.lower()
    for c in songname:
         for c in bannedsymbols:
            songname = songname.replace(c, "")
    return [bandname, songname, bandnameBEFORE, songnameBEFORE]
        
    

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
        window['-BN-'](infolist[2])
        window['-SN-'](infolist[3])

window.close()
