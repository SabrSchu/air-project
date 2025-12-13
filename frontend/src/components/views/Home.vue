<template>
  <motion.div class="title"
              :initial="{ scale: 0 }"
              :animate="{ scale: 1, transition: { duration: 0.6 } }"
  >
    <h1>Welcome to Plant Finder!</h1>
    <TreeIcon/>
  </motion.div>

  <Questionnaire/>
  <PlantOverview/>
</template>

<script setup lang="ts">
import PlantOverview from "@/components/PlantOverview.vue";
import Questionnaire from "@/components/Questions/Questionnaire.vue";
import TreeIcon from "vue-material-design-icons/Tree.vue";
import { motion } from 'motion-v'
</script>

<style scoped>
.title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem;
  width: 100%;
  background-color: white;
}
</style>