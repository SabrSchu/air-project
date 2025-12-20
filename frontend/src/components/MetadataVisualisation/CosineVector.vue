<!-- CosineDistanceVector.vue -->
<script setup lang="ts">
import {computed} from 'vue'

const props = defineProps({
  distance: {
    type: Number,
    required: true
  },
  maxAngle: {
    type: Number,
    default: 90
  },
  minAngle: {
    type: Number,
    default: 0
  }
})

const clamped = computed(() => Math.max(0, Math.min(props.distance, 1)))
const angle = computed(() => props.minAngle + (props.maxAngle - props.minAngle) * clamped.value)
</script>

<template>
  <section class="distance-angle">
    <div class="angle-canvas">
      <div class="arm fixed" :style="{transform: `rotate(${90}deg)` }" />
      <div class="arm moving" :style="{transform: `rotate(${90 - angle}deg)` }" />
    </div>

    <div class="angle-text">
      <p class="title">Cosine Distance</p>
      <p class="value">{{ distance.toFixed(3) }}</p>
      <p class="note">Smaller value = better match.</p>
    </div>
  </section>
</template>

<style scoped>
.distance-angle {
  display: flex;
  align-items: center;
  gap: 2rem;
  width: fit-content;
}

.angle-canvas {
  position: relative;
  width: 3.25rem;
  height: 3.25rem;
}

.arm {
  position: absolute;
  bottom: 0.3rem;
  left: 50%;
  width: 0.18rem;
  height: 2.75rem;
  background: #2f4858;
  transform-origin: bottom center;
  border-radius: 1rem;
}

.arm.moving {
  background: #b7d5ac;
}

.angle-text {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.title {
  margin: 0;
  font-weight: 600;
}

.value {
  margin: 0;
  font-weight: 700;
}

.note {
  margin: 0;
  font-size: 0.75rem;
  color: #4b5563;
  text-wrap: nowrap;
}
</style>
