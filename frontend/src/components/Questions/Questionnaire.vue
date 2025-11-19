<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Motion } from 'motion-v'
import Question from './Question.vue'
import PlantCard from "@/components/PlantCard.vue";
import FreeTextQuestion from "./FreeTextQuestion.vue";
import EndOfQuestions from "./EndOfQuestions.vue";
import ArrowLeft from 'vue-material-design-icons/ArrowLeft.vue'

import {accessQuestionsEndpoint, postQuestionnaire} from "@/services/questionsEnpointService.ts";

const isLoading = ref(true)
const questions = ref([])
const quizStarted = ref(false)
const quizFinished = ref(false)
const currentStep = ref(0)
const answers = ref([])

const freeText = ref('')

const finalResults = ref(null)
const recommendations = ref([])

/**
 * Function that calls the services which call our Backend endpoints
 */
async function fetchData() {
  try {
    const fetchedQuestions = await accessQuestionsEndpoint()

    fetchedQuestions.push({
      id: 'free_text_question',
      question: 'Is there anything else you would like to add?',
      type: 'free_text'
    });
    questions.value = fetchedQuestions

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
  if (currentQuestionData.value?.type === 'free_text') {
    return FreeTextQuestion
  }
  return Question
})

const startQuestionnaire = () => {
  quizStarted.value = true
}

const handleNext = (payload: any) => {
  const currentQuestion = currentQuestionData.value;

  if (currentQuestion.type === 'free_text') {
    freeText.value = payload;
  }
  else {

    const existingAnswerIndex = answers.value.findIndex(
        (ans) => ans.question_id === payload.question_id
    );
    if (existingAnswerIndex !== -1) {
      answers.value[existingAnswerIndex] = payload;
    }
    else {
      answers.value.push(payload);
    }
  }

  if (currentStep.value < questions.value.length - 1) {
    currentStep.value++
  } else {
    quizFinished.value = true
    finalResults.value = {
      answers: answers.value,
      created_at: new Date().toISOString(),
      free_text: freeText.value
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
</script>

<template>
  <div class="questionnaire-wrapper">
    <Motion
        is="div"
        :initial="{ opacity: 0 }"
        :animate="{ opacity: 1 }"
        :transition="{ duration: 1.8 }"
        class="questionnaire-main-container">

      <!-- Start Screen -->
      <template v-if="!quizStarted">
        <h2>Discover our plant recommender!</h2>
        <p>This tool is made for you. Feel free to use it, to find the perfect companion for you and your flat.</p>
        <Motion
            class="questionnaire-start-button"
            is="button"
            :whileHover="{ scale: 1.1 }"
            :whilePress="{ scale: 0.95 }"
            :transition="{ duration: 0.2 }"
            @click="startQuestionnaire"
        >
          Find your perfect plant
        </Motion>
      </template>

      <!-- Questions -->
      <template v-else-if="!quizFinished">
        <Motion
            class="questionnaire-each-question"
            :key="currentStep"
            :initial="{ opacity: 0, x: 50 }"
            :animate="{ opacity: 1, x: 0 }"
            :exit="{ opacity: 0, x: -50 }"
            :transition="{ duration: 0.3 }"
        >
          <component
              :is="currentComponent"
              :question-data="currentQuestionData"
              @next="handleNext"/>
        </Motion>

        <div class="questionnaire-navigation" v-if="!isLoading && questions.length > 0">
          <ArrowLeft
              class="arrow-left-button"
              v-if="currentStep > 0"
              @click="handlePrevious"/>
          <span>Question {{ currentStep + 1 }} of {{ questions.length }}</span>
        </div>
      </template>

      <!-- Endscreen -->
      <template v-else>
        <EndOfQuestions :results="finalResults"/>
      </template>
    </Motion>

    <div v-if="quizFinished && recommendations.length > 0" class="recommendations-container">
      <h1>Your Plant Recommendations</h1>

      <template class="recommender-group-container" v-for="group in recommendations.values()">
        <h2>{{ group.label }}</h2>
        <PlantCard
            v-for="plant in group.recommendation"
            :name="plant.name"
            :description="plant.description"
            :waterAmount="plant.watering"
            :sunlightAmount="plant.sunlight"
            :image_url="plant.image_url"/>
      </template>
    </div>
  </div>
  <hr class="separator"/>
</template>

<style scoped>
.questionnaire-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.questionnaire-main-container {
  position: relative;
  width: 60%;
  max-width: 60rem;
  height: 30rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 1rem;
  box-shadow: 0 0.5rem 1rem 0 rgba(0,0,0,0.3);
  transition: transform 0.2s ease;
}
.questionnaire-main-container h2 {
  width: 100%;
  text-align: center;
  font-size: 1.75rem;
  background-color: #b7d5ac;
}
.questionnaire-main-container p {
  width: 80%;
  font-size: 1.5rem;
}

.questionnaire-each-question {
  width: 100%;
}

.questionnaire-start-button {
  width: 40%;
  height: 3rem;
  position: absolute;
  bottom: 2rem;
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
</style>
