# Simplespotifydownloader

  Download spotify songs and playlists with python
  
## Usage

First, go to the playlist or song on Spotify, click share, and copy the playlist URI or the song URI. Then open a shell terminal and run:

for a playlist
```shell
./python spotifyplaylistdownloader.py  <Playlist URI> <format>
```

for a song
```shell
./python spotifyplaylistdownloader.py  <Song URI> <format>
```

If you don't specify the format, the songs will be downloaded as .webm files
```shell
./python spotifyplaylistdownloader.py  <Song URI>
```

The script will automatically create a folder named after the song/playlist in the parent directory of the script, and download the corresponding song/songs into it. Additionally, it will generate a .txt file containing the names of the downloaded songs.
# Dependencies
Install the necessary dependencies by running:
```shell
pip install -r requirements.txt
```
or 
```shell
pip3 install -r requirements.txt
```

# Prerequisites
 You need to create an app on the [Spotify Developers Dashboard](https://developer.spotify.com/dashboard) and get your CLIENT_ID and CLIENT_SECRET.
 When you run the script for the first time, it will prompt you to enter these credentials and subsequently generate a .env file with your envars.
 To download the songs as mp3 files, you need have [FFMPEG](https://phoenixnap.com/kb/ffmpeg-windows) installed.
# Format
The format can be `mp3`, `mp4`, `ma4` or `webm`.
