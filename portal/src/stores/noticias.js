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
                const response = await axios.get("http://localhost:5000/api/contenido")  //cambiar esto para que deje de estar hardcodead (separar dev de deploy):
                this.noticias = response.data
            } catch (error){
                this.error = "Error al obtener las noticias"
            } finally {
                this.loading = false
            }
        }
    }
})