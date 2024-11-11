import {defineStore} from "pinia"
import  axios from "axios"
export const useIssues = defineStore('issuesStore', {
    state:() => ({
        issues: [],
        loading: false,
        error: null,
    }),
    actions:{
        async fetchIssues(){
            try {
                this.loading=true
                this.error=null
                const response = await axios.get("http://localhost:5000/api/consultas")  //cambiar esto para que deje de estar hardcodead (separar dev de deploy):
                this.issues = response.data
            } catch (error){
                this.error = "Error al obtener los issues"
            } finally {
                this.loading = false
            }
        }
    }
})