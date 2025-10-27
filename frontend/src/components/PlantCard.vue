<script setup lang="ts">
import DemoPlant from '@/assets/DemoPlant.jpg'

let name = "Monstera";
let description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec condimentum velit vel augue rutrum, in mattis nibh ornare.";

function showMessage() {
  console.log('Hello World');
}
</script>

<template>
  <div class="plant-card">
    <img class="plant-image" :src="DemoPlant" alt="Demo Plant" />

    <div class="text-box">

      <h1>{{ name }}</h1>

      <p>
        {{ description }}
      </p>

      <button class="button-more-info" @click="showMessage">
        Let's find out more!
      </button>
    </div>
  </div>
</template>

<style scoped>
.plant-card {
  max-width: 600px;
  max-height: 200px;
  display: flex;
  flex-direction: row;
  align-items: stretch;
  border: 2px solid #333;
  border-radius: 10px;
  overflow: hidden;
}

.plant-image {
  width: 30%;
  object-fit: cover;
  padding: 1.5rem;
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
  height: 25px;
  color: white;
  background-color: darkgreen;
  border-radius: 10px;
}

.score-box {
  display: flex;
  width:20%;
  border: black solid 1px;
}
</style>