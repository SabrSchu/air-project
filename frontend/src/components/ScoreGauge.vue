<!-- ScoreGauge.vue -->
<script setup lang="ts">
import { Doughnut } from 'vue-chartjs'
import { Chart, ArcElement, Tooltip } from 'chart.js'
Chart.register(ArcElement, Tooltip)

const props = defineProps<{ value: number; label: string }>()
const data = {
  labels: [props.label, 'Rest'],
  datasets: [
    {
      data: [props.value, 1 - props.value],
      backgroundColor: ['#b7d5ac', '#ececec'],
      borderWidth: 0
    }
  ]
}
const options = {
  cutout: '70%',
  plugins: { tooltip: { enabled: false } }
}
</script>

<template>
  <div v-if="props.label == 'Normalized'" class="metric-column">
    <h2>Normalized</h2>
    <div class="gauge-wrapper">
      <Doughnut :data="data" :options="options" />
      <span class="gauge-value">{{ (value * 100).toFixed(0) }}</span>
    </div>
  </div>

  <div v-else class="metric-column">
    <h2>Match Percentage</h2>
    <div class="gauge-wrapper">
      <Doughnut :data="data" :options="options" />
      <span class="gauge-value">{{ (value * 100).toFixed(0) }}%</span>
    </div>
  </div>
</template>

<style scoped>
.metric-column {
  display: flex;
  flex-direction: column;
  text-align: center;
  justify-content: center;
  align-items: center;

  h2 {
    font-size: 1.2rem;
    font-weight: bold;
    text-wrap: nowrap;
  }
}

.gauge-wrapper {
  position: relative;
  width: 8rem;
  height: 8rem;
}
.gauge-value {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  font-weight: 600;
  font-size: 1.2rem;
}
</style>
