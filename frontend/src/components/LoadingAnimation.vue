<script setup lang="ts">

</script>

<template>
  <div class="loader-container">
    <div class="flower-loader">
      <div class="petal"></div>
      <div class="petal"></div>
      <div class="petal"></div>
      <div class="petal"></div>
    </div>
    <p class="loading-text">Finding the perfect plants...</p>
  </div>
</template>

<style scoped>
.loader-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.flower-loader {
  display: flex;
  flex-wrap: wrap;
  width: 6rem;
  height: 6rem;
  animation: rotate 2.5s infinite linear;
}

.petal {
  width: 1.5rem;
  height: 1.5rem;
  background-color: #b7d5ac;
  margin: 0.75rem;
  border-radius: 2rem 1rem 1rem 2rem;
  box-shadow: 0 0.5rem 0.4rem rgba(0,0,0,0.1);
  animation: bloom 1.5s infinite ease-in-out alternate;
}

.petal:nth-child(1) { border-radius: 2rem 0.5rem 2rem 2rem; animation-delay: 0s; }
.petal:nth-child(2) { border-radius: 0.5rem 2rem 2rem 2rem; animation-delay: 0.2s; }
.petal:nth-child(3) { border-radius: 2rem 2rem 2rem 2rem; animation-delay: 0.4s; }
.petal:nth-child(4) { border-radius: 2rem 2rem 0.5rem 2rem; animation-delay: 0.6s; }

.loading-text {
  margin-top: 1.5rem;
  color: #666;
  font-size: 1.5rem;
  font-family: sans-serif;
  animation: pulse 1.5s infinite ease-in-out;
}

@keyframes rotate {
  100% { transform: rotate(360deg); }
}

@keyframes bloom {
  0% { transform: scale(0.8); opacity: 0.7; }
  100% { transform: scale(1.1); opacity: 1; }
}

@keyframes pulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}
</style>
