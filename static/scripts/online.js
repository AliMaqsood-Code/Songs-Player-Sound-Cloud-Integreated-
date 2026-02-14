const searchInput = document.getElementById("song-search");
const songsList = document.getElementById("songs-list");
const customPlayer = document.getElementById("custom-player");
const customAudio = document.getElementById("audio");
const playBtn = document.getElementById("play-pause");
const progress = document.getElementById("progress");
const volume = document.getElementById("volume");
const titleDisplay = document.getElementById("playing-title");

let isPlaying = false;

playBtn.addEventListener("click", () => {
  console.log("Play/Pause button clicked");
  if (!customAudio.src) {
    console.warn("No audio source set");
    return;
  }
  if (customAudio.paused) {
    const playPromise = customAudio.play();
    if (playPromise !== undefined) {
      playPromise
        .then(() => {
          playBtn.textContent = "⏸️";
          isPlaying = true;
        })
        .catch((err) => {
          console.error("Play error:", err);
          alert(`Failed to play: ${err.message}`);
        });
    }
  } else {
    customAudio.pause();
    playBtn.textContent = "▶️";
    isPlaying = false;
  }
});

customAudio.addEventListener("timeupdate", () => {
  if (customAudio.duration) {
    progress.value = (customAudio.currentTime / customAudio.duration) * 100;
  }
});

customAudio.addEventListener("loadstart", () => {
  console.log("Audio loading started...");
});

customAudio.addEventListener("canplay", () => {
  console.log("Audio can play");
});

customAudio.addEventListener("stalled", () => {
  console.warn("Audio stream stalled");
});

customAudio.addEventListener("ended", () => {
  console.log("Audio playback ended");
  playBtn.textContent = "▶️";
  isPlaying = false;
  progress.value = 0;
});

progress.addEventListener("input", () => {
  if (customAudio.duration) {
    customAudio.currentTime = (progress.value / 100) * customAudio.duration;
  }
});

volume.addEventListener("input", () => {
  customAudio.volume = volume.value;
});

async function fetchSongs(query = "") {
  try {
    console.log("Fetching songs with query:");
    const res = await fetch(`/search_songs?q=${encodeURIComponent(query)}`);
    const songs = await res.json();
    renderSongs(songs);
  } catch (err) {
    console.error("Error fetching songs:", err);
  }
}

function renderSongs(songs) {
  songsList.innerHTML = songs
    .map(
      (song) => `
    <div class="song-card">
      <h3 title="${song.title}">${truncateText(song.title, 25)}</h3>
      <p title="${song.artist}">${truncateText(song.artist, 25)} • ${song.duration_min}</p>
      <button class="play-btn" data-title="${song.title}">Play</button>
    </div>
  `
    )
    .join("");
}

function truncateText(text, maxLength) {
  return text.length <= maxLength ? text : text.slice(0, maxLength) + "...";
}

async function playSong(title) {
  try {
    console.log("Playing song:", title);
    const res = await fetch(`/play?name=${encodeURIComponent(title)}`);
    const data = await res.json();

    if (data.error) {
      console.error("Backend error:", data.error);
      alert(`Error: ${data.error}`);
      return;
    }

    customAudio.src = `/stream/${data.track_id}`;
    titleDisplay.textContent = `🎵 Now Playing: ${data.title}`;
    customPlayer.style.display = "flex";
    
    customAudio.onerror = (error) => {
      console.error("Audio playback error:", error, customAudio.error);
      const errorMsg = customAudio.error ? customAudio.error.message : "Unknown error";
      alert(`Failed to play audio: ${errorMsg}`);
      playBtn.textContent = "▶️";
      isPlaying = false;
    };
    
    const playPromise = customAudio.play();
    if (playPromise !== undefined) {
      playPromise
        .then(() => {
          console.log("Audio playback started successfully");
          playBtn.textContent = "⏸️";
          isPlaying = true;
        })
        .catch((err) => {
          console.error("Play promise rejected:", err);
          alert(`Failed to play audio: ${err.message}`);
          playBtn.textContent = "▶️";
          isPlaying = false;
        });
    }
  } catch (err) {
    console.error("Error playing song:", err);
    alert(`Error: ${err.message}`);
  }
}

songsList.addEventListener("click", (e) => {
  console.log("Song list clicked:", e.target);
  if (e.target.classList.contains("play-btn")) {
    const songTitle = e.target.dataset.title;
    console.log("✅ PLAY BUTTON CLICKED!");
    console.log("Song Title from data-title:", songTitle);
    playSong(songTitle);
  } else {
    console.log("Clicked element is not a play button:", e.target.className);
  }
});

fetchSongs();
searchInput.addEventListener("input", (e) => fetchSongs(e.target.value));
