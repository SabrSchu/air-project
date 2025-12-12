<script setup lang="ts">
import DemoPlant from '@/assets/DemoPlant.jpg'
import WaterIcon from 'vue-material-design-icons/Water.vue'
import WeatherSunnyIcon from 'vue-material-design-icons/WeatherSunny.vue'
import CircleIcon from 'vue-material-design-icons/Circle.vue'
import SproutIcon from 'vue-material-design-icons/Sprout.vue'
import HeartIcon from 'vue-material-design-icons/Heart.vue'
import { ref } from 'vue'

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: "No description available"
  },
  waterAmount: {
    type: String,
    required: true
  },
  sunlightAmount: {
    type: String,
    required: true
  },
  fertilizerAmount: {
    type: String,
    required: true
  },
  image_url: {
    type: String,
    required: false,
    default: DemoPlant
  }
});

const isLiked = ref(false)

function showMessage() {
  console.log('Hello World');
}

function toggleLike() {
  isLiked.value = !isLiked.value
  if (isLiked.value === false) {
    console.log('Disliked this plant!')
  }
  else {
    console.log('Liked this plant!')
  }
}


function filledCircles(type: string) {
  if (type === 'sunlight') {
    switch (props.sunlightAmount.toLowerCase()) {
      case 'full sunlight': return 4
      case 'indirect sunlight': return 2;
      case 'partial sunlight': return 1;
      default: return 0;
    }
  }
  if (type === 'water') {
    switch (props.waterAmount.toLowerCase()) {
      case 'keep soil consistently moist': return 4;
      case 'keep soil evenly moist': return 4;
      case 'keep soil moist': return 4;
      case 'keep soil slightly moist': return 3;
      case 'let soil dry between watering': return 3;
      case 'regular watering': return 3;
      case 'regular, moist soil': return 2;
      case 'regular, well-drained soil': return 2;
      case 'water weekly': return 2;
      case 'water when soil feels dry': return 1;
      case 'water when soil is dry': return 1;
      case 'water when topsoil is dry': return 1;
      default: return 0;
    }
  }
  if (type === 'fertilizer') {
    switch (props.fertilizerAmount?.toLowerCase()) {
      case 'no': return 1;
      case 'organic': return 1;
      case 'balanced':return 2;
      case 'low-nitrogen': return 3;
      case 'acidic': return 4;
    }
  }
  return 0;
}
</script>

<template>
  <div class="plant-card">
    <img class="plant-image" :src="image_url && image_url !== '' ? image_url : DemoPlant" alt="Demo Plant" />

    <div class="text-box">
      <h1>{{ name }}</h1>

      <!--
      <p>{{ description }}</p>

      <button class="button-more-info" @click="showMessage">
        Let's find out more!
      </button>
      -->
    </div>
    <div class="value-box">
      <div class="favorite-box">
        <HeartIcon :style="{ color: isLiked ? 'red' : 'black' }" @click="toggleLike" />
      </div>
      <div class="water-value">
        <div class="water-icon-wrapper">
          <WaterIcon :size="25" />
        </div>
        <CircleIcon
            v-for="index in 4"
            :key="index"
            :size="15"
            :style="{ color: index <= filledCircles('water') ? 'deepskyblue' : 'currentColor' }"
        />
      </div>
      <div class="sun-value">
        <div class="sun-icon-wrapper">
          <WeatherSunnyIcon :size="25" />
        </div>
        <CircleIcon
            v-for="index in 4"
            :key="index"
            :size="15"
            :style="{ color: index <= filledCircles('sunlight') ? 'orange' : 'currentColor' }"
        />
      </div>
      <div class="temperature-value">
        <div class="temperature-icon-wrapper">
          <SproutIcon :size="25" />
        </div>
        <CircleIcon
            v-for="index in 4"
            :key="index"
            :size="15"
            :style="{ color: index <= filledCircles('fertilizer') ? 'red' : 'currentColor' }"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.plant-card {
  position: relative;
  max-width: 600px;
  max-height: 200px;
  display: flex;
  flex-direction: row;
  align-items: stretch;
  border: 2px solid #333;
  border-radius: 1rem;
  overflow: hidden;
}

.plant-image {
  width: 20%;
  object-fit: cover;
  padding: 1.5rem;
  border-radius: 2rem;
}

.text-box {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.text-box h1 {
  margin-top: 0.1rem;
  margin-bottom: 0.25rem;
}
.text-box p {
  margin-top: 0.25rem;
}

.button-more-info {
  align-self: center;
  width: 60%;
  height: 15%;
  color: white;
  background-color: darkgreen;
  border-radius: 1rem;
  transition: transform 0.2s ease;
}
.button-more-info:hover {
  cursor: pointer;
  transform: scale(1.1);
}
.button-more-info:active {
  transform: scale(0.95);
}

.value-box {
  flex-direction: column;
  justify-content: center;
  align-items: center;
  display: flex;
  width:20%;
  padding-top: 2rem;
  padding-right: 0.5rem;
  /*Just for development
  border: black solid 2px;*/
}

.favorite-box {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  transition: transform 0.2s ease;
}
.favorite-box:hover {
  cursor: pointer;
  transform: scale(1.2);
}
.favorite-box:active {
  transform: scale(0.95);
}

.water-value,
.sun-value,
.temperature-value {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  margin: 0.5rem;
  transition: transform 0.2s ease;
}
.water-icon-wrapper,
.temperature-icon-wrapper,
.sun-icon-wrapper {
  transition: transform 0.2s ease;
  display: flex;
  align-items: center;
}
.water-icon-wrapper:hover,
.temperature-icon-wrapper:hover,
.sun-icon-wrapper:hover{
  cursor: pointer;
  transform: scale(1.2);
}
.water-icon-wrapper:active,
.temperature-icon-wrapper:active,
.sun-icon-wrapper:active{
  transform: scale(0.95);
}
</style>