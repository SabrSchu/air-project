<script setup lang="ts">
import {ref} from "vue";
import PlantCard from "@/components/PlantCard.vue";
import Pin from 'vue-material-design-icons/Pin.vue'
import PinOff from 'vue-material-design-icons/PinOff.vue'

import {postFreeText} from "@/services/questionsEndpointService.ts";

defineProps<{
  isPinned: boolean
}>();

const emit = defineEmits(['togglePin']);

const userInput = ref("");
const recommendations = ref([]);
const isLoading = ref(false);
const finalResults = ref(null)

const handleSend = async () => {
  if (!userInput.value.trim()) return;

  finalResults.value = {
    created_at: new Date().toISOString(),
    free_text: userInput.value
  }

  console.log("Send text:", JSON.stringify(finalResults.value, null, 2));
  isLoading.value = true;

  try {
    recommendations.value = await postFreeText(finalResults.value, {
      num_perfect_fits: 3,
      num_good_fits: 3,
      num_bad_fits: 3
    });
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
  <div class="chat-layout">
    <div class="header">
      <div class="visible-handle">Chat</div>
      <button @click="emit('togglePin')" class="pin-btn">
        <span v-if="isPinned"><Pin/></span>
        <span v-else><PinOff/></span>
      </button>
    </div>

    <div class="messages-area">
      <div class="recommendation-container-chat-window" v-if="recommendations.length > 0" v-for="group in recommendations.values()">
        <h2>{{ group.label }}</h2>
        <PlantCard
            v-for="plant in group.recommendation"
            :name="plant.name"
            :description="plant.description"
            :waterAmount="plant.watering"
            :sunlightAmount="plant.sunlight"
            :image_url="plant.image_url"/>
      </div>
    </div>

    <div class="footer">
      <input
          v-model="userInput"
          @keydown.enter="handleSend"
          class="chat-input"
          placeholder="Tell me what you are searching for..."
          :disabled="isLoading"
      />
      <button
          @click="handleSend"
          class="pin-btn"
          :disabled="isLoading"
      >
        <span v-if="isLoading">...</span>
        <span v-else>Send</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.chat-layout {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: white;
  border-radius: 1rem;
  overflow: hidden;
}

.header {
  padding: 1rem;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 0.1rem solid #ddd;
  flex-shrink: 0;
}

.messages-area {
  flex-grow: 1;
  overflow-y: auto;
  padding: 1rem;
}

.footer {
  display: flex;
  padding: 1rem;
  gap: 0.5rem;
  flex-direction: row;
  border-top: 0.1rem solid #eee;
  background-color: white;
  flex-shrink: 0;
}

.chat-input {
  width: 100%;
  padding: 0.8rem;
  border: 0.1rem solid #ccc;
  border-radius: 0.5rem;
  outline: none;
  box-sizing: border-box;
}

.chat-input:focus {
  border-color: #888;
}

.pin-btn {
  background: white;
  border: 0.1rem solid #ccc;
  padding: 0.3rem 0.8rem;
  cursor: pointer;
  border-radius: 0.4rem;
  font-size: 0.8rem;
}

.pin-btn:hover {
  background-color: #e0e0e0;
}

.recommendation-container-chat-window {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}
</style>
