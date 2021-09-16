import PySimpleGUI as sg
import spotipy
import string
import spotipy.oauth2 as oauth2
import spotipy.util as util
import json
import re
from webbrowser import open_new
from spotipy.oauth2 import SpotifyOAuth

def open_lyrics(bandname,songname):
    bandname = re.sub('The ', '', bandname)         
    songname = re.sub('[\W_]+', '', songname)       
    bandname = re.sub('[\W_]+', '', bandname) 
    open_new("https://www.azlyrics.com/lyrics/" + bandname.lower() + "/" + songname.lower() + ".html")  #genius api later? az missing tracks

def songrefresh():
    currentsong = sp.current_playback()
    songdump = json.dumps(currentsong,indent=4)
    data = json.loads(songdump)
    for i in data['item']['album']['artists']:
         bandname= i['name']
    songname = data['item']['name']
    window['-BN-'](bandname)      #update display
    window['-SN-'](songname)
    return [bandname, songname] 
        
#doesn't work for artists that replace letters with symbols, '$uicideboy$', probably breaks with multiple artists
scope = "user-library-read,user-read-currently-playing,user-read-playback-state,user-read-private"
client_id = ''
client_secret = ''  
redirect_uri = 'http://localhost:8080'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth( client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

bandname = '                                                  ' #text display output matches this length
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

window.close()
