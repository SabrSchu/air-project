<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits(['next'])
const inputText = ref('')

const submitText = () => {
  emit('next', inputText.value)
}
</script>

<template>
  <div class="free-text-container">
    <h3 style="font-size: 1.5rem">Please describe what you are looking for</h3>
    <textarea
        v-model="inputText"
        placeholder="Write something like: A plant that needs indirect sunlight, watering weekly and no fertilizer."
        rows="5"
    ></textarea>
    <button style="font-size: 1.2rem" @click="submitText">Submit your Text</button>
  </div>
</template>

<style scoped>
.free-text-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
  padding: 1rem;
  width: 100%;
}

textarea {
  width: 80%;
  height: 10em;
  padding: 0.5rem;
  border-radius: 0.4rem;
  border: 1px solid #ccc;
  font-size: 1.2rem;
}

button {
  background: #b7d5ac;
  padding: 0.5rem 2rem;
  cursor: pointer;
  border-radius: 0.4rem;
  border: none;
  box-shadow: 0 0.5rem 1rem 0 rgba(0,0,0,0.2);
  transition: transform 0.2s ease;
}
button:hover {
  transform: scale(1.05);
}
</style>
