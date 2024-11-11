import {defineStore} from "pinia"
export const useIssues = defineStore('issues', {
    state:() => ({
        issues: [],
    }),
    actions:{
        async fetchIssues(){
            try {
                this.loading=true
                this.error=null
                this.issues = [
                    {
                        id:1,
                        tittle: "issue 1",
                        description: "description 1",
                        user: {email: "user1@example.com"},
                    },
                    {
                        id:2,
                        tittle: "issue 2",
                        description: "description 2",
                        user: {email: "user2@example.com"},
                    },
                    {
                        id:3,
                        tittle: "issue 3",
                        description: "description 3",
                        user: {email: "user3@example.com"},
                    },
                ]                
            } catch (error){
                this.error = "Error al obtener los issues"
            } finally {
                this.loading = false
            }
        }
    }
})