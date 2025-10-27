<template>
  <div class="main-div">
    <PlantCard />
  </div>
  <div class="button-div">
    <TestButton />
    <DataButton />
  </div>
</template>

<script setup lang="ts">
import TestButton from './components/TestButton.vue'
import DataButton from './components/DataButton.vue'
import PlantCard from './components/PlantCard.vue'
</script>

<style scoped>
.main-div {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.button-div {
  background-color: white;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>