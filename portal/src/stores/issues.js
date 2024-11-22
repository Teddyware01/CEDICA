import { defineStore } from 'pinia';
import axios from 'axios';


export const useIssues = defineStore('issuesStore', {
  state: () => ({
    issues: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchIssues() {
      try {
        this.loading = true;
        this.error = null;
        const baseUrl = import.meta.env.VITE_FLASK_API_URL;
        const response = await axios.get(`${baseUrl}/api/consultas`);
        this.issues = response.data;
      } catch (error) {
        this.error = "Error al obtener los issues";
      } finally {
        this.loading = false;
      }
    }
  }
});
