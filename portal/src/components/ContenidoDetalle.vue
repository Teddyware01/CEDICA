<template>
  <div class="noticia page">
    <h1 class="titulo">{{ noticia.titulo }}</h1>
    <p class="copete">{{ noticia.copete }}</p>
    <div class="recuadro">
      <p>{{ noticia.contenido }}</p>
      <div class="recuadro">
        <p class="fecha">Publicado el: {{ new Date(noticia.published_at).toLocaleDateString() }}</p>
        <p class="author">Por el autor: {{ noticia.autor }}</p>
        <p class="tipo">Tipo de publicación: {{ noticia.tipo }}</p>
        <p class="estado">Estado: {{ noticia.estado }}</p>
      </div>
    </div>
    <router-link class="volver" to="/noticias">Volver</router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const noticia = ref({});

onMounted(() => {
  const id = route.params.id;
  const baseUrl = import.meta.env.VITE_FLASK_API_URL;
  fetch(`${baseUrl}/api/contenido/id/${id}`)
    .then(response => response.json())
    .then(data => noticia.value = data)
    .catch(err => console.error(err));
});
</script>

<style scoped>

.noticia  {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  max-width: 100%;
  margin: 0 auto;
}

.titulo {
  font-size: 2.5em;
  color: var(--color-text, #333);
  font-weight: bold;
  margin-bottom: 15px;
}

.copete {
  font-size: 1.2em;
  color: var(--color-muted, #555);
  margin-bottom: 20px;
}

.recuadro {
  background-color: var(--color-background-soft);
  border-radius: 10px;
  padding: 50px 60px;
  text-align: justify;
  width: 100%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.recuadro p {
  margin-bottom: 10px;
  color: var(--color-text, #444);
}

.fecha,
.author,
.tipo,
.estado {
  font-size: 0.9em;
  color: var(--color-muted, #888);
}

.volver {
  margin-top: 20px;
  display: inline-block;
  padding: 10px 20px;
  background-color: var(--color-primary, #007bff);
  color: white;
  font-weight: bold;
  text-decoration: none;
  border-radius: 5px;
}

.volver:hover {
  background-color: var(--color-primary-dark, #0056b3);
  cursor: pointer;
}

@media (max-width: 600px) {
  .titulo {
    font-size: 2em;
  }

  .copete {
    font-size: 1.1em;
  }

  .recuadro {
    padding: 15px;
  }

  .volver {
    padding: 8px 15px;
  }
}
</style>
