<template>
  <div class="recommendations-overview-container">
    <h1>All your Recommendations</h1>

    <div v-if="allRecommendations.length === 0">
      <p>You dont have any recommendations yet.</p>
      <p>Please try out our Plant Recommender first before giving feedback.</p>
    </div>

    <div v-else>
      <p>Please check your recommendations while giving feedback.</p>
      <div v-for="recommendationSet in allRecommendations"
           :key="recommendationSet.submission_id"
           class="recommendation-card">
        <div class="card-header"
             @click="toggleExpand(recommendationSet.submission_id)">
          <span>
            Recommendation Nr. #{{ recommendationSet.submission_id }}
            <small>
              ({{ recommendationSet.user_input.type === 'free_text' ? 'Free Text' : 'Guided Quiz' }})
            </small>
          </span>
          <span v-if="recommendationSet.rating">
            Rating: {{ recommendationSet.rating }}/5
            <LeafIcon :size="13" />
          </span>
          <component :is="expandedRecommendations[recommendationSet.submission_id] ? ChevronUp : ChevronDown"/>
        </div>

        <div v-show="expandedRecommendations[recommendationSet.submission_id]">
          <div class="user-input-summary">
            <strong>Your Request:</strong>
            <p v-if="recommendationSet.user_input.type === 'free_text'" class="free-text">
              "{{ recommendationSet.user_input.free_text }}"
            </p>
            <ul v-else class="questionnaire-summary">
              <li v-for="(q, index) in recommendationSet.user_input.questionnaire" :key="index">
                <small>{{ q.question }}:</small> <span>{{ q.answer }}</span>
              </li>
            </ul>
          </div>

          <div class="plants-grid">
            <template v-for="(recGroup, index) in recommendationSet.recommendations_per_submission" :key="recGroup.recommendation[0].id">

              <h1 v-if="index === 0 || recGroup.label !== recommendationSet.recommendations_per_submission[index - 1].label"
                  class="group-label"
                  :class="recGroup.label">
                {{ formatLabel(recGroup.label) }}
              </h1>

              <PlantCard
                  :id="recGroup.recommendation[0].id"
                  :name="recGroup.recommendation[0].name"
                  :description="recGroup.recommendation[0].description"
                  :waterAmount="recGroup.recommendation[0].watering"
                  :sunlightAmount="recGroup.recommendation[0].sunlight"
                  :fertilizerAmount="recGroup.recommendation[0].fertilization"
                  :image_url="recGroup.recommendation[0].image_url"
                  :can_be_liked="false"
              />
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {onMounted, ref} from "vue";
import ChevronDown from "vue-material-design-icons/ChevronDown.vue";
import ChevronUp from "vue-material-design-icons/ChevronUp.vue";
import LeafIcon from 'vue-material-design-icons/Leaf.vue'

import {getAllRecommendationsEndpoint} from "@/services/recommendationsEndpointService.ts";
import ScoreGauge from "@/components/MetadataVisualisation/ScoreGauge.vue";
import MatchPercentageBar from "@/components/MetadataVisualisation/MatchPercentageBar.vue";
import PlantCard from "@/components/PlantCard.vue";
import CosineVector from "@/components/MetadataVisualisation/CosineVector.vue";
import MetadataVisulizerTest from "@/components/MetadataVisualisation/MetadataVisulizerTest.vue";

const allRecommendations = ref([]);
const expandedRecommendations = ref<Record<number, boolean>>({});

const toggleExpand = (id: number) => {
  expandedRecommendations.value[id] = !expandedRecommendations.value[id];
};

const fetchAllRecommendations = async () => {
  try {
    allRecommendations.value = await getAllRecommendationsEndpoint(true);
  } catch (err) {
    console.error("Error fetching all recommendations:", err);
  }
}

const formatLabel = (label: string) => {
  const map: Record<string, string> = {
    'perfect': 'Perfect Match',
    'good': 'Good Match',
    'mismatch': 'Mismatch'
  };
  return map[label.toLowerCase()] || label;
};

onMounted(() => {
  fetchAllRecommendations();
})
</script>

<style scoped>
.recommendations-overview-container {
  flex: 1;
  max-width: 40%;
  height: 67vh;
  overflow-y: auto;
  padding: 1.5rem;
  border-radius: 1rem;
  background-color: rgba(255, 255, 255, 0.9);
  text-align: center;

  h1 {
    margin-bottom: 1rem;
    color: #4a6a41;
    font-size: 1.5rem;
  }

  .recommendation-card {
    background: white;
    border: 0.1rem solid #e0e0e0;
    border-radius: 0.8rem;
    padding: 1rem;
    margin-bottom: 1rem;
    text-align: left;

    .card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.8rem;
      color: #666;
      cursor: pointer;
    }

    .user-input-summary {
      font-size: 0.9rem;
      margin-bottom: 1rem;
      background: #f9f9f9;
      padding: 0.5rem;
      border-radius: 0.4rem;

      .free-text {
        font-style: italic;
        color: #555;
      }

      .questionnaire-summary {
        list-style: none;
        padding: 0;
        font-size: 0.8rem;
      }
    }

    .plants-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      justify-content: center;
      background: #f9f9f9;
      border-radius: 0.4rem;
      padding-bottom: 0.5rem;

      .group-label {
        width: 100%;
        font-size: 0.9rem;
        letter-spacing: 0.05rem;
        text-align: center;

        &.perfect {
          color: #2e7d32;
        }

        &.good {
          color: #ef6c00;
        }

        &.mismatch {
          color: #c62828;
        }
      }

      .metadata-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        padding: 1rem;
        background: #f9f9f9;
        border-radius: 0.5rem;
        margin-top: 0.5rem;
      }

      .match-and-cosine-div {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        justify-content: center;
      }
    }
  }
}
</style>