<template>
    <div>
      <h2>Lista de Noticias</h2>
      <p v-if="loading">Cargando noticias...</p>
      <p v-if="error">{{ error }}</p>
  
      <div v-if="!loading && noticias.length">
          <div v-for="noticia in noticias" :key="noticia.id">
            <h1>{{ noticia.titulo }}</h1>
            <p>{{ noticia.contenido }}</p>
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
  
  
  </style>