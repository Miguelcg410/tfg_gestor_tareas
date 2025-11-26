<template>
  <div v-if="visible" class="splash-container">
    <div class="glow-wrapper">
      <img :src="logo" alt="Order Dragon Logo" class="logo" />
    </div>

    <h1 class="title">ORDER DRAGON</h1>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import logo from "@/assets/logo_dark.png"; // CAMBIA AQUÍ según nombre del archivo

const visible = ref(true);

onMounted(() => {
  setTimeout(() => {
    visible.value = false;
  }, 2200); // Duración splash
});
</script>

<style scoped>
.splash-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: #0b0b0b;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 99999;
  animation: fadeOut 0.6s ease forwards;
  animation-delay: 2s;
}

/* LOGO */
.logo {
  width: 180px;
  height: auto;
  animation: glow 2s ease-in-out infinite alternate,
             appear 1.2s ease forwards;
  opacity: 0;
}

/* Animación del brillo */
@keyframes glow {
  from {
    filter: drop-shadow(0 0 2px #ff3b30)
            drop-shadow(0 0 4px #b3140e)
            drop-shadow(0 0 8px #5a0000);
  }
  to {
    filter: drop-shadow(0 0 8px #ff6a4d)
            drop-shadow(0 0 16px #d42010)
            drop-shadow(0 0 28px #7a0000);
  }
}

/* Aparición inicial */
@keyframes appear {
  from {
    transform: scale(0.8);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

/* Texto */
.title {
  margin-top: 20px;
  font-size: 28px;
  letter-spacing: 4px;
  font-family: "Cinzel", serif;
  color: #ffffff;
  animation: appear 1.5s ease forwards;
  opacity: 0;
}

/* Desaparición del splash */
@keyframes fadeOut {
  to {
    opacity: 0;
    visibility: hidden;
  }
}
</style>
