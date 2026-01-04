<template>
  <div class="app-container">
    <NavBar/>
    <main>
      <RouterView />
    </main>
    <Footer/>
  </div>
</template>

<script setup lang="ts">
import {RouterView} from 'vue-router';
import NavBar from "@/components/NavBar.vue";
import Footer from "@/components/Footer.vue";
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');

* {
  font-family: 'Poppins', sans-serif;
}

a {
  text-decoration: none;
  color: black;
}

body {
  margin: 0;
  padding: 0;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  min-width: 320px;
}

main {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
}
</style>
