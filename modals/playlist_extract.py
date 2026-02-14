# This file will be used to extract the required data from the playlist of any public user on SoundCloud.
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
USERNAME = "ali-maqsood-319387361" #You can change the user name here

headers = {
    "Authorization": f"OAuth {ACCESS_TOKEN}"
}
user_url = f"https://soundcloud.com/{USERNAME}"
resolve_endpoint = f"https://api.soundcloud.com/resolve?url={user_url}"
resp = requests.get(resolve_endpoint, headers=headers)
if resp.status_code != 200:
    print("Error resolving user:", resp.status_code, resp.text)
    exit()

user_info = resp.json()
USER_ID = user_info.get('id')
if not USER_ID:
    print("Failed to get USER_ID")
    exit()

print(f"Resolved username '{USERNAME}' to USER_ID: {USER_ID}")

# Fetch playlists
playlists_url = f"https://api.soundcloud.com/users/{USER_ID}/playlists"
resp = requests.get(playlists_url, headers=headers)
if resp.status_code != 200:
    print("Error fetching playlists:", resp.status_code, resp.text)
    exit()

playlists = resp.json()
if not playlists:
    print("No playlists found for this user.")
    exit()

# Collect songs from all playlists
songs_data = []
for playlist in playlists:
    playlist_title = playlist.get("title")
    for track in playlist.get("tracks", []):
        songs_data.append({
            "title": track.get("title"),
            "artist": track.get("user", {}).get("username"),
            "duration_ms": track.get("duration"),
            "duration_min": round(track.get("duration") / 60000, 2) if track.get("duration") else None,
            "url": track.get("permalink_url")
        })

df = pd.DataFrame(songs_data)
csv_filename = f"{USERNAME}_soundcloud_playlist_songs.csv"
df.to_csv(csv_filename, index=False)
print(f"Saved {len(songs_data)} tracks from playlists to {csv_filename}")
