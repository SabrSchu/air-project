<script setup lang="ts">
defineProps({
  questionData: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['next'])

const selectAnswer = (option: string) => {
  emit('next', option)
}
</script>

<template>
  <div class="question-main-container">
    <h3>{{ questionData.question }}</h3>
    <div class="answers">
      <button
          v-for="option in questionData.answer_option"
          :key="option"
          @click="selectAnswer(option)">
        {{ option.answer }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.question-main-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  align-items: center;
  padding: 1rem;
  overflow: hidden;
  height: 100%;
}

.answers {
  justify-content: space-between;
  align-content: flex-start;
  width: 80%;
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

button {
  background: white;
  padding: 0.5rem 2rem;
  cursor: pointer;
  border-radius: 0.4rem;
  border: none;
  box-shadow: 0 0.5rem 1rem 0 rgba(0,0,0,0.2);
  transition: transform 0.2s ease;
}
button:hover {
  cursor: pointer;
  transform: scale(1.1);
  background: #fafafa;
}
</style>
