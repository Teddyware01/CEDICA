<template>
    <div class="page">
        <h1>CONTÁCTANOS</h1>
        <form @submit.prevent="submitForm">
            <input type="text" v-model="form.nombre" placeholder="Nombre completo" class="input" required>
            <input type="email" v-model="form.email" placeholder="Dirección de correo electrónico" class="input" required>
            <textarea v-model="form.mensaje" placeholder="Cuerpo del mensaje" class="input" required></textarea>
            <button type="submit" class="submit-button">Enviar</button>
            <div class="g-recaptcha captcha" :data-sitekey="siteKey" data-callback="onCaptchaVerified"></div>
        </form>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            form: {
                nombre: '',
                email: '',
                mensaje: ''
            },
            siteKey: '6LcD3n4qAAAAAOmTb-KAAnFAOjECmUzcHSkeM_87',
            captchaVerified: false 
        };
    },
    methods: {
        submitForm() {
            if (!this.captchaVerified) {
                alert('Por favor, completa el captcha.');
                return;
            }
            const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
            if (!emailRegex.test(this.form.email)) {
                alert('Por favor, introduce un correo electrónico válido.');
                return;
            }
            const formData = {
                nombre: this.form.nombre,
                email: this.form.email,
                mensaje: this.form.mensaje
            };

            fetch('https://grupo15.proyecto2024.linti.unlp.edu.ar/contacto/submit_form', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                alert('Mensaje enviado con éxito');
                this.resetForm();
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        
            console.log("Enviando formulario con datos:", this.form);
            alert('Mensaje enviado con éxito');
            this.resetForm();
        },
        resetForm() {
            this.form.nombre = '';
            this.form.email = '';
            this.form.mensaje = '';
            this.captchaVerified = false;
            grecaptcha.reset();
        }
    },
    mounted() {
        const script = document.createElement('script');
        script.src = 'https://www.google.com/recaptcha/api.js';
        script.async = true;
        script.defer = true;
        document.head.appendChild(script);

        window.onCaptchaVerified = () => {
            this.captchaVerified = true;
        };
    }
}
</script>

<style scoped>
h1 {
    padding-bottom: 10px;
}
</style>