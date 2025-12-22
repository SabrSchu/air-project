<script setup lang="ts">
import InformationOutline from 'vue-material-design-icons/InformationOutline.vue'

const props = defineProps({
  metadata: {
    type: Object,
    required: true
  },
});

const RANK_TOOLTIP =
    "Position of the plant compared to all others. 1 means best match."

const RAW_SIMILARITY_TOOLTIP =
    "Un-scaled cosine similarity between your answers and this plant's profile. Higher is better."

const NORMALIZED_SIMILARITY_TOOLTIP =
    "Cosine similarity rescaled between 0 and 1 so you can compare plants at a glance. Closer to 1 means stronger match."

const COSINE_DISTANCE_TOOLTIP =
    "How far this plant's profile is from your ideal vector. Smaller value = better match."

const GAP_TO_BEST_TOOLTIP =
    "Difference between this plant an the top-ranked option. Zero means it's tied for best."
</script>

<template>
  <div class="metrics-card">
    <h3>Recommendation-Score</h3>

    <div class="metric-row">
      <span class="tooltip-trigger" tabindex="0">
        <InformationOutline :size="16" />
        <span class="tooltip" role="tooltip">
          {{ RANK_TOOLTIP }}
        </span>
      </span>
      <span class="label">Rank:</span>
      <span class="value">{{ metadata.rank }}</span>
    </div>

    <div class="metric-row">
      <span class="tooltip-trigger" tabindex="0">
        <InformationOutline :size="16" />
        <span class="tooltip" role="tooltip">
          {{ RAW_SIMILARITY_TOOLTIP }}
        </span>
      </span>
      <span class="label">Raw Similarity:</span>
      <span class="value">{{ metadata.cosine_sim_raw }}</span>
    </div>

    <div class="metric-row">
      <span class="tooltip-trigger" tabindex="0">
        <InformationOutline :size="16" />
        <span class="tooltip" role="tooltip">
          {{ NORMALIZED_SIMILARITY_TOOLTIP }}
        </span>
      </span>
      <span class="label">Normalized Similarity:</span>
      <span class="value">{{ (metadata.cosine_sim_normalized).toFixed(2) }}</span>
    </div>

    <div class="metric-row">
      <span class="tooltip-trigger" tabindex="0">
        <InformationOutline :size="16" />
        <span class="tooltip" role="tooltip">
          {{ COSINE_DISTANCE_TOOLTIP }}
        </span>
      </span>
      <span class="label">Cosine Distance:</span>
      <span class="value">{{ (metadata.cosine_distance).toFixed(4) }}</span>
    </div>

    <div class="metric-row">
      <span class="tooltip-trigger" tabindex="0">
        <InformationOutline :size="16" />
        <span class="tooltip" role="tooltip">
          {{ GAP_TO_BEST_TOOLTIP }}
        </span>
      </span>
      <span class="label">Gap to best:</span>
      <span class="value">{{ (metadata.gap_to_best).toFixed(4) }}</span>
    </div>
  </div>
</template>

<style scoped>
.metrics-card {
  background: rgba(229, 229, 229, 0.5);
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 0.25rem 0.5rem rgba(0,0,0,0.1);
  width: fit-content;
  text-wrap: nowrap;
  font-size: 0.9rem;
}

.metric-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  text-align: right;
}

.label {
  flex: 0 0 10rem;
  font-weight: 500;
  color: #2c3e50;
  text-align: left;
  text-wrap: nowrap;
}

.value {
  flex: 0 0 1rem;
  text-align: right;
  font-weight: bold;
  color: #2c3e50;
}

.tooltip-trigger {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: fit-content;
  height: 1.25rem;
  border-radius: 50%;
  cursor: pointer;
}

.tooltip {
  position: absolute;
  bottom: calc(100% + 0.35rem);
  left: 50%;
  transform: translateX(-50%);
  width: fit-content;
  padding: 0.5rem;
  border-radius: 0.5rem;
  background: #1f2937;
  color: #ffffff;
  font-size: 0.75rem;
  line-height: 1.2;
  text-align: center;
  box-shadow: 0 0.25rem 0.75rem rgba(0,0,0,0.2);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.15s ease, transform 0.15s ease;
  z-index: 20;
}

.tooltip-trigger:hover .tooltip,
.tooltip-trigger:focus-visible .tooltip {
  opacity: 1;
  transform: translate(-50%, -0.1rem);
}
</style>
