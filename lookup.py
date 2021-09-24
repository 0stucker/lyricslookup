import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Button, Output
import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util
import json
import re
from pytube import Search
from webbrowser import open_new
from spotipy.oauth2 import SpotifyOAuth

def auth(): 
    scope = "user-library-read,user-read-currently-playing"
    client_id = ''
    client_secret = ''  #learn how credentials work for sharing script
    redirect_uri = 'http://localhost:8080'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth( client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
    return sp

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

def download(bandname, songname, filepath):
    s = Search(bandname +" "+ songname)
    ytobj = s.results[0]
    stream = ytobj.streams.get_by_itag(251)
    stream.download(filepath)
    return None

        
#doesn't work for artists that replace letters with symbols, '$uicideboy$', probably breaks with multiple artists

sp = auth()
bandname = '                                                  ' #text display output matches this length, can probably be fixed with size()
songname = '                                                              '
layout = [[sg.Text(bandname, key ='-BN-')], [sg.Text(songname, key='-SN-')],
          [sg.In(key='-FILE-')],        
          [sg.FolderBrowse("Download Location", target='-FILE-'),sg.Button('Open Lyrics'), sg.Button('Refresh'), sg.Button('Download'), sg.Button('Quit')]]
window = sg.Window('Lyric Lookup', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    if event == 'Open Lyrics':
        open_lyrics(bandname,songname)
    elif event == 'Refresh':
        infolist = songrefresh()
        bandname = infolist[0]
        songname = infolist[1]
    elif event == 'Download':
        filepath = values['-FILE-']
        download(bandname, songname, filepath)
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

window.close()
