<template>
  <div class="card">
    <img :src="song.img" alt="cover" />
  </div>
</template>

<script setup>
defineProps({
  song: Object
})
</script>

<style scoped>
.card {
  width: 100%;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  border-radius: 8px;
  transition: transform 0.2s;
  background: #333;
  box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.card:hover {
  transform: scale(1.05);
}

img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
