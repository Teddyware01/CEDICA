<template>
  <div class="page">
    <h1 class="titulo">LISTA DE NOTICIAS</h1>
    <p v-if="loading">Cargando noticias...</p>
    <p v-if="error">{{ error }}</p>

    <div v-if="!loading && noticias.length" class="noticias-container">
      <div class="contenido" v-for="noticia in noticias" :key="noticia.id">
        <h2>{{ noticia.titulo }}</h2>
        <p>{{ noticia.copete }}</p>
        <p class="fecha">{{ new Date(noticia.published_at).toLocaleDateString() }}</p>
        <router-link class="leer-mas" :to="'/contenido/' + noticia.id">Leer más</router-link>
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
  
  

.hola {
  color: red;
}


.noticias-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}

.contenido {
  background-color: var(--color-background-soft, #f0f0f0); /* Color de fondo */
  border: 2px solid var(--color-border);
  border-radius: 8px;
  padding: 20px;
  width: 100%;
  max-width: 80%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: left;
}

.contenido h2 {
  margin: 0 0 10px;
  font-size: 2em;
  color: var(--color-text);
  font-weight: bold;
}

.contenido p {
  margin: 0 0 10px;
  color: var(--color-text, #555);
}

.fecha {
  font-size: 0.9em;
  color: var(--color-muted, #888);
}

.leer-mas {
  display: inline-block;
  margin-top: 10px;
  color: var(--color-primary, #007bff);
  text-decoration: none;
  font-weight: bold;
  line-height: 1.5;
  padding: 5px 10px;
  border-radius: 8px;

}

.leer-mas:hover {
  color: var(--color-primary);
  background-color: #888;
  font-weight: bolder;

}

@media (max-width: 600px) {
  .contenido {
    padding: 15px;
  }
}
</style>
