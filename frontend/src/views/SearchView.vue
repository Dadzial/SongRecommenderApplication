<template>
  <div class="container">
    <div class="app-icon">
      <img src="/sound.png" width="512" height="512" alt="SongRecommender" />
    </div>
    <h1 class="title">Song Recommender</h1>

    <div class="search-wrapper">
      <SearchBar @search="handleSearch" />
    </div>

    <div class="examples">
      <SongTrial
          v-for="song in exampleSongs"
          :key="song.id"
          :song="song"
      />
    </div>

    <p class="description">
      Write up to 5 songs that you like,<br />
      I'll find something new you might like
    </p>

    <div class="footer">
      <img src="/src/assets/spotify_logo.png" alt="Spotify" />
      <span>Powered by Spotify</span>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router"
import SearchBar from "../components/SearchBar.vue"
import SongTrial from "../components/SongTrial.vue"

const router = useRouter()

const exampleSongs = [
  { id: 1, title: "Song 1", img: "https://picsum.photos/300?1" },
  { id: 2, title: "Song 2", img: "https://picsum.photos/300?2" },
  { id: 3, title: "Song 3", img: "https://picsum.photos/300?3" }
]

const handleSearch = (songs) => {
  router.push({
    path: "/results",
    state: { songs }
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