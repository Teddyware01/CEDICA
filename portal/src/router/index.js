import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ContactoView from '../views/ContactoView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/contacto',
      name: 'Contacto',
      component: () => import('../views/ContactoView.vue'),
    },
    {
      path: '/noticias',
      name: 'Noticias',
      component: () => import('../views/NoticiasView.vue'),
    },

    // Las siguientes rutas son las de las explicaciones practias (de ejemplo)
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/issues',
      name: 'issues',
      component: () => import('../views/IssuesView.vue'),
    },
  ],
})

export default router
