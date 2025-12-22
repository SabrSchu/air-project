<script setup lang="ts">
import {computed} from 'vue'

const props = defineProps({
  value: {
    type: Number,
    required: true
  }
})

const clamped = computed(() => Math.min(Math.max(props.value, 0), 1))
const percent = computed(() => Math.round(clamped.value * 100))
</script>

<template>
  <section class="match-bar">
    <header>
      <h4>Match Percentage</h4>
      <span>{{ percent }}%</span>
    </header>
    <div class="bar-track">
      <div class="bar-fill" :style="{ width: `${percent}%` }" />
    </div>
    <p class="caption">
      Your score is better than {{ percent }}% of the dataset.
    </p>
  </section>
</template>

<style scoped>
.match-bar {
  width: 12rem;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

header {
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.bar-track {
  width: 100%;
  height: 0.75rem;
  border-radius: 100rem;
  background: #f4f4f4;
  overflow: hidden;
  border: 0.1rem solid #dfdfdf;
}

.bar-fill {
  height: 100%;
  background: repeating-linear-gradient(
      -45deg,
      rgba(183, 213, 172, 0.5),
      rgba(183, 213, 172, 0.5) 0.5rem,
      #b7d5ac 0.5rem,
      #b7d5ac 1rem
  );
  border-radius: 100rem 0 0 100rem;
  transition: width 0.2s ease;
}

.caption {
  margin: 0;
  font-size: 0.8rem;
  color: #4b5563;
}
</style>
