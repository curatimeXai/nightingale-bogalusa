import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import InfoPage from '../views/InfoPage.vue'

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/info', name: 'Info', component: InfoPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
