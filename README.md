# 🎵 SoundWave - Music Player

A modern web-based music player application that lets you play music from both local storage and online sources (SoundCloud).

## Features

✨ **Local Music Playback**
- Browse and play MP3 files stored on your local system
- Automatic MP3 file discovery across multiple drives
- Track metadata extraction (title, artist, duration)
- Offline music playback

🎧 **Online Music Integration**
- Search and stream music from SoundCloud
- Browse popular tracks
- Play songs directly from the web interface
- Powered by SoundCloud API

🎨 **Modern User Interface**
- Clean, gradient-based design
- Responsive web interface
- Easy navigation between local and online music
- Real-time song scanning status

## Tech Stack

### Backend
- **Flask** - Web server framework
- **Python 3** - Core language
- **Pandas** - Data manipulation and CSV handling
- **Mutagen** - MP3 metadata extraction
- **Requests** - HTTP library for API calls
- **python-dotenv** - Environment variable management

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling with gradients and animations
- **JavaScript** - Interactive features and dynamic content loading

### APIs
- **SoundCloud API** - Music streaming and search

## Project Structure

```
.
├── app.py                      # Main Flask application
├── .env                        # Environment variables (not in repo)
├── .env.example               # Example environment configuration
├── data/
│   ├── local_songs.csv        # Local music metadata
│   ├── online_songs.csv       # SoundCloud music metadata
│   └── extracted_songs.csv    # Additional song data
├── modals/                    # Python modules
│   ├── api.py                 # API integration
│   ├── soundcloud_api.py      # SoundCloud API handler
│   ├── local_song_extract.py  # Local MP3 scanner
│   ├── playlist_extract.py    # Playlist management
│   ├── auth_key_extract.py    # Authentication utilities
│   └── testing_songs.py       # Testing module
├── templates/                 # HTML templates
│   ├── index.html             # Homepage
│   ├── local.html             # Local music page
│   ├── online.html            # Online music page
│   └── loader.html            # Loading page
└── static/                    # Frontend assets
    ├── scripts/
    │   ├── index.js           # Homepage logic
    │   ├── loader.js          # Loader logic
    │   ├── local.js           # Local music player
    │   └── online.js          # Online music player
    └── styles/
        ├── index.css          # Homepage styles
        ├── loader.css         # Loader styles
        ├── local.css          # Local music styles
        └── online.css         # Online music styles
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- MP3 files on your system (for local music feature)
- SoundCloud API credentials (for online music feature)

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd "github.com/PythonMindset/Songs-Player-Sound-Cloud-Integreated-"
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask pandas mutagen python-dotenv requests
   ```

4. **Set up environment variables**
   - Create a `.env` file based on `.env.example` with your SoundCloud API credentials:
   ```
   CLIENT_ID=your_soundcloud_client_id
   CLIENT_SECRET=your_soundcloud_client_secret
   ACCESS_TOKEN=your_soundcloud_access_token
   ```

5. **Verify file paths**
   - Update the `DATA_FOLDER` path in `app.py` if needed
   - Update scan paths in `modals/local_song_extract.py` (currently scans D:/ and E:/)

## Usage

### Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Features Overview

**Homepage**
- Choose between Local or Online music
- View available options with descriptions

**Local Music Player**
- Click "Browse Local" to load local songs
- The first visit will trigger a system scan for MP3 files
- Watch the loader page as music files are discovered
- Once scanning is complete, browse and play your music
- Songs must be longer than 2 minutes (configurable)

**Online Music Player**
- Search for songs by title or artist
- Browse available tracks from SoundCloud
- Click a song to play it directly
- Requires internet connection

## API Endpoints

### Routing
- `GET /` - Homepage
- `GET /local` - Local music player page
- `GET /online` - Online music player page
- `GET /loader` - File scanning page

### Data Endpoints
- `GET /search_songs?q=query` - Search online songs
- `GET /play?name=song_name` - Get track info
- `GET /stream/<track_id>` - Stream audio from SoundCloud
- `GET /scan_status` - Check local file scanning progress
- `GET /data/<filename>` - Serve data files
- `GET /local_music/<path>` - Serve local MP3 files

## Configuration

### Local Music Scanning
Edit `modals/local_song_extract.py`:
- **Minimum duration**: Change `min_duration=120` to scan songs shorter than 2 minutes
- **Scan paths**: Modify `start_paths = ["D:/", "E:/"]` to scan different drives

### Data Paths
Edit `app.py`:
- `DATA_FOLDER` - Location where CSV files are stored
- `ONLINE_SONGS_CSV` - Path to online songs database

## SoundCloud API Setup

To use the online music feature:

1. Visit [SoundCloud Developers](https://soundcloud.com/you/apps)
2. Register your application
3. Get your `CLIENT_ID` and `CLIENT_SECRET`
4. Add credentials to `.env` file
5. The app will handle OAuth authentication automatically

## How It Works

### Local Music Flow
1. User clicks "Browse Local"
2. Backend triggers `local_song_extract.list_long_mp3()`
3. System scans D:/ and E:/ drives for MP3 files
4. File metadata (title, duration) extracted using Mutagen
5. Data saved to `local_songs.csv`
6. Frontend updates with available songs
7. User clicks play → browser streams the MP3 file

### Online Music Flow
1. User searches for a song
2. Backend filters `online_songs.csv` by title/artist
3. User clicks play
4. Backend resolves song to SoundCloud track ID
5. Gets OAuth token from SoundCloud API
6. Streams audio through `/stream/<track_id>` endpoint
7. Browser plays the audio stream

## Troubleshooting

### No Local Songs Found
- Check if MP3 files exist on D:/ or E:/ drives
- Verify file permissions
- Ensure songs are longer than 2 minutes
- Check `data/local_songs.csv` to see what was found

### SoundCloud Playback Issues
- Verify API credentials in `.env`
- Check internet connection
- Some songs may be restricted by region or rights
- Check browser console for error messages

### File Path Errors
- Use forward slashes `/` in path configurations
- On Windows, paths like `E:/` work in Python
- Update `DATA_FOLDER` path to match your system

## Future Enhancements

- 🎼 Playlist creation and management
- 🔍 Advanced search filters
- ⭐ Favorites/bookmarking
- 📊 Play history and statistics
- 🎨 Theme customization
- 📱 Mobile app version
- 🔐 User authentication system
- 🎵 Equalizer and audio controls

## License

This is a university project (4th Semester, Operating Systems Project).

## Notes

- This application is designed for educational purposes
- Ensure you have the right to play music files from your local storage
- Respect SoundCloud's Terms of Service when using their API
- Large music libraries may take time to scan on first run

---

**Created for:** University 4th Semester Project - Operating Systems  
**Made with ❤️**
