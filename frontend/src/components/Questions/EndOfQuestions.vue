<script setup lang="ts">
const emit = defineEmits(['reset-questionnaire']);

const handleReset = () => {
  emit('reset-questionnaire');
};
</script>

<template>
  <div class="question-container">
    <h3>This is the end of our recommender!</h3>
    <h3>Thank you very much for finding your perfect plant!</h3>
    <h3>Below this window you can find your recommendations grouped into three groups, which represent the match between your answers and all available plants.</h3>
    <h3>Happy Planting!</h3>

    <button class="reset-btn" @click="handleReset">
      Click here for another recommendation
    </button>
  </div>
</template>

<style scoped>
.question-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
}

.question-container h3{
  padding: 0.5rem;
}

.reset-btn {
  background-color: #6a9a5f;
  color: white;
  border: none;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: bold;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(106, 154, 95, 0.3);
}

.reset-btn:hover {
  background-color: #b7d5ac;
  color: #2c3e50;
}
</style>
