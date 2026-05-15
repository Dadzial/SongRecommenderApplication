<template>
  <div class="container">
    <div class="app-icon">
      <img src="/sound.png" width="512" height="512" alt="SongRecommender" />
    </div>
    <h1 class="title">Song Recommender</h1>

    <div class="search-wrapper">
      <SearchBar @select="addSong" />
    </div>

    <div class="selected-songs-container">
      <div v-if="selectedSongs.length > 0" class="selected-songs-grid">
        <div v-for="(song, index) in selectedSongs" :key="song.track_id" class="song-item">
          <div class="card-wrapper">
            <SongTrial :song="song" />
            <button class="remove-btn" @click="removeSong(index)">×</button>
          </div>
          <div class="song-info">
            <p class="song-title">{{ song.track_name }}</p>
            <p class="song-artist">{{ song.artists }}</p>
          </div>
        </div>
      </div>
      <div v-else class="empty-state">
         <p class="hint">Your selected songs will appear here</p>
      </div>
    </div>

    <p class="description">
      Select up to 5 songs that you like,<br />
      I'll find something new you might like
    </p>

    <button 
      class="recommend-btn" 
      :disabled="selectedSongs.length === 0"
      @click="handleRecommend"
    >
      Find Recommendations
    </button>

    <div class="footer">
      <img src="/src/assets/spotify_logo.png" alt="Spotify" />
      <span>Powered by Spotify</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import SearchBar from "../components/SearchBar.vue"
import SongTrial from "../components/SongTrial.vue"
import Predict from "../services/Predict"

const router = useRouter()
const selectedSongs = ref([])

const addSong = (song) => {
  if (selectedSongs.value.length >= 5) return
  if (selectedSongs.value.some(s => s.track_id === song.track_id)) return

  song.img = `https://picsum.photos/seed/${song.track_id}/300`
  selectedSongs.value.push(song)
}

const removeSong = (index) => {
  selectedSongs.value.splice(index, 1)
}

const handleRecommend = async () => {
  const trackIds = selectedSongs.value.map(s => s.track_id)
  const recommendations = await Predict(trackIds)
  
  router.push({
    path: "/results",
    state: { recommendations }
  })
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: radial-gradient(circle, #3a3a3a, #1f1f1f);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 20px;
  gap: 25px;
  color: white;
  text-align: center;
  box-sizing: border-box;
}

.app-icon {
  height: 80px;
  width: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
}

.app-icon img {
  width: 150%;
  height: 150%;
  object-fit: contain;
}

.title {
  font-size: 36px;
  margin: 0;
}

.selected-songs-container {
  width: 100%;
  max-width: 1000px;
  min-height: 220px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.selected-songs-grid {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 30px;
}

.song-item {
  width: 160px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.card-wrapper {
  position: relative;
  width: 100%;
}

.remove-btn {
  position: absolute;
  top: -12px;
  right: -12px;
  background: #ff4444;
  color: white;
  border: 2px solid #222;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(0,0,0,0.5);
  transition: transform 0.1s;
}

.remove-btn:hover {
  transform: scale(1.1);
  background: #ff6666;
}

.song-info {
  margin-top: 12px;
  width: 100%;
}

.song-title {
  font-size: 15px;
  font-weight: bold;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.song-artist {
  font-size: 13px;
  color: #aaa;
  margin: 4px 0 0 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.recommend-btn {
  background: #1DB954;
  color: white;
  border: none;
  padding: 14px 40px;
  border-radius: 30px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 10px;
}

.recommend-btn:hover:not(:disabled) {
  transform: scale(1.05);
  background: #1ed760;
  box-shadow: 0 4px 15px rgba(29, 185, 84, 0.4);
}

.recommend-btn:disabled {
  background: #444;
  cursor: not-allowed;
  opacity: 0.6;
}

.hint {
  color: #666;
  font-style: italic;
  font-size: 18px;
}

.footer {
  margin-top: auto;
  display: flex;
  align-items: center;
  gap: 12px;
  opacity: 0.5;
}

.footer img {
  width: 24px;
}
</style>
