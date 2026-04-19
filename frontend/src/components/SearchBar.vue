<template>
  <div class="search">
    <input
        v-model="query"
        placeholder="e.g Bracia Figo Fagot – Bożenko"
    />
    <button @click="handleSearch">
      <span class="separator" aria-hidden="true">|</span>
      <img src="/src/assets/search_icon.png" alt="search" />
    </button>
  </div>
</template>

<script setup>
import { ref } from "vue"

const emit = defineEmits(["search"])
const query = ref("")

const handleSearch = () => {
  const songs = query.value
      .split(",")
      .map(s => s.trim())
      .filter(s => s)

  if (songs.length > 5) {
    alert("Max 5 songs!")
    return
  }

  emit("search", songs)
}
</script>

<style scoped>
.search {
  display: flex;
  background: #555;
  border-radius: 25px;
  padding: 10px 15px;
  width: 600px;
}

input {
  flex: 1;
  border: none;
  background: transparent;
  color: white;
  outline: none;
  font-size: 18px;
}

.search {
  display: flex;
  align-items: center;
  background: #555;
  border-radius: 25px;
  padding: 10px 15px;
  width: 600px;
}

button {
  background: none;
  border: none;
  cursor: pointer;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 36px;
  height: 36px;
  flex-shrink: 0;
}

.separator {
  color: white;
  font-size: 18px;
  line-height: 1;
  margin-right: 6px;
}

button img {
  width: 18px !important;
  height: 18px !important;
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
</style>