<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Motion } from 'motion-v'
import Question from './Question.vue'
import EndOfQuestions from "./EndOfQuestions.vue";

import {accessQuestionsEndpoint} from "@/services/questionsEnpointService.ts";

const isLoading = ref(true)
const questions = ref([])
const quizStarted = ref(false)
const quizFinished = ref(false)
const currentStep = ref(0)
const answers = ref([])

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

const startQuestionnaire = () => {
  quizStarted.value = true
}

const handleNext = (answer: string) => {
  answers.value[currentQuestionData.value.id] = answer

  if (currentStep.value < questions.value.length - 1) {
    currentStep.value++
  } else {
    quizFinished.value = true
    console.log('Final Answers:', answers.value)
  }
}

const handlePrevious = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const sendResults = () => {
  console.log("Sending questionnaire...")
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
          <Question
              :question-data="currentQuestionData"
              @next="handleNext"/>
        </Motion>

        <div class="questionnaire-navigation" v-if="!isLoading && questions.length > 0">
          <button
              v-if="currentStep > 0"
              @click="handlePrevious"
          >
            Back
          </button>
          <span>Question {{ currentStep + 1 }} of {{ questions.length }}</span>
        </div>
      </template>

      <!-- Endscreen (muss noch eingefügt werden)-->
      <template v-else>
        <EndOfQuestions :answers="answers" />
      </template>
    </Motion>
</div>
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
  height: 25rem;
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
  background-color: #b7d5ac;
}
.questionnaire-main-container p {
  width: 80%;
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
  align-items: center;
}
</style>
