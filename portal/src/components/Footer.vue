<template>
    <footer>
        <div class="footer-content py-3">
            <p>SEDES
                Sede Hipódromo de La Plata (HLP)
                Calle 44 y 115 (1900) La Plata
                Sede Campo Arroyo San Juan (ASJ)
                Arturo Seguí (1895) La Plata</p>
            <p>Teléfono: 0221 506-6291</p>
            <p>Correo Electrónico: equitacionparatodos@gmail.com</p>
            <p>Proyecto de Software 2024 - Grupo 15: 
                <a href="https://gitlab.catedras.linti.unlp.edu.ar/proyecto2024/proyectos/grupo15">GitLab</a>
            </p>
        </div>
    </footer>
</template>

<script>
    export default {
        name: 'Footer'
    }
</script>

<style scoped>
    footer {
        display: flex;
        width: 100%;
        position: static;
        bottom: 0;
        left: 0;
        z-index: 1000;
        color: var(--vt-c-text-light-1);
        background-color: #e0f7fa; 
        text-align: center;
        padding: 20px 0;
        padding: 20px 0;
        margin-top: auto;
        max-width: 100%; /* O elimina esta línea */
    }

    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
    }


</style>

