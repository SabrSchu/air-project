<template>
  <nav class="navbar" ref="navbarRef">
    <div class="navbar__container">
      <div class="navbar__logo">
        <LeafIcon/>
        <a href="/">Plant Finder</a>
      </div>

      <div class="navbar__menu">
        <div class="navbar__links">
          <a href="#categories">Categories</a>
          <span>|</span>
          <a href="#favourites">Favourites</a>
        </div>

        <button class="navbar__burger" @click="toggleMenu">
          <MenuIcon size="1.5rem"/>
        </button>
      </div>
    </div>

    <div v-if="isMenuOpen" class="navbar__dropdown">
      <div class="navbar__dropdown-item">
        <ShapeIcon/>
        <a href="#categories" @click="toggleMenu">Categories</a>
      </div>
      <div class="navbar__dropdown-item">
        <HeartIcon/>
        <a href="#favourites" @click="toggleMenu">Favourites</a>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import LeafIcon from 'vue-material-design-icons/Leaf.vue'
import MenuIcon from 'vue-material-design-icons/Menu.vue'
import HeartIcon from 'vue-material-design-icons/Heart.vue'
import ShapeIcon from 'vue-material-design-icons/ShapePlus.vue'

const isMenuOpen = ref(false)
const navbarRef = ref<HTMLElement | null>(null)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (isMenuOpen.value && navbarRef.value && !navbarRef.value.contains(target)) {
    isMenuOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
  .navbar {
    background-color: #b7d5ac;
  }

  .navbar__container {
    display: flex;
    padding: 1rem;
  }

  .navbar__logo {
    display: flex;
    gap: 0.5rem;
  }

  .navbar__logo a {
    font-size: 1.3rem;
    text-decoration: none;
  }

  .navbar__menu {
    display: flex;
    align-content: center;
    justify-content: center;
    gap: 5rem;
    margin-left: auto;
  }

  .navbar__links {
    display: flex;
    gap: 1.5rem;
    align-self: center;
  }

  .navbar__links a {
    text-decoration: none;
  }

  .navbar__links a:hover {
    transition: transform 0.2s ease;
    transform: scale(1.1);
  }

  .navbar__dropdown {
    position: absolute;
    top: 3rem;
    right: 1rem;
    display: flex;
    flex-direction: column;
    padding: 0.8rem 0.8rem;
    background-color: #e0f0da;
    border-radius: 0.2rem;
  }

  .navbar__dropdown:hover  {
    transition: transform 0.2s ease;
    transform: scale(1.05);
  }

  .navbar__dropdown-item {
    display: flex;
    gap: 0.5rem;
  }

  .navbar__dropdown-item a {
    text-decoration: none;
    cursor: pointer;
  }

  .navbar__dropdown-item a:hover  {
    transition: transform 0.2s ease;
    transform: scale(1.1);
  }

  .navbar__burger {
    display: flex;
    justify-content: center;
    align-items: center;
    background: none;
    border: none;
    cursor: pointer;
    align-self: center;
    padding: 0;
  }

  .navbar__burger:hover {
    transition: transform 0.2s ease;
    transform: scale(1.2);
  }

</style>
