<template>
    <div class="contacto">
        <h1>Contactanos</h1>
        <form @submit.prevent="submitForm">
            <input type="text" v-model="form.name" placeholder="Nombre completo" required>
            <input type="email" v-model="form.email" placeholder="Dirección de correo electrónico" required>
            <textarea v-model="form.message" placeholder="Cuerpo del mensaje" required></textarea>
            <button type="submit" class="submit-button">Enviar</button>
            <div class="g-recaptcha captcha" :data-sitekey="siteKey" data-callback="onCaptchaVerified"></div>
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            form: {
                name: '',
                email: '',
                message: ''
            },
            siteKey: '6LcD3n4qAAAAAOmTb-KAAnFAOjECmUzcHSkeM_87',
            captchaVerified: false // Asegúrate de que esta propiedad está en tu componente
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
            console.log("Enviando formulario con datos:", this.form);
            alert('Mensaje enviado con éxito');
            this.resetForm();
        },
        resetForm() {
            this.form.name = '';
            this.form.email = '';
            this.form.message = '';
            this.captchaVerified = false; // Reset captcha verification on form reset
            grecaptcha.reset(); // Reset the reCAPTCHA widget
        },
        onCaptchaVerified() {
            this.captchaVerified = true;
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
