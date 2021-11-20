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
import config

def auth(): 
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(config.client_id, config.client_secret, redirect_uri=config.redirect_uri, scope=config.scope))
    return sp

def open_lyrics(band_name,song_name):
    band_name = re.sub('The ', '', band_name)         
    song_name = re.sub('[\W_]+', '', song_name)       
    band_name = re.sub('[\W_]+', '', band_name) 
    open_new("https://www.azlyrics.com/lyrics/" + band_name.lower() + "/" + song_name.lower() + ".html")  #genius api later? az missing tracks

def song_refresh(window):
    try:
        current_song = sp.current_playback()
        song_dump = json.dumps(current_song,indent=4)
        data = json.loads(song_dump)
        band_name = data['item']['album']['artists'][0]['name']
        song_name = data['item']['name']
        window['-BN-'](band_name)      #  Updates display
        window['-SN-'](song_name)
        return [band_name, song_name] 
    except:
        window['-BN-']('no song detected')
        return None, None


def download(band_name, song_name, file_path):
    s = Search(band_name +" "+ song_name)
    youtube_obj = s.results[0]
    stream = youtube_obj.streams.get_by_itag(251)
    stream.download(file_path)
    return None

def interface_loop():
    band_name = ''
    song_name = ''
    layout = [
            [sg.Text( band_name, key ='-BN-', size=(None, None))], [sg.Text(song_name, key='-SN-', size=(None, None))],
            [sg.In(key='-FILE-')],        
            [sg.FolderBrowse("Download Location", target='-FILE-'),sg.Button('Open Lyrics'), sg.Button('Refresh'), sg.Button('Download'), sg.Button('Quit')]
            ]
    window = sg.Window('Lyric Lookup', layout)

    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read()
        if event == 'Open Lyrics':
            open_lyrics(band_name,song_name)
        elif event == 'Refresh':
            infolist = song_refresh(window)
            band_name = infolist[0]
            song_name = infolist[1]
        elif event == 'Download':
            file_path = values['-FILE-']
            download(band_name, song_name, file_path)
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
    window.close()
            
#  Doesn't work for artists that replace letters with symbols, '$uicideboy$', probably breaks with multiple artists
if __name__ == "__main__":
    sp = auth()
    interface_loop()
