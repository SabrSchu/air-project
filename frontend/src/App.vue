<template>
  <NavBar/>
  <Questionnaire/>
  <PlantOverview/>
<!--
  <div
      class="chat-drawer"
      :class="{ 'is-open': isOpen }"
      @mouseenter="openChat"
      @mouseleave="closeChat"
  >
    <ChatWindow
        :isPinned="isPinned"
        @togglePin="togglePin"
    />
  </div>
  -->
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import NavBar from "@/components/NavBar.vue";
import Header from "@/components/Header.vue";
import Questionnaire from "@/components/Questions/Questionnaire.vue";
import PlantOverview from "@/components/PlantOverview.vue";
import ChatWindow from "@/components/ChatWindow.vue";

const isHovered = ref(false);
const isPinned = ref(false);

const isOpen = computed(() => isHovered.value || isPinned.value);

const openChat = () => { isHovered.value = true; };
const closeChat = () => { isHovered.value = false; };
const togglePin = () => { isPinned.value = !isPinned.value; };
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');

* {
  font-family: 'Poppins', sans-serif;
}

a {
  text-decoration: none;
  color: black;
}

body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

/* ChatWindow Style */
.chat-drawer {
  position: fixed;
  bottom: 0;
  right: 0;
  width: 40rem;
  height: 70vh;
  border-radius: 1rem;
  border: 0.1rem solid #969696;

  box-shadow: -0.5rem -0.5rem 2rem rgba(0,0,0,0.1);
  z-index: 9999;

  /* Animation */
  transform: translateX(calc(100% - 1rem));
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
}

.chat-drawer.is-open {
  transform: translateX(0);
}
</style>
