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
      meta: { title: 'Inicio' },
    },
    {
      path: '/contacto',
      name: 'Contacto',
      component: () => import('../views/ContactoView.vue'),
      meta: { title: 'Contacto' },
    },
    {
      path: '/noticias',
      name: 'Noticias',
      component: () => import('../views/NoticiasView.vue'),
      meta: { title: 'Actividades y noticias' },
    },
    {
      path: '/contenido/:id',
      name: 'ContenidoDetalle',
      component: () => import('../views/ContenidoDetalleView.vue'),
      props: true,
      meta: { title: 'Noticia' },
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

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'CEDICA';
  next();
});
export default router
