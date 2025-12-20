<script setup lang="ts">

const props = defineProps({
  metadata: {
    type: Object,
    required: true
  },
});
</script>

<template>
  <div class="metrics-card">
    <h3>Recommendation-Score</h3>

    <div class="metric-row">
      <span class="label">Raw Similarity:</span>
      <div class="bar-container">
        <div class="bar" :style="{ width: metadata.cosine_sim_raw * 100 + '%'}"></div>
      </div>
      <span class="value">{{ metadata.cosine_sim_raw }}</span>
    </div>

    <div class="metric-row">
      <span class="label">Normalized:</span>
      <div class="bar-container">
        <div class="bar" :style="{ width: metadata.cosine_sim_normalized}"></div>
      </div>
      <span class="value">{{ (metadata.cosine_sim_normalized).toFixed(2) }}</span>
    </div>

    <div class="metric-row">
      <span class="label">Match Percentage:</span>
      <div class="bar-container">
        <div class="bar" :style="{ width: metadata.cosine_sim_percentile * 100 + '%'}"></div>
      </div>
      <span class="value">{{ (metadata.cosine_sim_percentile * 100).toFixed(0) }}%</span>
    </div>

    <div class="metric-row">
      <span class="label">Gap to best:</span>
      <span class="value">{{ (metadata.gap_to_best).toFixed(4) }}</span>
    </div>
  </div>
</template>

<style scoped>
.metrics-card {
  background: rgba(229, 229, 229, 0.5);
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 0.25rem 0.5rem rgba(0,0,0,0.1);
  width: fit-content;
}

.metric-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.label {
  flex: 0 0 10rem;
  font-weight: 500;
  color: #2c3e50;
  text-align: left;
  text-wrap: nowrap;
}

.bar-container {
  flex: 1;
  height: 1.5rem;
  background: #ecf0f1;
  border-radius: 2rem;
  overflow: hidden;
}

.bar {
  height: 100%;
  transition: width 0.3s ease;
}

.value {
  flex: 0 0 4rem;
  text-align: right;
  font-weight: bold;
  color: #2c3e50;
}
</style>
