<script setup lang="ts">
import {computed, onMounted, ref} from 'vue'
import {Motion} from 'motion-v'
import Question from './Question.vue'
import PlantCard from "@/components/PlantCard.vue";
import EndOfQuestions from "./EndOfQuestions.vue";
import FreeTextQuestion from "@/components/Questions/FreeTextQuestion.vue";
import LoadingAnimation from "@/components/LoadingAnimation.vue";
import ScoreGauge from "@/components/MetadataVisualisation/ScoreGauge.vue";
import MetadataVisulizerTest from "@/components/MetadataVisualisation/MetadataVisulizerTest.vue";
import MatchPercentageBar from "@/components/MetadataVisualisation/MatchPercentageBar.vue";
import CosineVector from "@/components/MetadataVisualisation/CosineVector.vue";
import ArrowLeft from 'vue-material-design-icons/ArrowLeft.vue'

import {
  accessQuestionsEndpoint,
  postFreeText,
  postQuestionnaire
} from "@/services/questionsEnpointService.ts";

const isLoading = ref(true)
const questions = ref([])
const quizStarted = ref(false)
const quizFinished = ref(false)
const currentStep = ref(0)
const answers = ref([])

const isFreeTextMode = ref(false)
const userInput = ref("");

const finalResults = ref(null)
const recommendations = ref([])

const animationKey = computed(() => {
  if (quizFinished.value) return 'end-screen';
  return isFreeTextMode.value ? 'submitFreeTextQuestion' : currentStep.value;
});

/**
 * Function that calls the services which call our Backend endpoints
 */
async function fetchData() {
  try {
    questions.value = await accessQuestionsEndpoint()
  } catch (err) {
    console.error("Error:", err)
    questions.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchData()
})

const currentQuestionData = computed(() => questions.value[currentStep.value])

const currentComponent = computed(() => {
  if (quizFinished.value) {
    return EndOfQuestions;
  }
  if (isFreeTextMode.value) {
    return FreeTextQuestion;
  }
  return Question;
});

const currentProps = computed(() => {
  if (quizFinished.value) {
    return { results: finalResults.value };
  }
  return { questionData: currentQuestionData.value };
});

const startQuestionnaire = () => {
  quizStarted.value = true
}

const handleNext = (payload: any) => {
  const existingAnswerIndex = answers.value.findIndex(
      (ans) => ans.question_id === payload.question_id
  );
  if (existingAnswerIndex !== -1) {
    answers.value[existingAnswerIndex] = payload;
  }
  else {
    answers.value.push(payload);
  }

  if (currentStep.value < questions.value.length - 1) {
    currentStep.value++
  } else {
    quizFinished.value = true
    finalResults.value = {
      answers: answers.value,
      created_at: new Date().toISOString(),
      free_text: ""
    }
    console.log('Final Answers:', JSON.stringify(finalResults.value, null, 2))
    sendResults();
  }
}

const handlePrevious = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const sendResults = async () => {
  if (!finalResults.value) return;

  console.log("Sending questionnaire...");
  try {
    const result = await postQuestionnaire(finalResults.value, {
      num_perfect_fits: 3,
      num_good_fits: 2,
      num_bad_fits: 1
    });
    recommendations.value = result;
    console.log("Received recommendations:", JSON.stringify(recommendations.value, null, 2));
  } catch (error) {
    console.error("Failed to send results or get recommendations:", error);
  }
}

const handleSendFreeText = async (payload: string) => {
  userInput.value = payload;

  if (!userInput.value.trim()) return;

  quizFinished.value = true;

  finalResults.value = {
    created_at: new Date().toISOString(),
    free_text: userInput.value,
    answers: []
  }

  console.log("Send text:", JSON.stringify(finalResults.value, null, 2));
  isLoading.value = true;

  try {
    const result = await postFreeText(finalResults.value, {
      num_perfect_fits: 3,
      num_good_fits: 2,
      num_bad_fits: 1
    });

    recommendations.value = result;
    console.log("Receive recommendations:", JSON.stringify(recommendations.value, null, 2));

    userInput.value = "";

  } catch (error) {
    console.error("Error while sending:", error);
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <div class="questionnaire-wrapper">
    <Motion
        is="div"
        :initial="{ opacity: 0 }"
        :animate="{ opacity: 1 }"
        :transition="{ duration: 0.7 }"
        class="questionnaire-main-container">

      <!-- Start Screen -->
      <template v-if="!quizStarted">
        <h1>Discover our plant recommender!</h1>
        <p>This tool is made for you. Feel free to use it, to find the perfect companion for you and your flat.</p>

        <div class="mode-toggle-container">
          <button
              :class="['toggle-btn', { active: !isFreeTextMode }]"
              @click="isFreeTextMode = false">
            Guided Quiz
          </button>
          <button
              :class="['toggle-btn', { active: isFreeTextMode }]"
              @click="isFreeTextMode = true">
            Free Text
          </button>
        </div>

        <Motion
            class="questionnaire-start-button"
            is="button"
            :whileHover="{ scale: 1.1 }"
            :whilePress="{ scale: 0.95 }"
            :transition="{ duration: 0.2 }"
            @click="startQuestionnaire"
        >
          {{ isFreeTextMode ? 'Ask your question' : 'Find your perfect plant' }}
        </Motion>
      </template>

      <!-- Questions & Endscreen -->
      <template v-else>
        <Motion
            class="questionnaire-each-question"
            :key="animationKey"
            :initial="{ opacity: 0, x: 50 }"
            :animate="{ opacity: 1, x: 0 }"
            :exit="{ opacity: 0, x: -50 }"
            :transition="{ duration: 0.3 }"
        >
          <component
              v-if="!isLoading"
              :is="currentComponent"
              v-bind="currentProps"
              @next="isFreeTextMode ? handleSendFreeText($event) : handleNext($event)"
          />
          <component
            v-if="isLoading"
            :is="LoadingAnimation"
          />
        </Motion>

        <div class="questionnaire-navigation" v-if="!quizFinished && !isLoading && !isFreeTextMode && questions.length > 0">
          <ArrowLeft
              class="arrow-left-button"
              v-if="currentStep > 0"
              @click="handlePrevious"/>
          <span>Question {{ currentStep + 1 }} of {{ questions.length }}</span>
        </div>
      </template>
    </Motion>

    <div v-if="quizFinished && recommendations.length > 0" class="recommendations-container">
      <h1>Your Plant Recommendations</h1>

      <template class="recommender-group-container" v-for="group in recommendations.values()">
        <h2>{{ group.label }}</h2>
        <div v-for="plant in group.recommendation">
          <PlantCard
              v-if="plant.metadata.algorithm != 'BM25'"
              :key="plant.id"
              :id="plant.id"
              :name="plant.name"
              :description="plant.description"
              :waterAmount="plant.watering"
              :sunlightAmount="plant.sunlight"
              :fertilizerAmount="plant.fertilization"
              :image_url="plant.image_url"
              :metadata="plant.metadata"
          >
            <template #metadata="{ metadata }">
              <section class="metadata-grid">
                <MetadataVisulizerTest :metadata="metadata" />
                <ScoreGauge label="Normalized" :value="metadata.cosine_sim_normalized" />
                <div class="match-and-cosine-div">
                  <MatchPercentageBar :value="metadata.cosine_sim_percentile" />
                  <CosineVector :distance="metadata.cosine_distance" />
                </div>
              </section>
            </template>
          </PlantCard>

          <PlantCard
              v-else
              :id="plant.id"
              :name="plant.name"
              :description="plant.description"
              :waterAmount="plant.watering"
              :sunlightAmount="plant.sunlight"
              :fertilizerAmount="plant.fertilization"
              :image_url="plant.image_url"
          />
        </div>
      </template>

      <RouterLink to="/feedback">
        <Motion
            class="feedback-button"
            is="button"
            :whileHover="{ scale: 1.1 }"
            :whilePress="{ scale: 0.95 }"
            :transition="{ duration: 0.2 }"
        >
          <h1>Please give us Feedback!</h1>
        </Motion>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.questionnaire-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;

  background-image: url("public/background.jpeg");
  background-color: rgba(255,255,255,0.3);
  background-blend-mode: lighten;
  background-size: cover;
  background-position: center;
  z-index: 0;
}

.questionnaire-main-container {
  position: relative;
  width: 60%;
  max-width: 50rem;
  margin: 1rem;
  padding: 1rem;
  border-radius: 1.5rem;
  min-height: 30rem;
  height: auto;
  gap: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 0.5rem 1rem 0 rgba(0,0,0,0.3);
  transition: transform 0.2s ease;
  background-color: rgba(255,255,255,1);
}
.questionnaire-main-container h1 {
  width: calc(100% + 2rem);
  padding-top: 1em;
  padding-bottom: 1em;
  margin: -1rem -1rem 0 -1rem;
  text-align: center;
  font-size: 1.75rem;
  background-color: #b7d5ac;
  border-top-left-radius: 1.5rem;
  border-top-right-radius: 1.5rem;
}
.questionnaire-main-container p {
  width: 80%;
  font-size: 1.5rem;
  margin: 0;
  text-align: center;
}

.questionnaire-each-question {
  width: 100%;
  height: 100%;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.questionnaire-start-button {
  width: 40%;
  margin-bottom: 1rem;
  min-height: 3rem;
  height: auto;
  padding: 0.5rem 1rem;
  position: relative;
  cursor: pointer;
  align-content: center;
  text-align: center;
  font-size: 1.2rem;
  background-color: #b7d5ac;
  border-radius: 1rem;
  border: none;
  box-shadow: 0 0.25rem 0.5rem 0 rgba(0,0,0,0.3);
}

.questionnaire-navigation {
  position: absolute;
  bottom: 2rem;
  display: flex;
  gap: 1rem;
  flex-direction: row;
}

.arrow-left-button {
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  transition: transform 0.2s ease;
}

.arrow-left-button:hover {
  transform: scale(1.2);
}

.recommendations-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.recommendations-container h1 {
  width: 100%;
  text-align: center;
  margin-bottom: 1rem;
}

.recommendations-container h2 {
  width: 100%;
  text-align: center;
  margin-bottom: 1rem;
}

.recommender-group-container {
  border: solid 1rem black;
  border-radius: 0.5rem;
}

.separator {
  width: 100%;
  border: none;
  border-top: 0.1rem solid #000000;
  margin: 2rem 0;
}

.mode-toggle-container {
  display: flex;
  gap: 1rem;
  background: #f0f0f0;
  padding: 0.5rem;
  border-radius: 2rem;
  margin-top: auto;
  margin-bottom: auto;
}

.toggle-btn {
  padding: 1rem 2rem;
  border: none;
  border-radius: 1.5rem;
  cursor: pointer;
  background: transparent;
  font-size: 1rem;
  transition: all 0.3s ease;
  color: #666;
}

.toggle-btn.active {
  background-color: #b7d5ac;
  color: black;
  font-weight: bold;
  box-shadow: 0 0.2rem 0.4rem rgba(0, 0, 0, 0.1);
}

.feedback-button{
  margin-top: 1rem;
  background-color: #b7d5ac;
  border: none;
  padding: 1rem;
  border-radius: 1rem;
  cursor: pointer;

  h1 {
    font-size: 1rem;
  }
}

.metadata-grid {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  background: #ffffff;
  padding: 0.5rem;
  border-radius: 0.5rem;
}

.match-and-cosine-div {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  justify-content: center;
}
</style>
