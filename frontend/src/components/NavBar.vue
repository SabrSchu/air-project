<template>
  <header class="header">
    <nav class="navbar">
      <div class="wrapper">
        <div class="logo">
          <LeafIcon/>
          <RouterLink to="/">Plant Finder</RouterLink>
        </div>

        <div class="links">
          <RouterLink to="/favourites">Favourites</RouterLink>
          <span>|</span>
          <RouterLink to="/feedback">Feedback</RouterLink>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
import LeafIcon from 'vue-material-design-icons/Leaf.vue'
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.header {
  display: flex;
  flex-direction: column;
  width: 100%;
  position: sticky;
  top: 0;
  z-index: 100;

  .navbar {
    background-color: #b7d5ac;
    padding: 1rem;

    .wrapper {
      display: flex;
      flex-direction: row;
      margin-right: 2rem;
      gap: 2rem;

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
  }
}
</style>
