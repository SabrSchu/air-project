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
            :size="13"
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
        <TuneIcon
            class="overview__actions-item"
            @click="toggleFilterVisible"
        />
      </div>
    </div>

    <!-- Filter Panel -->
    <div v-if="isFilterVisible" class="filter-panel">
      <h1>Filter Plants by ...</h1>
      <div class="filter-content">
        <div class="filter-group">
          <label>Growth</label>
          <select v-model="selectedFilters.growth">
            <option>All</option>
            <option>Slow</option>
            <option>Moderate</option>
            <option>Fast</option>
          </select>
        </div>

        <div class="filter-group">
          <label>Soil</label>
          <select v-model="selectedFilters.soil">
            <option>All</option>
            <option>Well-drained</option>
            <option>Sandy</option>
            <option>Moist</option>
            <option>Loamy</option>
            <option>Acidic</option>
          </select>
        </div>

        <div class="filter-group">
          <label>Sun</label>
          <select v-model="selectedFilters.sun">
            <option>All</option>
            <option>Full Sunlight</option>
            <option>Indirect Sunlight</option>
            <option>Partial Sunlight</option>
          </select>
        </div>

        <div class="filter-group">
          <label>Water</label>
          <select v-model="selectedFilters.water">
            <option>All</option>
            <option>Concistently Moist</option>
            <option>Evenly Moist</option>
            <option>Moist</option>
            <option>Regular Moist</option>
            <option>Regular well drained</option>
            <option>Water when dry</option>
            <option>Weekly</option>
          </select>
        </div>

        <div class="filter-group">
          <label>Fertilization</label>
          <select v-model="selectedFilters.fertilization">
            <option>All</option>
            <option>Acidic</option>
            <option>Low Nitrogen</option>
            <option>Balanced</option>
            <option>No Fertilizer</option>
            <option>Organic</option>
          </select>
        </div>
      </div>

      <div class="filter-actions">
        <button class="apply-btn"
                @click="applyFilters">
          Apply
        </button>
        <button
            class="clear-btn"
            @click="clearFilters">
          Clear All
        </button>
      </div>
    </div>

    <!-- Plant Cards Grid -->
    <div v-if="plantsToShow.length > 0" class="overview__elements" :class="{ 'grid-layout': isGridLarge }">
      <PlantCard
          v-for="plant in plantsToShow"
          :key="plant.id"
          :id="plant.id"
          :name="plant.name"
          :description="plant.description"
          :waterAmount="plant.watering"
          :sunlightAmount="plant.sunlight"
          :fertilizerAmount="plant.fertilization"
          :image_url="plant.image_url"
          :liked="isPlantLiked(plant.id)"
          @toggle-like="handleOverviewToggleLike"/>
    </div>

    <!-- Pagination -->
    <div class="pagination" v-if="totalPages > 1 && input.length === 0">
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
import {ref, onMounted, watch, computed, reactive} from "vue";
import TuneIcon from 'vue-material-design-icons/Tune.vue'
import MagnifyIcon from 'vue-material-design-icons/Magnify.vue'
import ClearIcon from 'vue-material-design-icons/CloseThick.vue'
import GridIcon from 'vue-material-design-icons/Grid.vue'
import GridLargeIcon from 'vue-material-design-icons/GridLarge.vue'

import {
  accessPlantsEndpoint,
  filterPlantsByName,
  getAllFavouritePlantsEndpoint,
  filterPlantsByOptions
} from "@/services/plantEndpointService.ts";
import PlantCard from "@/components/PlantCard.vue";

const plants = ref([]);
const plantsToShow = computed(() => {
  const start = (currentPage.value - 1) * plantsPerPage;
  const end = start + plantsPerPage;

  return plants.value.slice(start, end);
})
const likedPlantIds = ref<number[]>([]);

const currentPage = ref(1);
const plantsPerPage = 9;
const totalPlants = computed(() => {
  return plants.value.length;
})
const totalPages = computed(() => {
  return Math.ceil(totalPlants.value / plantsPerPage);
})

const isGridLarge = ref(true);
let input = ref("");
const isFilterVisible = ref(false);
const selectedFilters = reactive({
  growth: "All",
  soil: "All",
  sun: "All",
  water: "All",
  fertilization: "All"
});

onMounted(() => {
  fetchLikedPlants();
  fetchAllPlants();
  goToPage(1);
});

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
      currentPage.value = 1;
    } catch (error) {
      console.error("Error searching plants:", error);
    }
  }, 300);
});

const toggleGridView = () => {
  isGridLarge.value = !isGridLarge.value;
}

const toggleFilterVisible = () => {
  isFilterVisible.value = !isFilterVisible.value;
}

const resetOverview = () => {
  currentPage.value = 1;
  fetchAllPlants();
  goToPage(1);
}

const fetchAllPlants = async () => {
  try {
    plants.value = await accessPlantsEndpoint(0, 600);
  }
  catch (error) {
    console.error("Error while fetching plants: ", error);
  }
}

const applyFilters = async () => {
  try {
    const filters = Object.fromEntries(
        Object.entries(selectedFilters)
            .filter(([_, val]) => val !== "All")
            .map(([key, val]) => [key, val.toLowerCase().replaceAll(" ", "_")])
    );

    if (Object.keys(filters).length === 0) {
      toggleFilterVisible();
      return;
    }

    plants.value = await filterPlantsByOptions(filters);
    currentPage.value = 1;

    toggleFilterVisible();

  } catch (error) {
    console.error("Error filtering plants:", error);
  }
}

const clearFilters = () => {
  selectedFilters.growth = "All";
  selectedFilters.soil = "All";
  selectedFilters.sun = "All";
  selectedFilters.water = "All";
  selectedFilters.fertilization = "All";

  input.value = "";

  toggleFilterVisible();
  resetOverview();
}

const goToPage = (page: number) => {
  currentPage.value = page;
}

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

const fetchLikedPlants = async () => {
  try {
    const favorites = await getAllFavouritePlantsEndpoint();
    likedPlantIds.value = favorites.map((plant: any) => plant.id);
  } catch (error) {
    console.error("Error fetching favorites:", error);
  }
}

const isPlantLiked = (plantId: number): boolean => {
  return likedPlantIds.value.includes(plantId);
}

const handleOverviewToggleLike= (id: number, isLiked: boolean) => {
  if (isLiked) {
    if (!likedPlantIds.value.includes(id)) {
      likedPlantIds.value.push(id);
    }
  } else {
    likedPlantIds.value = likedPlantIds.value.filter(existingId => existingId !== id);
  }
}

</script>

<style scoped>
@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.overview__wrapper {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  background-color: rgb(183,213,172,0.3);
  background-blend-mode: lighten;
  container-type: inline-size;
  container-name: plant-overview;

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

      input {
        flex: 1;
        border: none;
        outline: none;
        padding: 0 0.3rem;
      }

      .overview__search-clear-icon {
        cursor: pointer;
        margin-left: auto;
      }
    }

    .overview__actions {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 0.3rem;

      .overview__actions-item {
        cursor: pointer;
      }
    }
  }

  .filter-panel {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    width: 70%;
    margin: 0 auto 1rem auto;
    background-color: white;
    border-radius: 0.5rem;
    padding: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    animation: slideDown 0.3s ease-out;

    h1 {
      margin-top: 0;
      margin-bottom: 1.4rem;
      font-size: 1rem;
      color: #333;
    }

    .filter-content {
      display: flex;
      gap: 2rem;
      flex-wrap: wrap;
      align-items: center;
      justify-content: center;

      .filter-group {
        display: flex;
        flex-direction: column;
        gap: 0.3rem;

        label {
          font-size: 0.9rem;
          font-weight: bold;
          color: #555;
        }

        select {
          padding: 0.4rem;
          border: 1px solid #ccc;
          border-radius: 0.3rem;
          min-width: 150px;
        }
      }
    }

    .filter-actions {
      display: flex;
      justify-content: flex-end;
      gap: 1rem;
      margin-top: 1rem;
      padding-top: 1rem;
      border-top: 1px solid #eee;

      .apply-btn {
        background-color: white;
        border: 1px solid #ccc;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem;
        cursor: pointer;

        &:hover {
          background-color: #b7d5ac;
        }
      }

      .clear-btn {
        background-color: white;
        border: 1px solid #ccc;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem;
        cursor: pointer;

        &:hover {
          background-color: #b7d5ac;
        }
      }
    }
  }

  .overview__elements {
    display: flex;
    flex-direction: column;
    align-items: center;
    /*if more then one card*/
    gap: 0.5rem;

    &.grid-layout {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1rem;
      width: 90%;
      align-items: flex-start;
      margin: auto;

      @container plant-overview (max-width: 1100px) {
        grid-template-columns: repeat(2, 1fr);
      }

      @container plant-overview (max-width: 700px) {
        grid-template-columns: 1fr;
      }
    }
  }

  .pagination {
    display: flex;
    justify-content: center;
    margin-top: 1rem;
    gap: 0.5rem;

    .page-btn {
      padding: 0.5rem 1rem;
      border-radius: 0.5rem;
      border: none;
      background-color: white;
      cursor: pointer;
      transition: 0.2s;

      &:hover {
        background-color: #b7d5ac;
        color: white;
      }

      &.dots {
        cursor: default;
        background-color: transparent;
        border: none;
      }

      &.active {
        background-color: #6a9a5f;
        color: white;
        font-weight: bold;
        border-color: #6a9a5f;
      }
    }
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
}

</style>