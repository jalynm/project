import vlc
import pafy

import urllib.request
import urllib.parse
import re

import time
import random

import json
import urllib.request

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


client_id = "50ce6b13e4714c3d87aa102059b01fe0"
client_secret = "7febc9be981f453d93b19d92c2d4c20b"

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_track_ids(user, playlist_id):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids


def get_track_features(id):
    meta = sp.track(id)
    features = sp.audio_features(id)

    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']

    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']

    track = [name, album, artist, release_date, length, popularity, danceability, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
    return track


def get_playlist_tracks(username,playlist_id):
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


while True:

    #get random song_id from playlist
    ids = get_track_ids('', '37i9dQZEVXcEFCXh5msbdI')
    song = get_track_features(random.choice(ids))
    track_name = song[0]
    artist = song[2]
    print(f"Track: {track_name}")
    print(f"Artist: {artist}")

    search_input = f"{track_name} {artist} audio"
    print(search_input)
    query_string = urllib.parse.urlencode({"search_query" : search_input})
    html_content = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
    video_ids = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
    url = "https://www.youtube.com/watch?v=" + video_ids[0]
    print(video_ids[0])

    #play song
    video = pafy.new(url)
    best = video.getbest()
    playurl = best.url

    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    player.audio_set_volume(80)
    player.play()

    #get length of track
    video_id = video_ids[0]
    API_KEY = "AIzaSyDstd8B0y1Lp5yiwSDtvYYbEd4ffPiIPHQ"

    search_url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={API_KEY}&part=contentDetails'
    req = urllib.request.Request(search_url)
    response = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(response)
    
    #try:
    all_data = data['items']
    duration = all_data[0]['contentDetails']['duration']
    minutes = int(duration[2:].split('M')[0])
    print(duration)
    seconds = int(duration[-3:-1])
    song_length = minutes * 60 + seconds
    
    print(song_length)

    #wait, repeat
    time.sleep(song_length - 5)

    #except ValueError:
        #print("Error")
