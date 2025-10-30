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
        <ChevronDownIcon class="overview__actions-item"/>
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

    <div class="overview__elements" :class="{ 'grid-layout': isGridLarge }">
      <PlantCard
          v-for="plant in testJson"
          :key="plant.id"
          :name="plant.name"
          :description="plant.description"
          :water-amount="plant.watering"
          :sunlight-amount="plant.sunlight"/>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import TuneIcon from 'vue-material-design-icons/Tune.vue'
import MagnifyIcon from 'vue-material-design-icons/Magnify.vue'
import ChevronDownIcon from 'vue-material-design-icons/ChevronDown.vue'
import ClearIcon from 'vue-material-design-icons/CloseThick.vue'
import GridIcon from 'vue-material-design-icons/Grid.vue'
import GridLargeIcon from 'vue-material-design-icons/GridLarge.vue'

import testJson from "@/assets/test-plants.json";
import PlantCard from "@/components/PlantCard.vue";

let input = ref("");

const isGridLarge = ref(true);

function toggleGridView() {
  isGridLarge.value = !isGridLarge.value;
}

</script>

<style scoped>
.overview__wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
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
  align-self: center;
  gap: 0.2rem;
  border: 1px solid black;
  border-radius: 0.5rem;
  padding: 0.3rem 0.5rem;
  min-width: 18rem;
  max-width: 18rem;
}

.overview__search input {
  border: none;
  outline: none;
}

.overview__search-clear-icon {
  cursor: pointer;
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



</style>