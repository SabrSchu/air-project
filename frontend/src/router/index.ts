import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/views/Home.vue'
import Favourites from '../components/views/Favourites.vue'
import Feedback from '../components/views/Feedback.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/feedback',
      name: 'feedback',
      component: Feedback
    },
    {
      path: '/favourites',
      name: 'favourites',
      component: Favourites
    }
  ]
})

export default router