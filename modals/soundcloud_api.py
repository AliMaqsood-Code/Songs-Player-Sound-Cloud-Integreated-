# This file is being used to play the songs from SoundCloud API

import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
DATA_FOLDER = "E:/University/4th Semester/Projects/OS/data"
ONLINE_SONGS_CSV = os.path.join(DATA_FOLDER, "online_songs.csv")
# ONLINE_SONGS_CSV = os.path.join(DATA_FOLDER, "extracted_songs.csv")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

def get_token():
    """Get OAuth token from SoundCloud API."""
    url = "https://api.soundcloud.com/oauth2/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, data=data)
    print("Fetching token...")
    if response.status_code == 200:
        token=response.json().get("access_token")
        # print(token)
        return response.json().get("access_token")
    else:
        print("❌ Error fetching token:", response.text)
        return None

def get_track_url(track_name, csv_file=ONLINE_SONGS_CSV):
    """Get track URL from the CSV file based on song name."""
    df = pd.read_csv(csv_file)

    df["title"] = df["title"].astype(str).str.strip().str.lower()
    track_name = track_name.strip().lower()

    track_row = df[df['title'] == track_name]
    print("Track URL recieved")
    
    if not track_row.empty:
        return track_row.iloc[0]['url']
    
    possible = df[df["title"].str.contains(track_name)]
    if not possible.empty:
        return possible.iloc[0]['url']

    return None

def resolve_track(track_name):
    """Resolve track info and get track ID for streaming."""
    token = get_token()
    # token = ACCESS_TOKEN
    if not token:
        return {"error": "Could not authenticate with SoundCloud API"}
    
    track_url = get_track_url(track_name)
    if not track_url:
        return {"error": f"Track '{track_name}' not found in CSV"}

    resolve_url = "https://api.soundcloud.com/resolve"
    print("Playing song now:", track_url)
    headers = {"Authorization": f"OAuth {token}"}
    params = {"url": track_url}
    
    try:
        response = requests.get(resolve_url, params=params, headers=headers, timeout=10)
        
        if response.status_code != 200:
            error_msg = response.json().get("error_description", response.text) if response.headers.get('content-type') == 'application/json' else response.text
            return {"error": f"Failed to resolve track: {error_msg[:100]}"}

        track_info = response.json()
        if not track_info.get("id"):
            return {"error": "Track has no ID - may not be streamable"}
        
        track_id = track_info.get("id")
        title = track_info.get("title", "Unknown Title")

        if not track_info.get("downloadable") and not track_info.get("policy"):
            print(f"⚠️  Warning: Track may not be publicly streamable")

        return {
            "title": title,
            "track_id": track_id
        }
    except Exception as e:
        return {"error": f"Exception during track resolution: {str(e)[:100]}"}
