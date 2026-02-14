let playlist = [];
let allSongs = [];
let currentPlaylist = []; // this holds the current playlist (play all / shuffle)

async function loadSongs() {
    try {
        const res = await fetch('/data/local_songs.csv');
        const text = await res.text();
        const lines = text.trim().split('\n');
        lines.shift(); // remove header

        allSongs = lines.map(line => {
            const [id, title, artist, duration, url] = line.split(',');
            return { name: title, artist, url, duration };
        });

        document.getElementById('totalSongsText').textContent =
            `${allSongs.length} songs available`;

        // Initialize Amplitude once with all songs
        Amplitude.init({
            songs: allSongs,
            waveforms: { sample_rate: 50 }
        });

        buildSongCards(allSongs);

    } catch (err) {
        console.error(err);
    }
}

function buildSongCards(songs) {
    const container = document.getElementById('songsContainer');
    container.innerHTML = "";

    songs.forEach((song, index) => {
        const card = document.createElement('div');
        card.className = 'song-card';
        card.innerHTML = `
            <div class="song-meta">
                <div class="song-title">${song.name}</div>
                <div class="song-artist">${song.artist}</div>
            </div>

            <div class="song-controls">
                <button class="play-btn" data-index="${index}">
                    <span class="material-icon">▶</span>
                </button>

                <button class="add-btn" data-index="${index}">
                    <span class="material-icon">＋</span>
                </button>
            </div>
        `;
        container.appendChild(card);
    });

    // Play button
    document.querySelectorAll('.play-btn').forEach(btn => {
        btn.onclick = e => {
            const idx = parseInt(e.currentTarget.dataset.index);
            Amplitude.playSongAtIndex(idx);
            showTopPlayer();
        };
    });

    // Add to playlist button
    document.querySelectorAll('.add-btn').forEach(btn => {
        btn.onclick = e => {
            const idx = parseInt(e.currentTarget.dataset.index);
            if (!playlist.includes(idx)) playlist.push(idx);
            renderPlaylist();
        };
    });
}

function showTopPlayer() {
    document.getElementById('top-player').classList.remove('hidden');
}

/** PLAYLIST MODAL */
const playlistButton = document.getElementById('playlist-button');
const playlistModal = document.getElementById('playlist-modal');
const closePlaylist = document.getElementById('close-playlist');
const playlistContainer = document.getElementById('playlist-container');

playlistButton.onclick = () => playlistModal.classList.remove('hidden');
closePlaylist.onclick = () => playlistModal.classList.add('hidden');

function renderPlaylist() {
    playlistContainer.innerHTML = "";

    playlist.forEach(idx => {
        const song = allSongs[idx];

        const div = document.createElement('div');
        div.className = 'playlist-item';
        div.innerHTML = `
            <span>${song.name} — ${song.artist}</span>
            <button class="remove-btn" data-index="${idx}">✕</button>
        `;

        playlistContainer.appendChild(div);
    });

    document.querySelectorAll('.remove-btn').forEach(btn => {
        btn.onclick = e => {
            const idx = parseInt(e.target.dataset.index);
            playlist = playlist.filter(i => i !== idx);
            renderPlaylist();
        };
    });
}

/** PLAY ALL */
document.getElementById('play-all').onclick = () => {
    if (!playlist.length) return;

    // Set the current playlist
    currentPlaylist = [...playlist];

    // Play the first song in playlist
    const firstSongIndex = currentPlaylist[0];
    Amplitude.playSongAtIndex(firstSongIndex);
    showTopPlayer();
};

/** SHUFFLE */
document.getElementById('shuffle').onclick = () => {
    if (!playlist.length) return;

    // Shuffle the playlist
    currentPlaylist = [...playlist].sort(() => Math.random() - 0.5);

    // Play the first song in shuffled playlist
    const firstSongIndex = currentPlaylist[0];
    Amplitude.playSongAtIndex(firstSongIndex);
    showTopPlayer();
};

loadSongs();
