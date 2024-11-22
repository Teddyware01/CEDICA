<template>
  <div id="app">
    <Header />
    <router-view/>
    <Footer />
  </div>
</template>

<script setup>
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import { useHead } from '@vueuse/head';

  useHead({
    link: [
      { rel: 'icon', href: '/cedica_icon.png' },
    ],
  });
</script>
