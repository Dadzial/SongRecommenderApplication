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
  width: 180px;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  transition: transform 0.2s;
  background: #333;
}

.card:hover {
  transform: scale(1.08);
}

img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>