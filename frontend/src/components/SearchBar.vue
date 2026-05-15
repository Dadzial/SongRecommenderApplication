<template>
  <div class="search-container">
    <div class="search-bar">
      <input
          v-model="query"
          @input="onInput"
          @keydown.enter="handleEnter"
          placeholder="Search for a song (e.g. Bohemian Rhapsody)"
      />
      <div class="button-group">
        <span class="separator">|</span>
        <button @click="handleSearch">
          <img src="/src/assets/search_icon.png" alt="search" />
        </button>
      </div>
    </div>

    <!-- Dropdown z wynikami -->
    <ul v-if="results.length > 0 && showDropdown" class="results-list">
      <li 
        v-for="song in results" 
        :key="song.track_id" 
        @click="selectSong(song)"
        class="result-item"
      >
        <span class="song-name">{{ song.track_name }}</span>
        <span class="artist-name">{{ song.artists }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue"
import searchSongs from "../services/SongsQuery.ts"

const emit = defineEmits(["select"])
const query = ref("")
const results = ref([])
const showDropdown = ref(false)
let debounceTimer = null

const onInput = () => {
  clearTimeout(debounceTimer)
  if (query.value.length < 2) {
    results.value = []
    return
  }

  debounceTimer = setTimeout(async () => {
    results.value = await searchSongs(query.value)
    showDropdown.value = true
  }, 300)
}

const selectSong = (song) => {
  emit("select", song)
  query.value = ""
  results.value = []
  showDropdown.value = false
}

const handleEnter = () => {
  if (results.value.length > 0) {
    selectSong(results.value[0])
  }
}

// Zamykanie dropdownu po kliknięciu poza nim
const closeDropdown = (e) => {
  if (!e.target.closest('.search-container')) {
    showDropdown.value = false
  }
}

onMounted(() => window.addEventListener('click', closeDropdown))
onUnmounted(() => window.removeEventListener('click', closeDropdown))
</script>

<style scoped>
.search-container {
  position: relative;
  width: 600px;
}

.search-bar {
  display: flex;
  align-items: center;
  background: #333;
  border-radius: 25px;
  padding: 10px 20px;
  border: 1px solid #444;
}

input {
  flex: 1;
  border: none;
  background: transparent;
  color: white;
  outline: none;
  font-size: 18px;
}

.button-group {
  display: flex;
  align-items: center;
}

.separator {
  color: #666;
  margin: 0 10px;
}

button {
  background: none;
  border: none;
  cursor: pointer;
}

button img {
  width: 20px;
  height: 20px;
}

.results-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #222;
  border-radius: 12px;
  margin-top: 8px;
  padding: 0;
  list-style: none;
  z-index: 1000;
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #444;
  text-align: left;
}

.result-item {
  padding: 12px 20px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  border-bottom: 1px solid #333;
}

.result-item:hover {
  background: #333;
}

.song-name {
  color: white;
  font-weight: bold;
}

.artist-name {
  color: #aaa;
  font-size: 14px;
}
</style>
