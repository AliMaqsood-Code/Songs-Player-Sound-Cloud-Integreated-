from flask import Flask, render_template, jsonify, request, Response, send_from_directory
from modals import local_song_extract, soundcloud_api
import pandas as pd
import os, requests
from dotenv import load_dotenv
from threading import Thread
# netlify
load_dotenv()
app = Flask(__name__)

# ---------------- DATA ----------------
DATA_FOLDER = "E:/University/4th Semester/Projects/OS/data"
# ONLINE_SONGS_CSV = os.path.join(DATA_FOLDER, "extracted_songs.csv")
ONLINE_SONGS_CSV = os.path.join(DATA_FOLDER, "online_songs.csv")
online_songs_df = pd.read_csv(ONLINE_SONGS_CSV)
LOCAL_SONGS_CSV = os.path.join(DATA_FOLDER, "local_songs.csv")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# ---------------- LOCAL ROUTES ----------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loader')
def loader():
    Thread(target=local_song_extract.list_long_mp3).start()
    return render_template('loader.html')

@app.route('/scan_status')
def scan_status():
    return jsonify({"done": local_song_extract.scan_done})

@app.route("/data/<filename>")
def serve_data(filename):
    return send_from_directory(DATA_FOLDER, filename)

@app.route('/local_music/<path:filename>')
def serve_local_music(filename):
    if filename.startswith("/"):
        filename = filename[1:]
    system_path = filename.replace("/", os.sep)
    if os.path.exists(system_path):
        return send_from_directory(os.path.dirname(system_path), os.path.basename(system_path))
    else:
        return "File not found", 404

@app.route('/local')
def local_songs():
    return render_template('local.html')

# ---------------- ONLINE ROUTES ----------------
@app.route('/online')
def online():
    return render_template("online.html")

@app.route('/search_songs')
def search_songs():
    query = request.args.get("q", "").lower()
    if query:
        filtered = online_songs_df[
            online_songs_df['title'].str.lower().str.contains(query) |
            online_songs_df['artist'].str.lower().str.contains(query)
        ]
    else:
        filtered = online_songs_df.head(20)
    return jsonify(filtered.to_dict(orient="records"))

@app.route('/play')
def play():
    track_name = request.args.get("name")
    if not track_name:
        return jsonify({"error": "No song name provided"}), 400

    track_info = soundcloud_api.resolve_track(track_name)
    print("Got the request for playing:", track_info)
    if "error" in track_info:
        return jsonify({"error": track_info['error']}), 400

    if not track_info.get("track_id"):
        return jsonify({"error": "Failed to get track ID"}), 400

    return jsonify({
        "title": track_info["title"],
        "track_id": track_info["track_id"]
    })

@app.route("/stream/<track_id>")
def stream(track_id):
    token = soundcloud_api.get_token()
    print("Playing song now:", track_id)
    if not token:
        return "❌ Could not authenticate", 500

    url = f"https://api.soundcloud.com/tracks/{track_id}/stream"
    headers = {"Authorization": f"OAuth {token}"}
    
    try:
        r = requests.get(url, headers=headers, stream=True, timeout=10)
        
        if r.status_code != 200:
            print(f"❌ Stream request failed with status {r.status_code}: {r.text[:200]}")
            return f"Failed to get stream: {r.status_code}", 400
        
        content_type = r.headers.get('content-type', 'application/octet-stream')
        print(f"Stream content-type: {content_type}")
        
        return Response(r.iter_content(chunk_size=4096), 
                    content_type=content_type or "audio/mpeg",
                    headers={"Accept-Ranges": "bytes"})
    except Exception as e:
        print(f"❌ Stream error: {str(e)}")
        return f"Error streaming audio: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
