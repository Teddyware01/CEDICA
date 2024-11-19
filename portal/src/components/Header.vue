
<template>
    <header>
        <div class="left">
            <router-link to="/" class="link">
                <img alt="Logo CEDICA" class="logo" src="@/assets/cedica.jpg" width="100" height="100" title="Logo CEDICA">
            </router-link>
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
        z-index: 1000;
        background-color: #e0f7fa;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        padding: 0 20px;
    }
    
    .left {
        flex-shrink: 0;
        padding: 0;
    }

    .link {
        background: none;
    }


    .nav-container {
        flex-grow: 1; 
        display: flex;
        justify-content: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 25px;
    }

    nav {
        display: flex;
        gap: 10px;
    }

    .logo {
        margin-right: 10px;
        padding-top: 0;
    }

    nav a {
        padding: 5px 10px;
    }
</style>
