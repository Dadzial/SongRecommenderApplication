<template>
  <div class="container">
    <div class="app-icon">
      <img src="/sound.png" width="512" height="512" alt="SongRecommender" />
    </div>
    <button class="back-btn" @click="router.push('/')">← Back</button>
    <h1 class="title">Song Recommender</h1>

    <div class="search-wrapper">
      <SearchBar @search="handleSearch" />
    </div>

    <div class="examples">
      <SongTrial
          v-for="song in recommendedSongs"
          :key="song.id"
          :song="song"
      />
    </div>

    <p class="description">
      These are five songs chosen for you.<br />
      Enjoy listening!
    </p>

    <div class="footer">
      <img src="/src/assets/spotify_logo.png" alt="Spotify" />
      <span>Powered by Spotify</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"

import SongTrial from "../components/SongTrial.vue"
import SearchBar from "../components/SearchBar.vue"

const router = useRouter()

const recommendedSongs = ref([
  { id: 1, title: "Purple lace bra", artist: "Tate McRae", img: "https://picsum.photos/300?1" },
  { id: 2, title: "Purple lace bra", artist: "Tate McRae", img: "https://picsum.photos/300?2" },
  { id: 3, title: "Purple lace bra", artist: "Tate McRae", img: "https://picsum.photos/300?3" },
  { id: 4, title: "Purple lace bra", artist: "Tate McRae", img: "https://picsum.photos/300?4" },
  { id: 5, title: "Elegancja Francja", artist: "Bracia Figo Fagot", img: "https://picsum.photos/300?5" }
])

const handleSearch = (songs) => {
  window.location.reload()
}
</script>

<style scoped>
.container {
  position: relative;
  min-height: 100vh;
  background: radial-gradient(circle, #3a3a3a, #1f1f1f);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 100px;
  gap: 30px;
  color: white;
  text-align: center;
  box-sizing: border-box;
}

.app-icon {
  margin-bottom: 10px;
  height: 120px;
  width: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.app-icon img {
  width: 200%;
  height: 200%;
  object-fit: contain;
}

.back-btn {
  position: absolute;
  top: 20px;
  left: 20px;
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 16px;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.back-btn:hover {
  opacity: 1;
}

.title {
  font-size: 48px;
}

.search-wrapper {
  margin-bottom: 30px;
}

.examples {
  display: flex;
  gap: 20px;
}

.description {
  font-size: 22px;
}

.footer {
  display: flex;
  align-items: center;
  gap: 12px;
  opacity: 0.7;
}

.footer img {
  width: 32px;
}
</style>
