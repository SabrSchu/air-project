<template>
  <div class="overview__wrapper">
    <div class="overview__header">
      <p>Plant Overview</p>
    </div>

    <!-- Plant Filter & Grid Options -->
    <div class="overview__option-container">
      <div class="overview__spacer"></div>

      <div class="overview__search">
        <MagnifyIcon/>
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

    <!-- Plant Cards Grid -->
    <div v-if="plants.length > 0" class="overview__elements" :class="{ 'grid-layout': isGridLarge }">
      <PlantCard
          v-for="plant in plants"
          :key="plant.id"
          :name="plant.name"
          :description="plant.description"
          :waterAmount="plant.watering"
          :sunlightAmount="plant.sunlight"
          :image_url="plant.image_url"/>
    </div>

    <!-- Pagination -->
    <div class="pagination" v-if="totalPages > 1 && plants.length > 0 && input.length === 0">
      <button
          class="page-btn"
          :disabled="currentPage === 1"
          @click="goToPage(currentPage - 1)"
      >
        &lt;
      </button>

      <button
          v-for="page in visiblePages"
          :key="page"
          :class="['page-btn', { active: page === currentPage, dots: page === '...' }]"
          @click="typeof page === 'number' ? goToPage(page) : null"
          :disabled="page === '...'"
      >
        {{ page }}
      </button>

      <button
          class="page-btn"
          :disabled="currentPage === totalPages"
          @click="goToPage(currentPage + 1)"
      >
        &gt;
      </button>
    </div>


    <!-- No plants found -->
    <div v-if="plants.length === 0" class="no-results">
      <p>No plants found. Please try again!</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted, watch, computed} from "vue";
import TuneIcon from 'vue-material-design-icons/Tune.vue'
import MagnifyIcon from 'vue-material-design-icons/Magnify.vue'
import ClearIcon from 'vue-material-design-icons/CloseThick.vue'
import GridIcon from 'vue-material-design-icons/Grid.vue'
import GridLargeIcon from 'vue-material-design-icons/GridLarge.vue'

import {accessPlantsEndpoint} from "@/services/plantEnpointService.ts";
import {filterPlantsByName} from "@/services/plantEnpointService.ts";
import PlantCard from "@/components/PlantCard.vue";

let input = ref("");
let plants = ref([]);
const currentPage = ref(1);
const plantsPerPage = 9;
const totalPlants = ref(0);
const totalPages = ref(1);
const isGridLarge = ref(true);

function toggleGridView() {
  isGridLarge.value = !isGridLarge.value;
}

async function fetchPlants(page: number) {
  try {
    const skip = (page - 1) * plantsPerPage;
    plants.value = await accessPlantsEndpoint(skip, plantsPerPage);
  }
  catch (error) {
    console.error("Error while fetching plants: ", error);
  }
}

async function fetchAllPlants() {
  try {
    let allPlants = await accessPlantsEndpoint(0, 600);
    totalPlants.value = allPlants.length;
    totalPages.value = Math.ceil(totalPlants.value / plantsPerPage);
  }
  catch (error) {
    console.error("Error while fetching plants: ", error);
  }
}

function goToPage(page: number) {
  currentPage.value = page;
  fetchPlants(page);
}

function resetOverview() {
  currentPage.value = 1;
  fetchAllPlants();
  fetchPlants(1);
}

// watcher for search filtering
let timer: number | undefined;
watch(input, (newValue) => {
  clearTimeout(timer);
  currentPage.value = 1;

  if (!newValue.trim()) {
    resetOverview();
    return;
  }

  timer = window.setTimeout(async () => {
    try {
      plants.value = await filterPlantsByName(newValue.trim());
      totalPages.value = 1;
      currentPage.value = 1;
    } catch (error) {
      console.error("Error searching plants:", error);
    }
  }, 300);
});

const visiblePages = computed(() => {
  const pages: (number | string)[] = [];
  const maxPagesToShow = 5;
  const half = Math.floor(maxPagesToShow / 2);

  if (totalPages.value <= maxPagesToShow) {
    for (let i = 1; i <= totalPages.value; i++) pages.push(i);
    return pages;
  }

  let start = currentPage.value - half;
  let end = currentPage.value + half;

  if (start <= 1) {
    start = 1;
    end = maxPagesToShow;
  }
  if (end >= totalPages.value) {
    end = totalPages.value;
    start = totalPages.value - maxPagesToShow + 1;
  }

  if (start > 1) pages.push(1, '...');
  for (let i = start; i <= end; i++) pages.push(i);
  if (end < totalPages.value) pages.push('...', totalPages.value);

  return pages;
});

onMounted(() => {
  fetchAllPlants(); // fetch all plants to get number of all plants
  fetchPlants(1);
});

</script>

<style scoped>
.overview__wrapper {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  background-color: rgb(183,213,172,0.3);
  background-blend-mode: lighten;
}

.overview__header{
  display: flex;
  align-items: center;
  justify-content: center;

  p {
    margin: 0;
    margin-top: 1rem;
    font-size: 1.5rem;
    font-weight: bold;
  }
}

.overview__option-container {
  display: flex;
  align-self: center;
  justify-self: center;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  width: 90%;
}

.overview__spacer {
  flex: 1;
}

.overview__search {
  flex: 1;
  display: flex;
  align-items: center;
  align-self: center;
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

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
  gap: 0.5rem;
}

.page-btn {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  border: none;
  background-color: white;
  cursor: pointer;
  transition: 0.2s;
}

.page-btn:hover {
  background-color: #b7d5ac;
  color: white;
}

.page-btn.dots {
  cursor: default;
  background-color: transparent;
  border: none;
}

.page-btn.active {
  background-color: #6a9a5f;
  color: white;
  font-weight: bold;
  border-color: #6a9a5f;
}

</style>