<template>
    <div class="contacto">
        <form @submit.prevent="submitForm">
            <input type="text" v-model="form.name" placeholder="Nombre completo" required>
            <input type="email" v-model="form.email" placeholder="Dirección de correo electrónico" required>
            <textarea v-model="form.message" placeholder="Cuerpo del mensaje" required></textarea>
            <vue-recaptcha
                ref="recaptcha"
                @verify="onCaptchaVerified"
                @expired="onCaptchaExpired"
                sitekey="tu_clave_de_sitio_publica"
            ></vue-recaptcha>
            <button type="submit">Enviar</button>
        </form>
    </div>
</template>

<script>
    import axios from 'axios';
    import VueRecaptcha from 'vue-recaptcha';
    
    export default {
        components: {
            VueRecaptcha
        },
        data() {
            return {
                form: {
                    name: '',
                    email: '',
                    message: ''
                },
                recaptchaVerified: false
            };
        },
        methods: {
            submitForm() {
                const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
                    if (!emailRegex.test(this.form.email)) {
                        alert('Por favor, introduce un correo electrónico válido.');
                        return;
                    }

                if (!this.recaptchaVerified) {
                    alert('Por favor, verifica que no eres un robot.');
                    return;
                }

                axios.post('url_del_endpoint_de_tu_API', this.form)
                .then(() => {
                    alert('Mensaje enviado con éxito');
                    this.resetForm();
                })
                .catch(error => {
                    console.error('Error al enviar el mensaje:', error);
                    alert('Error al enviar el mensaje');
                });
            },
            resetForm() {
                this.form.name = '';
                this.form.email = '';
                this.form.message = '';
                this.recaptchaVerified = false;
                this.$refs.recaptcha.reset(); // Resetea el reCAPTCHA
            },
            onCaptchaVerified(response) {
                this.recaptchaVerified = true;
            },
            onCaptchaExpired() {
                this.recaptchaVerified = false;
            }
        }
    };
</script>
