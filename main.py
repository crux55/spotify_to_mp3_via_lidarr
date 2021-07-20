import configparser
import spotipy
import youtube_dl
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch

config = configparser.ConfigParser()
config.read('ConfigFile.properties')

print(config.get("ExampleSection", "example"))

SPOTIFY_CLIENT_ID = config.get("SPOTIPY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = config.get("SPOTIPY_CLIENT_SECRET")
ROOT_FOLDER = config.get("ROOT_FOLDER")

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

artist_name = "if these trees could talk"
album_name = "Red Forest"
artist_search = spotify.search(artist_name, 3, 0, "artist")
albums = spotify.artist_albums(artist_search['artists']['items'][0]['id'], album_type="album")

for item in albums['items']:
    if item['name'] == album_name:
        spotify_album = spotify.album(item['id'])
        for track in spotify_album['tracks']['items']:
            song_search_string = track['artists'][0]['name'] + "-" + track['name']
            print(song_search_string)
            results_list = YoutubeSearch(song_search_string, max_results=1).to_dict()
            best_url = "https://www.youtube.com{}".format(results_list[0]['url_suffix'])
            print(best_url)
            output_loc = ROOT_FOLDER = '%(title)s.%(ext)s'
            ydl_opts = {
                'format': 'bestaudio/best',
                'download_archive': 'downloaded_songs.txt',
                'outtmpl': output_loc,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([best_url])