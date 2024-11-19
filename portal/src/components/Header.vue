
<template>
    <header>
        <div class="left">
            <img alt="Logo CEDICA" class="logo" src="@/assets/cedica.jpg" width="100" height="100">
        </div>
        <div class="nav-container">
            <nav>
                <router-link to="/">Inicio</router-link>
                <router-link to="/contacto">Contáctanos</router-link>
                <router-link to="/noticias">Act. y noticias</router-link>
                <router-link to="/about">Sobre nosotros</router-link>
            </nav>
        </div>
    </header>
</template>

<script>
    export default {
        name: 'Header'
    }
</script>

<style scoped>
    header {
        display: flex;
        align-items: center;
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        background-color: white;
        z-index: 1000;
        padding: 10px 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    .left {
        flex-shrink: 0;
    }

    .nav-container {
        flex-grow: 1; 
        display: flex;
        justify-content: center;
    }

    nav {
        display: flex;
        gap: 10px;
    }

    .logo {
        margin-right: 10px; 
    }
</style>
