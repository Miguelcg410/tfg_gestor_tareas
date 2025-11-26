<script setup>
import { ref, onMounted } from "vue";
import SplashScreen from "./components/SplashScreen.vue";
import Navbar from "./components/Navbar.vue";

const loaded = ref(false);

onMounted(() => {
  setTimeout(() => {
    loaded.value = true;
  }, 2000);
});
</script>

<template>
  <v-app>
    <!-- Splash SOLO mientras loaded es false -->
    <SplashScreen v-if="!loaded" />
    
    <!-- App completa cuando loaded es true -->
    <template v-else>
      <Navbar />
      <v-main>
        <router-view />
      </v-main>
    </template>
  </v-app>
</template>

<style>
html, body {
  background: #0b0b0b;
  margin: 0;
  padding: 0;
}
</style>