<script setup lang="ts">
import DemoPlant from '@/assets/DemoPlant.jpg'
import ScoreGauge from "@/components/ScoreGauge.vue";
import MetadataVisulizerTest from "@/components/MetadataVisulizerTest.vue";
import WaterIcon from 'vue-material-design-icons/Water.vue'
import WeatherSunnyIcon from 'vue-material-design-icons/WeatherSunny.vue'
import CircleIcon from 'vue-material-design-icons/Circle.vue'
import SproutIcon from 'vue-material-design-icons/Sprout.vue'
import HeartIcon from 'vue-material-design-icons/Heart.vue'
import InformationOutline from 'vue-material-design-icons/InformationOutline.vue'
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import {likePlantEndpoint, unlikePlantEndpoint} from "@/services/plantEnpointService.ts";

const emit = defineEmits(['toggle-like']);

const props = defineProps({
  id: {
    type: Number,
    required: true
  },
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
  },
  liked: {
    type: Boolean,
    required: false,
    default: false
  },
  metadata: {
    type: Object,
    required: false,
    default: null
  }
});

// Section for PopoverItem
const isMetadataOpen = ref(false)
const popoverRef = ref<HTMLElement | null>(null)

function toggleMetadata() {
  if (!props.metadata) return
  isMetadataOpen.value = !isMetadataOpen.value
}

function closeMetadata() {
  isMetadataOpen.value = false
}

function handleClickOutside(event: MouseEvent) {
  if (popoverRef.value && !popoverRef.value.contains(event.target as Node)) {
    closeMetadata()
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', handleClickOutside))

const isLiked = ref(props.liked)

watch(() => props.liked, (newVal) => {
  isLiked.value = newVal;
});

async function toggleLike() {
  const previousState = isLiked.value;

  isLiked.value = !isLiked.value
  emit('toggle-like', props.id, isLiked.value);

  try {
    if (isLiked.value) {
      await likePlantEndpoint(props.id);
    } else {
      await unlikePlantEndpoint(props.id);
    }
  } catch (error) {
    console.error("API Error - Rolling back UI:", error);

    isLiked.value = previousState;
    emit('toggle-like', props.id, previousState);
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
    <button
        v-if="metadata"
        class="info-button"
        type="button"
        @click.stop="toggleMetadata"
    >
      <InformationOutline :size="18" />
    </button>

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
    <transition name="fade-scale">
      <div
          v-if="isMetadataOpen"
          class="metadata-popover"
          ref="popoverRef"
      >
        <slot name="metadata" :metadata="metadata">
          <!-- fallback -->
          <section class="metadata-grid">
            <MetadataVisulizerTest :metadata="metadata" />
            <ScoreGauge label="Normalized" :value="metadata.cosine_sim_normalized" />
            <ScoreGauge label="Percentile" :value="metadata.cosine_sim_percentile" />
          </section>
        </slot>
      </div>
    </transition>
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
  border: 2px solid white;
  border-radius: 1rem;
  overflow: visible;
  background-color: white;
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

.info-button {
  position: absolute;
  top: 0.3rem;
  left: 0.3rem;
  width: 2rem;
  height: 2rem;
  border: none;
  border-radius: 100rem;
  background: white;
  box-shadow: 0 0.25rem 0.5rem rgba(0,0,0,0.2);
  display: grid;
  place-items: center;
  cursor: pointer;
}
.info-button:hover {
  background: rgba(240, 240, 240, 0.5);
}

.metadata-popover {
  position: absolute;
  bottom: calc(100% + 0.5rem);
  width: fit-content;
  padding: 1rem;
  z-index: 20;
  border-radius: 0.75rem;
  background: #ffffff;
  box-shadow: 0 0.75rem 1.5rem rgba(0,0,0,0.25);
  transform-origin: bottom left;
}

.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>