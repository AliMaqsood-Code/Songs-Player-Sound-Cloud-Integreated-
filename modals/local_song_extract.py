# This file is used to extract all the songs in your local storage.

import os
import csv
from mutagen.mp3 import MP3

DATA_FOLDER = "E:/University/4th Semester/Projects/OS/data"
CSV_PATH = os.path.join(DATA_FOLDER, "local_songs.csv")
scan_done = False

def format_duration(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"

def list_long_mp3(min_duration=120):
    global scan_done
    scan_done = False
    start_paths = ["D:/", "E:/"]  # Add other drives if needed
    long_mp3s = []
    song_id = 1

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(["id","title","artist","duration","url"])

        for drive in start_paths:
            print(f"\nScanning {drive} ...")
            for root, dirs, files in os.walk(drive):
                for file in files:
                    if file.lower().endswith(".mp3"):
                        full_path = os.path.join(root, file)
                        try:
                            audio = MP3(full_path)
                            duration = audio.info.length
                            if duration > min_duration:
                                title = os.path.splitext(file)[0]
                                artist = "Unknown Artist"
                                duration_str = format_duration(duration)

                                url_path = "/local_music/" + full_path.replace("\\","/")

                                writer.writerow([song_id, title, artist, duration_str, url_path])
                                print(f"{song_id}: {title} ({duration_str})")

                                long_mp3s.append({
                                    "id": song_id,
                                    "title": title,
                                    "artist": artist,
                                    "duration": duration_str,
                                    "url": url_path
                                })
                                song_id += 1
                        except Exception as e:
                            continue

    print(f"\n✅ Total MP3 files longer than 2 min: {len(long_mp3s)}")
    scan_done = True
    return long_mp3s
