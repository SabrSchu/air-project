<template>
  <div class="overview__wrapper">
    <div class="overview__option-container">
      <div class="overview__spacer"></div>

      <div class="overview__search">
        <MagnifyIcon size="1.2rem"/>
        <input v-model="input" placeholder="Search"></input>
        <ClearIcon
            v-if="input"
            size="0.8rem"
            class='overview__search-clear-icon'
            @click="input = ''"
        />
      </div>

      <div class="overview__actions">
        <GridIcon
            v-if="!isGridLarge"
            class="overview__actions-item"
            @click="toggleGridView"
        />
        <GridLargeIcon
            v-else
            class="overview__actions-item"
            @click="toggleGridView"
        />
        <TuneIcon class="overview__actions-item"/>
      </div>
    </div>

    <div v-if="response.length > 0" class="overview__elements" :class="{ 'grid-layout': isGridLarge }">
      <PlantCard
          v-for="plant in response"
          :key="plant.id"
          :name="plant.name"
          :description="plant.description"
          :waterAmount="plant.watering"
          :sunlightAmount="plant.sunlight"
          :image_url="plant.image_url"/>
    </div>

    <div v-else class="no-results">
      <p>No plants found. Please try again!</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted, watch} from "vue";
import TuneIcon from 'vue-material-design-icons/Tune.vue'
import MagnifyIcon from 'vue-material-design-icons/Magnify.vue'
import ClearIcon from 'vue-material-design-icons/CloseThick.vue'
import GridIcon from 'vue-material-design-icons/Grid.vue'
import GridLargeIcon from 'vue-material-design-icons/GridLarge.vue'

import {accessPlantsEndpoint} from "@/services/plantEnpointService.ts";
import {filterPlantsByName} from "@/services/plantEnpointService.ts";
import PlantCard from "@/components/PlantCard.vue";

let input = ref("");
let response = ref([]);

const isGridLarge = ref(true);

function toggleGridView() {
  isGridLarge.value = !isGridLarge.value;
}

async function fetchPlants() {
  try {
    response.value = await accessPlantsEndpoint();
  }
  catch (error) {
    console.error("Error while fetching plants: ", error);
  }
}

let timer: number | undefined;

watch(input, (newValue) => {
  clearTimeout(timer);

  if (!newValue.trim()) {
    fetchPlants();
    return;
  }

  timer = window.setTimeout(async () => {
    try {
      response.value = await filterPlantsByName(newValue.trim());
    } catch (error) {
      console.error("Error searching plants:", error);
    }
  }, 300);
});

onMounted(() => {
  fetchPlants();
});

</script>

<style scoped>
.overview__wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  background-color: rgb(183,213,172,0.3);
  background-blend-mode: lighten;
}

.overview__option-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.overview__spacer {
  flex: 1;
}

.overview__search {
  flex: 1;
  display: flex;
  align-items: center;
  position: relative;
  border: 1px solid white;
  border-radius: 0.5rem;
  padding: 0.3rem 0.5rem;
  min-width: 18rem;
  max-width: 18rem;
  background-color: white;
}

.overview__search input {
  flex: 1;
  border: none;
  outline: none;
  padding: 0 0.3rem;
}

.overview__search-clear-icon {
  cursor: pointer;
  margin-left: auto;
}

.overview__actions {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.3rem;
}

.overview__actions-item {
  cursor: pointer;
}

.overview__elements {
  display: flex;
  flex-direction: column;
  align-items: center;
  /*if more then one card*/
  gap: 0.5rem;
}

.grid-layout {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  width: 90%;
  align-items: flex-start;
  margin: auto;
}

.no-results {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 12rem;
  font-size: 1.2rem;
  color: #555;
  text-align: center;
}

</style>