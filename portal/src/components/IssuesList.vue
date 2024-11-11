<template>
  <div>
    <h2>Lista de Issues</h2>
    <p v-if="loading">Cargando...</p>
    <p v-if="error">{{ error }}</p>

    <table v-if="!loading && issues.length">
      <thead>
        <tr>
          <th>#</th>
          <th>Titulo</th>
          <th>Descripcion</th>
          <th>Usuario</th>
        </tr>
      </thead>
      <tbody> 
        <tr v-for="issue in issues" :key="issue.id">
          <td>{{ issue.id }}</td>
          <td>{{ issue.title }}</td>
          <td>{{ issue.description }}</td>
          <td>{{ issue.email }}</td>
        </tr>
      </tbody>
    </table>

    <p v-if="!loading && !issues.length">No hay issues para mostrar.</p>
  </div>
</template>

<script setup>
import { useIssues } from '../stores/issues';
import { storeToRefs } from 'pinia';
import { onMounted } from 'vue';

const store = useIssues()
const { issues, loading, error } = storeToRefs(store)
const fetchIssues = async() => {
  await store.fetchIssues();
};

onMounted(() => {
  if (!issues.value.length){
    fetchIssues();
  }
})
</script>

<style scoped>


</style>