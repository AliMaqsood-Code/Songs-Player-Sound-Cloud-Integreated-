# This file extracts songs from any public SoundCloud user and appends to an existing CSV
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import re

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
USERNAME = "mehpara-hussain-151667989"  # Change the username if needed

CSV_FILE = "extracted_songs.csv"  # Existing CSV to append to

headers = {
    "Authorization": f"OAuth {ACCESS_TOKEN}"
}

# Resolve user to get user ID
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
    for track in playlist.get("tracks", []):
        title = track.get("title", "")
        # Remove commas, quotes, double quotes
        title_clean = re.sub(r'[,"\']', '', title).strip()

        url = track.get("permalink_url", "")
        # Only keep the URL up to '?'
        url_clean = url.split("?")[0] if "?" in url else url

        duration_ms = track.get("duration")
        duration_min = round(duration_ms / 60000, 2) if duration_ms else None

        songs_data.append({
            "title": title_clean,
            "artist": track.get("user", {}).get("username", ""),
            "duration_ms": duration_ms,
            "duration_min": duration_min,
            "url": url_clean
        })

# Convert to DataFrame
df_new = pd.DataFrame(songs_data)

# Append to existing CSV if it exists
if os.path.exists(CSV_FILE):
    df_existing = pd.read_csv(CSV_FILE)
    # Concatenate and drop duplicates based on title + url
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.drop_duplicates(subset=["title", "url"], inplace=True)
else:
    df_combined = df_new

# Save back to CSV
df_combined.to_csv(CSV_FILE, index=False)
print(f"Saved {len(df_new)} new tracks. Total tracks in '{CSV_FILE}': {len(df_combined)}")
