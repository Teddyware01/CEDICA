import {defineStore} from "pinia"
import  axios from "axios"
export const useNoticias = defineStore('noticiasStore', {
    state:() => ({
        noticias: [],
        loading: false,
        error: null,
    }),
    actions:{
        async fetchNoticias(){
            try {
                this.loading=true
                this.error=null
                const baseUrl = import.meta.env.VITE_FLASK_API_URL;
                const response = await axios.get(`${baseUrl}/api/noticias`);
                this.noticia = response.data
            } catch (error){
                this.error = "Error al obtener las noticias"
            } finally {
                this.loading = false
            }
        }
    }
})