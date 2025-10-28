<template>
  <div class="main-div">
    <PlantCard
        v-for="plant in testJson"
        :key="plant.id"
    :name="plant.name"
    :description="plant.description"
    :water-amount="plant.watering"
    :sunlight-amount="plant.sunlight"/>
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
import testJson from './assets/test-plants.json'
</script>

<style scoped>
.main-div {
  display: flex;
  flex-direction: column;
  align-items: center;
  /*if more then one card*/
  gap: 0.5rem;
}

.button-div {
  background-color: white;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>