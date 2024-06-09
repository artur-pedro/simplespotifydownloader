import os
import re
import spotipy
import sys
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.request
import yt_dlp
from pathlib import Path
from urllib.parse import quote
import glob
def load_any_dotenv():
    env_files = glob.glob('*env')
    if env_files:
        load_dotenv(env_files[0])
        return True
    else:
        return False
def clean_filename(filename):
    cleaned_filename = re.sub(r'[<>:"/\\|?*?]', '', filename)
    return cleaned_filename

def YoutubeAudioDownload(link, filename, index, format):
    if format not in ['mp3', 'ma4','webm', 'mp4']:
        raise ValueError("Invalid format. Choose either 'mp3', 'ma4', 'webm' or 'mp4'.")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{filename}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    if(format == 'ma4'):
        ydl_opts.update({
            'format':'bestaudio[ext=m4a]/mp4',
            'extract_audio': True,
            'audio_format': 'mp4',
            'audio_quality': '256K',
        })
    if format == 'mp3':
        ydl_opts.update({
            'extract_audio': True,
            'audio_format': 'mp3',
            'audio_quality': '256K',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '256',
            }]
        })
    if(format == 'mp4'):
        ydl_opts.update({
            'format':'bestaudio[ext=mp4]/mp4',
            'extract_audio': True,
            'audio_format': 'mp4',
            'audio_quality': '256K',
        })
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([link])
            print(f"{index} - {filename} was downloaded successfully")
            return True
        except Exception as e:
            print(f"Failed to download {filename}: {str(e)}")
            return False
def youtubeSearcher(artist_name, song, index):
    search_word = f"{artist_name} - {song}"
    url = "https://www.youtube.com/results?search_query=" + quote(search_word)
    link = urllib.request.urlopen(url)
    video_ids = re.findall(r"watch\?v=(\S{11})", link.read().decode('utf-8'))
    music_link = ("https://www.youtube.com/watch?v=" + video_ids[0])
    filename = f"{f'{artist_name} - {song}'}"
    filename = clean_filename(filename)
    print(f"Downloading {filename}")
    if (len(sys.argv) == 3):
        if YoutubeAudioDownload(music_link, filename, index, format=sys.argv[2]) == True:
            return True
        else:
            print(f"Failed to download {filename}")
            return False
    if (len(sys.argv) == 2):
        if YoutubeAudioDownload(music_link, filename, index, format="webm") == True:
            return True
        else:
            print(f"Failed to download {filename}")
            return False
def spotifyMusicSearcher(link_passed):
    if load_any_dotenv() == True or load_dotenv() == True:
        pass
    else:
        client_id = input("Cliente ID: ")
        client_secret = input("Cliente secret: ")
        with open(".env", "w") as f:
            f.write(f"CLIENT_ID='{client_id}'\n")
            f.write(f"CLIENT_SECRET='{client_secret}'")
    load_any_dotenv()
    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID", "")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
    session = spotipy.Spotify(requests_session=True, client_credentials_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET))
    link_received = link_passed
    if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", link_received):
        playlist_uri = match.groups()[0]
        playlistDownloader(playlist_uri, session)
    elif match := re.match(r"https://open.spotify.com/track/(.*)\?", link_received):
        song_uri = match.groups()[0]
        song_Downloader(song_uri, session)
    else:
        raise ValueError("Expected format: https://open.spotify.com/playlist/... or https://open.spotify.com/tracks/... ")

def song_Downloader(song_uri, session):
    try:
        track= session.track(song_uri)
    except Exception as e:
        os.remove(".env")
    track_name = track["name"]
    track_name2 = track_name
    track_name = clean_filename(track_name2)
    directory = os.path.join(os.getcwd(), track_name)
    os.makedirs(directory, exist_ok=True)
    DOWNLOADED_NAME = "downloaded.txt"
    track_artists = track["artists"]
    track_artist = ""
    for index, artist in enumerate(track_artists):
        track_artist += (artist["name"])
        if index < len(track_artists) - 1:
            track_artist += ", "
    os.chdir(track_name)
    with open(DOWNLOADED_NAME, "w", encoding="UTF-8") as downloaded_file:
        if youtubeSearcher(track_artist, track_name, index) == True:
            downloaded_file.write(f"{track_artist} - {track_name}\n")  

def playlistDownloader(playlist_uri, session):
    try:
         tracks = session.playlist_tracks(playlist_uri)["items"]
    except Exception as e:
        os.remove(".env")
    name_playlist = session.user_playlist(None, playlist_uri, "name")
    name_playlist = name_playlist["name"]
    directory = os.path.join(os.getcwd(), name_playlist)
    os.makedirs(directory, exist_ok=True)
    DOWNLOADED_NAME = "downloaded.txt"
    os.chdir(name_playlist)
    with open(DOWNLOADED_NAME, "w", encoding="UTF-8") as downloaded_file:
        for index, track in enumerate(tracks, 1):
            artist_name = ""
            song = track["track"]["name"]
            for artist_index, artist in enumerate(track["track"]["artists"]):
                artist_name += artist["name"]
                if artist_index < len(track["track"]["artists"]) - 1:
                    artist_name += ", "
            if youtubeSearcher(artist_name, song, index) == True:
                downloaded_file.write(f"{artist_name} - {song}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 2:
        print("Usage: python spotifyplaylistdownloader.py <spotify playlist> <format>")
        print("or: python spotifyplaylistdownloader.py <spotify playlist> format will be 'webm' ")
        sys.exit(1)
    playlist_link = sys.argv[1]
    spotifyMusicSearcher(playlist_link)
