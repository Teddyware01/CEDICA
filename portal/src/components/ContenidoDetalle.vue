<template>
  <div>
    <h2>{{ noticia.titulo }}</h2>
    <p>{{ noticia.copete }}</p>
    <p>{{ noticia.contenido }}</p>
    <p>Publicado el: {{ noticia.published_at }}</p>
    <p>Por el user: {{ noticia.author_user_id }}</p>
    <p>Tipo publicacion: {{ noticia.tipo }}</p>
    <p>Estado: {{ noticia.estado }}</p>
    <button @click="$router.push('/')">Volver</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const noticia = ref({});

onMounted(() => {
  // Simula que obtienes la noticia desde la API o el store
  const id = route.params.id;
  fetch(`/api/noticias/${id}`)
    .then(response => response.json())
    .then(data => noticia.value = data)
    .catch(err => console.error(err));
});
</script>

<style scoped>
/* Estilos para la vista detallada */
</style>
