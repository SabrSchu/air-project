<template>
  <div class="feedback-wrapper">
    <!-- Page Title --->
    <motion.div class="title"
                :initial="{ scale: 0 }"
                :animate="{ scale: 1, transition: { duration: 0.6 } }"
    >
      <h1>Feedback</h1>
      <TreeIcon/>
    </motion.div>

    <!-- Feedback Content --->
    <div class="feedback-background">
      <div class="feedback-container">
        <template v-if="!studySubmitted">
          <h1>Feedback Questionnaire</h1>
          <p>Please help us improve our Plant Recommender by giving us feedback.</p>

          <div class="study-questions-list">
            <div
                v-for="section in userStudySections"
                :key="section.section_id"
                class="study-section"
            >
              <h3>{{ section.title }}</h3>
              <span v-if="section.sub_title" class="study-subtitle">{{ section.sub_title }}</span>

              <div
                  v-for="item in section.items"
                  :key="item.item_id"
                  class="study-item"
              >
                <p class="question-text">{{ item.question }}</p>

                <div v-if="item.type === 'scale_1_5'" class="feedback-icons-container">
                  <LeafIcon
                      v-for="n in 5"
                      :key="n"
                      :size="30"
                      class="plant-icon"
                      :class="{ 'filled': n <= (hoverState[getAnswerKey(section.section_id, item.item_id)] || userStudyAnswers[getAnswerKey(section.section_id, item.item_id)] || 0) }"
                      @click="userStudyAnswers[getAnswerKey(section.section_id, item.item_id)] = n"
                      @mouseenter="hoverState[getAnswerKey(section.section_id, item.item_id)] = n"
                      @mouseleave="hoverState[getAnswerKey(section.section_id, item.item_id)] = 0"
                  />
                </div>

                <div v-else-if="item.type === 'free_text'" class="text-input-container">
              <textarea
                  v-model="userStudyAnswers[getAnswerKey(section.section_id, item.item_id)]"
                  placeholder="Your feedback..."
                  rows="2"
              ></textarea>
                </div>
              </div>
              <div class="separator"></div>
            </div>
          </div>

          <button
              class="submit-feedback-btn"
              :disabled="!isFormComplete"
              :class="{ 'disabled-btn': !isFormComplete }"
              @click="submitFeedback">
            Submit Feedback
          </button>
        </template>

        <template v-else>
          <div>
            <h2>Thank you!</h2>
            <p>We appreciate your feedback.</p>
          </div>
        </template>
      </div>

      <RecommendationsOverview/>
    </div>
  </div>
</template>

<script setup lang="ts">
import { motion } from 'motion-v'
import RecommendationsOverview from "@/components/RecommendationsOverview.vue";
import { onMounted, ref, computed } from "vue";
import { getUserStudyQuestions, submitUserStudy } from "@/services/questionsEndpointService.ts";
import TreeIcon from "vue-material-design-icons/Tree.vue";
import LeafIcon from "vue-material-design-icons/Leaf.vue";

const userStudySections = ref([]);
const userStudyAnswers = ref<Record<string, any>>({});
const studySubmitted = ref(false);
const hoverState = ref<Record<string, number>>({});

const getAnswerKey = (sectionId: number, itemId: number) => `${sectionId}_${itemId}`;

async function fetchUserStudyQuestions() {
  try {
    const response = await getUserStudyQuestions();
    userStudySections.value = response.user_study_questions || [];
  } catch (err) {
    console.error("Error fetching study questions:", err)
    userStudySections.value = []
  }
}

const allRequiredKeys = computed(() => {
  const keys: string[] = [];
  userStudySections.value.forEach((section: any) => {
    section.items.forEach((item: any) => {
      keys.push(getAnswerKey(section.section_id, item.item_id));
    });
  });
  return keys;
});

const isFormComplete = computed(() => {
  if (allRequiredKeys.value.length === 0) return false;

  return allRequiredKeys.value.every(key => {
    const value = userStudyAnswers.value[key];

    if (value === undefined || value === null) return false;

    if (typeof value === 'string' && value.trim() === '') return false;

    return true;
  });
});

const submitFeedback = async () => {
  if (Object.keys(userStudyAnswers.value).length === 0) {
    console.warn("Cannot submit empty study");
    return;
  }

  const createdAt = new Date().toISOString();
  const userName = "User_" + Math.random().toString(36).substring(2, 9);

  const formattedAnswers = Object.entries(userStudyAnswers.value).map(([key, val]) => {
    const [sectionId, itemId] = key.split('_');

    if (sectionId === undefined || itemId === undefined) {
      return null;
    }

    const maybeInt = parseInt(val);

    if (isNaN(maybeInt)) {
      return {
        section_id: parseInt(sectionId),
        item_id: parseInt(itemId),
        free_text: val,
        rating: null
      };
    } else {
      return {
        section_id: parseInt(sectionId),
        item_id: parseInt(itemId),
        rating: maybeInt,
        free_text: null
      };
    }
  }).filter(Boolean);

  const payload = {
    user_name: userName,
    created_at: createdAt,
    user_study_answers: formattedAnswers
  };

  try {
    await submitUserStudy(payload);
    studySubmitted.value = true;
  } catch (error) {
    console.error("Error submitting study:", error);
  }
}

onMounted(() => {
  fetchUserStudyQuestions();
})

</script>

<style scoped>
.feedback-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
  min-height: 100%;

  .title {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.5rem;
    width: 100%;
    background-color: white;
  }

  .feedback-background{
    display: flex;
    flex: 1;
    gap: 1rem;
    align-content: center;
    justify-content: center;
    width: 100%;
    padding: 1rem;
    background-image: url("/background.jpeg");
    background-color: rgba(255,255,255,0.3);
    background-blend-mode: lighten;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;

    .feedback-container {
      flex: 1;
      max-width: 35%;
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

      .feedback-icons-container {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        margin: 1.5rem 0;

        .plant-icon {
          cursor: pointer;
          color: #d3d3d3;
          transition: color 0.2s ease, transform 0.1s ease;

          &:hover {
            transform: scale(1.2);
          }

          &.filled {
            color: #6a9a5f;
          }
        }
      }

      .text-input-container textarea {
        padding: 1rem;
        border-radius: 0.5rem;
        border: none;
        max-width: 90%;
      }

      .submit-feedback-btn {
        padding: 1rem;
        background-color: #9bc28e;
        border: none;
        border-radius: 0.5rem;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.2s;

        &.disabled-btn {
          background-color: #cccccc;
          cursor: not-allowed;
          opacity: 0.7;
        }

        &:hover:not(.disabled-btn) {
          background-color: #6a9a5f;
        }
      }
    }
  }
}
</style>