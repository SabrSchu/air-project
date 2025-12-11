<template>
  <header class="header">
    <nav class="navbar">
      <div class="wrapper">
        <div class="logo">
          <LeafIcon/>
          <a href="/">Plant Finder</a>
        </div>

        <div class="links">
          <a href="#categories">Categories</a>
          <span>|</span>
          <a href="#favourites">Favourites</a>
        </div>
      </div>
    </nav>

    <motion.div class="title"
                :initial="{ scale: 0 }"
                :animate="{ scale: 1, transition: { duration: 0.6 } }"
    >
      <h1>Welcome to Plant Finder!</h1>
      <TreeIcon/>
    </motion.div>
  </header>
</template>

<script setup lang="ts">
import LeafIcon from 'vue-material-design-icons/Leaf.vue'
import TreeIcon from 'vue-material-design-icons/Tree.vue'
import { motion } from 'motion-v'
</script>

<style scoped>
.header {
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: #b7d5ac;
  padding: 1rem;

  .wrapper {
    display: flex;
    flex-direction: row;
    margin-right: 2rem;
    gap: 2rem;
  }

  .logo {
    display: flex;
    gap: 0.5rem;

    a {
      font-size: 1.3rem;
      text-decoration: none;
    }
  }

  .links {
    display: flex;
    gap: 1.5rem;
    align-self: center;
    justify-self: flex-end;
    margin-left: auto;

    a {
      text-decoration: none;

      &:hover {
        transition: transform 0.2s ease;
        transform: scale(1.1);
      }
    }
  }
}

.title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem;
  margin: 0 auto;
}
</style>
