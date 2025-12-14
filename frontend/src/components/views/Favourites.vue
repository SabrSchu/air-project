<template>
  <div class="favourites-wrapper">
    <!-- Page Title --->
    <motion.div class="title"
                :initial="{ scale: 0 }"
                :animate="{ scale: 1, transition: { duration: 0.6 } }"
    >
      <h1>My favourite Plants</h1>
      <TreeIcon/>
    </motion.div>

    <div class="favourites-cards__background">
      <!-- Favourite Grid --->
      <div class="favourites-grid">
        <div v-if="favourites.length === 0" class="empty-message">
          <p>You haven't added any favourites yet!</p>
        </div>

        <!-- Plant Cards Grid -->
        <div v-else class="grid-layout">
          <PlantCard
              v-for="plant in favourites"
              :key="plant.id"
              :id="plant.id"
              :name="plant.name"
              :description="plant.description"
              :waterAmount="plant.watering"
              :sunlightAmount="plant.sunlight"
              :fertilizerAmount="plant.fertilization"
              :image_url="plant.image_url"
              :liked="true"
              @toggle-like="handleLikeToggle"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { motion } from 'motion-v'
import {onMounted, ref} from 'vue';
import TreeIcon from "vue-material-design-icons/Tree.vue";
import {getAllFavouritePlantsEndpoint} from "@/services/plantEnpointService.ts";
import PlantCard from "@/components/PlantCard.vue";

const favourites = ref<any[]>([]);

async function fetchFavourites() {
  try {
    favourites.value = await getAllFavouritePlantsEndpoint();
  }
  catch (error) {
    console.error("Error while fetching plants: ", error);
  }
}

function handleLikeToggle(id: number, isLiked: boolean) {
  if(!isLiked) {
    favourites.value = favourites.value.filter(plant => plant.id !== id);
  }
}

onMounted(() => {
  fetchFavourites();
});
</script>

<style scoped>
.favourites-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;

  .title {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.5rem;
    width: 100%;
    background-color: white;
  }

  .favourites-cards__background{
    flex: 1;
    width: 100%;
    min-height: 0;
    display: flex;
    justify-content: center;
    align-self: flex-start;
    padding-top: 1rem;
    padding-bottom: 1rem;
    background-image: url("/background.jpeg");
    background-color: rgba(255,255,255,0.3);
    background-blend-mode: lighten;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
  }

  .favourites-grid {
    padding: 2rem;
    margin: 1rem;
    border-radius: 1rem;
    box-shadow: 0 0.6rem 1.5rem rgba(0,0,0,0.15);
    background-color: rgb(183,213,172,0.6);
    max-width: 90%;
    width: 100%;
    max-height: 40rem;
    overflow-y: auto;
    scroll-behavior: smooth;
    container-type: inline-size;
    container-name: favourites-list;

    .empty-message {
      grid-column: 1 / -1;
      text-align: center;
      color: black;
      padding: 2rem;
    }

    .grid-layout {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1.5rem;
      width: 90%;
      align-items: flex-start;
      justify-items: center;
      margin: auto;

      @container favourites-list (max-width: 1100px) {
        grid-template-columns: repeat(2, 1fr);
      }

      @container favourites-list (max-width: 700px) {
        grid-template-columns: 1fr;
      }
    }
  }
}

</style>