<template>
    <div class="page inicio">
        <h1 class="titulo">INICIO</h1>
        <h2>
            Bienvenidos al portal de CEDICA
        </h2>
        <p>
            Tu fuente de información sobre nuestros servicios y actividades. 
            En este espacio, podrás descubrir más acerca de nuestra misión y 
            los programas que ofrecemos. Si tienes alguna consulta o necesitas
            información adicional, no dudes en contactarnos. 
            Además, asegúrate de visitar nuestra sección de noticias para estar 
            al día con las últimas novedades y eventos. 
            ¡No te pierdas la oportunidad de participar en nuestra comunidad!
        </p>
    </div>
</template>

<script>
    export default {
        name: 'Home'
    }
</script>

<style scoped>
    .inicio {
        font-family: Arial, Helvetica, sans-serif;
        margin: 0 auto;
        padding: auto 20px;
        margin-top: 60px;
        margin-bottom: 60px;
    }
    h1,h2 {
        padding-bottom: 10px;
    }

    p {
        padding-top: 10px;
        font-family: Arial, Helvetica, sans-serif;
        text-align: justify;
    }
</style>