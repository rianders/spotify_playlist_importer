import csv
import os
import gradio as gr
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()

# Get Spotify Developer credentials from environment variables
SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]
SPOTIFY_USERNAME = os.environ["SPOTIFY_USERNAME"]
# Authenticate with Spotify API
scope = "playlist-modify-public playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Replace with your Spotify username
username = SPOTIFY_USERNAME

def import_playlist(csv_file):
    # Create a new Spotify playlist
    playlist_name = "My Imported Playlist"
    playlist_description = "Playlist imported from a CSV file"
    new_playlist = sp.user_playlist_create(username, playlist_name, description=playlist_description)

    # Read the CSV file and search for track URIs
    track_uris = []
    reader = csv.DictReader(csv_file.split("\n"))
    for row in reader:
        artist = row['Artist']
        title = row['Title']
        query = f"artist:{artist} track:{title}"
        
        results = sp.search(q=query, type='track', limit=1)
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            track_uris.append(track_uri)

    # Add the tracks to the newly created playlist
    if track_uris:
        sp.playlist_add_items(new_playlist['id'], track_uris)
        return f"Successfully imported playlist '{playlist_name}' with {len(track_uris)} tracks."
    else:
        return "No tracks found."

# Gradio interface
iface = gr.Interface(
    fn=import_playlist,
    inputs=gr.inputs.Textbox(lines=18, label="Paste CSV Content"),
    outputs="text",
    title="CSV to Spotify Playlist",
    description="Import a playlist from a CSV file to your Spotify account."
)

iface.launch()
