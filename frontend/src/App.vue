<template>
  <NavBar/>
  <Header/>
  <QuestionCards/>
  <PlantOverview/>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');

* {
  font-family: 'Poppins', sans-serif;
}

a {
  text-decoration: none;
  color: black;
}

body{
  margin: 0;
  padding: 0;
}

</style>

<script setup lang="ts">
import NavBar from "@/components/NavBar.vue";
import Header from "@/components/Header.vue";
import QuestionCards from "@/components/QuestionCards.vue";
import PlantOverview from "@/components/PlantOverview.vue";
</script>
