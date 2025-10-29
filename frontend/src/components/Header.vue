<template>
  <motion.div class="header"
              :initial="{ scale: 0 }"
              :animate="{ scale: 1, transition: { duration: 0.6 } }"
  >
    <h1>Welcome to Plant Finder!</h1>
    <TreeIcon/>
  </motion.div>
</template>

<script setup lang="ts">
import TreeIcon from 'vue-material-design-icons/Tree.vue'
import { motion } from 'motion-v'

</script>

<style scoped>
  .header {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }
</style>