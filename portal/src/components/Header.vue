<template>
    <header @click.self="closeNav">
        <div class="left">
            <router-link to="/" class="link">
                <img alt="Logo CEDICA" class="logo" src="@/assets/cedica.jpg" width="100" height="100" title="Logo CEDICA">
            </router-link>
        </div>
        <button class="hamburger" @click.stop="toggleNav">&#9776;</button>
        <div class="nav-container" v-bind:class="{ 'open': isOpen }">
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
    name: 'Header',
    data() {
        return {
            isOpen: false
        }
    },
    methods: {
        toggleNav() {
            this.isOpen = !this.isOpen;
        },
        closeNav() {
            if (this.isOpen) {
                this.isOpen = false;
            }
        }
    },
    mounted() {
        document.addEventListener('click', (event) => {
            if (!this.$el.contains(event.target)) {
                this.closeNav();
            }
        });
    },
    beforeDestroy() {
        document.removeEventListener('click', this.closeNav);
    }
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
}

nav a {
    padding: 5px 10px;
    transition: box-shadow 0.3s ease;
}


nav a:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6);
}

.hamburger {
    display: none;  
    background: none;
    border: none;
    font-size: 30px;
    cursor: pointer;
    color: black;
}

.hamburger:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6);
}
@media (max-width: 1024px) {
    .hamburger {
        display: block;
        z-index: 100;
    }
    .nav-container {
        position: absolute;
        top: 80px;
        left: 0;
        width: 60%;
        background-color: #bbf7ff;
        box-shadow: 0 2px 5px rgba(5, 4, 4, 0.1);
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        display: none;
    }
    .nav-container.open {
        display: flex;
    }
    nav {
        flex-direction: column;
        align-items: center;
        width: 100%;
    }
    nav a {
        width: 100%;
        text-align: center;
    }
}

</style>
