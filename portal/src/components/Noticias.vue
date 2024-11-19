<template>
    <div class="page">
      <h1>LISTA DE NOTICIAS</h1>
      <p v-if="loading">Cargando noticias...</p>
      <p v-if="error">{{ error }}</p>
  
      <div v-if="!loading && noticias.length">
          <div class="contenido" v-for="noticia in noticias" :key="noticia.id">
            <h2>{{ noticia.titulo }}</h2>
            <p>{{ noticia.copete }}</p>
            <p>{{ noticia.published_at }}</p>
            <router-link :to="'/contenido/' + noticia.id">Leer</router-link>

          </div>
      </div>
      <p v-if="!loading && !noticias.length">No hay Noticias para mostrar.</p>
    </div>
  </template>
  
  <script setup>
  import { useNoticias } from '../stores/noticias';
  import { storeToRefs } from 'pinia';
  import { onMounted } from 'vue';
  
  const store = useNoticias()
  const { noticias, loading, error } = storeToRefs(store)
  const fetchNoticias = async() => {
    await store.fetchNoticias();
  };
  
  onMounted(() => {
    if (!noticias.value.length){
      fetchNoticias();
    }
  })
  </script>
  
  <style scoped>
  .contenido {
    background-color: rgba(0, 255, 255, 0.341);
    margin-top: 10px;
    margin-bottom: 10px;
    padding: 10px;
  }
  
    h1 {
      padding-top: 60px;
      padding-bottom: 10px;
  }
  
  </style>