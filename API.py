import pandas as pd
import numpy as np

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests.exceptions

df = pd.read_csv('MitoExport.csv')
#df = df.drop(df.index[:18725])
df.shape
client_id = "fdd79f8f236742a99ed71d14b6bd322f"
client_secret = "3dc8ab2bc7f54757946021f044f30e39"

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)
try:
    # Make an API request that could potentially fail
    results = sp.search(q='invalid search query')
except spotipy.client.SpotifyException as e:
    # Catch the SpotifyException and retrieve the HTTP error code
    if isinstance(e.http_status, requests.exceptions.HTTPError):
        http_error_code = e.http_status.response.status_code
        print(f"HTTP error code: {http_error_code}")
        # Define a function to retrieve the preview URL for a track
def get_track_preview_url(id):
    try:
        track_info = sp.track(id)
        return track_info['preview_url']
    except spotipy.client.SpotifyException as e:
        print(f"Spotify API error: {e}")
        return None

# Create an empty DataFrame to store the results
track_df = pd.DataFrame(columns=['id', 'preview_url'])

# Loop over the tracks in the input DataFrame and retrieve the preview URL
for i in range(len(df)):
    id = df.iloc[i]['track_id']
    preview_url = get_track_preview_url(id)
    
    # Add the track ID and preview URL to the DataFrame if the URL is not None
    if preview_url is not None:
        track_df.loc[i] = [id, preview_url]
    
    # Print the progress
    print(f"Processed {i+1}/{len(df)} tracks")

# Print the resulting DataFrame
print(track_df)
