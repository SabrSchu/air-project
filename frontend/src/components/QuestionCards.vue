<script setup lang="ts">
import { Motion } from 'motion-v'
</script>

<template>
  <div class="question-wrapper">
    <Motion
        is="div"
        :initial="{ opacity: 0 }"
        :animate="{ opacity: 1 }"
        :transition="{ duration: 1.8 }"
        class="question-main-container">
      <h2>Discover our plant recommender!</h2>

      <p>This tool is made for you. Feel free to use it, to find the perfect companion for you and your flat.</p>

      <Motion
          class="question-start-button"
          is="button"
          :whileHover="{ scale: 1.1 }"
          :whilePress="{ scale: 0.95 }"
          :transition="{ duration: 0.2 }"
      >
        Find your perfect plant
      </Motion>
    </Motion>
  </div>
</template>

<style scoped>
.question-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.question-main-container {
  position: relative;
  width: 60%;
  height: 25rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 1rem;
  box-shadow: 0 0.5rem 1rem 0 rgba(0,0,0,0.3);
}
.question-main-container h2 {
  width: 100%;
  text-align: center;
  background-color: #b7d5ac;
}
.question-main-container p {
  width: 80%;
}

.question-start-button {
  width: 30%;
  height: 3rem;
  position: absolute;
  bottom: 2rem;
  cursor: pointer;
  align-content: center;
  text-align: center;
  background-color: #b7d5ac;
  border-radius: 1rem;
  border: none;
  box-shadow: 0 0.25rem 0.5rem 0 rgba(0,0,0,0.3);
}
</style>
