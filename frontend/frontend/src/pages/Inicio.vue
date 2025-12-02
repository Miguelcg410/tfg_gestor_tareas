<script setup>
import { useRouter } from "vue-router";
import FlameBG from "@/assets/icons/flame-bg.png";
import DragonSilhouette from "@/assets/backgrounds/dragon-bg.jpg"; 
// ⭐ Usa aquí la imagen 2 de fondo que tienes guardada
// Si tiene otro nombre, cámbialo arriba

const router = useRouter();

function entrar() {
  router.push("/tareas");
}
</script>

<template>
  <div class="home-wrapper">

    <!-- 🔥 FONDO PRINCIPAL (DRAGÓN + OSCURIDAD) -->
    <div class="home-bg"></div>

    <!-- 🔥 FUEGO ANIMADO SUPERPUESTO -->
    <div class="fire-overlay"></div>

    <!-- ✨ PARTÍCULAS / BRASAS -->
    <div class="particle-layer"></div>

    <!-- CONTENIDO -->
    <div class="hero-content">
      <h1 class="hero-title">Order Dragon</h1>
      <p class="hero-sub">Organiza tu vida con fuego, poder y precisión.</p>

      <button class="hero-btn" @click="entrar">
        Entrar
      </button>
    </div>

  </div>
</template>

<style scoped>

/* ================================
   🐉 CONTENEDOR GENERAL
================================ */
.home-wrapper {
  width: 100%;
  height: calc(100vh - 70px);
  position: relative;
  overflow: hidden;
  background: black;
}

/* ================================
   🐉 FONDO CON DRAGÓN – Cinematic
================================ */
.home-bg {
  position: absolute;
  inset: 0;
  background-image: url("@/assets/backgrounds/dragon-bg.jpg");
  background-size: cover;
  background-position: center;
  opacity: 0.55;
  filter: brightness(0.6) contrast(1.15);
  animation: bgMove 24s ease-in-out infinite alternate;
}

@keyframes bgMove {
  0% { transform: scale(1); }
  100% { transform: scale(1.08); }
}

/* ================================
   🔥 CAPA DE FUEGO ANIMADO (Estilo imagen 2)
================================ */
.fire-overlay {
  position: absolute;
  inset: 0;
  background-image: url("@/assets/icons/flame-bg.png");
  background-size: cover;
  background-position: bottom;
  opacity: 0.35;
  mix-blend-mode: screen;

  /* 🔥 movimiento sutil del fuego */
  animation: fireMove 2.2s ease-in-out infinite alternate;
}

@keyframes fireMove {
  0% { transform: translateY(0) scale(1); opacity: 0.3; }
  100% { transform: translateY(-14px) scale(1.05); opacity: 0.4; }
}

/* ================================
   ✨ PARTÍCULAS / BRASAS
================================ */
.particle-layer {
  pointer-events: none;
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, rgba(255, 120, 40, 0.45) 2px, transparent 2px);
  background-size: 8px 8px;
  opacity: 0.15;
  animation: particleFloat 6s ease-in-out infinite alternate;
}

@keyframes particleFloat {
  0% { transform: translateY(0) scale(1); opacity: 0.1; }
  100% { transform: translateY(-25px) scale(1.1); opacity: 0.25; }
}

/* ================================
   🎬 HERO CONTENT (Texto estilo Imagen 3)
================================ */
.hero-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  z-index: 20;
}

/* TÍTULO CINEMÁTICO */
.hero-title {
  font-size: 88px;
  font-weight: 800;
  font-family: "Cinzel", serif;
  color: #ffe7c8;
  text-shadow: 0 0 18px rgba(255,140,80,0.9),
               0 0 35px rgba(255,80,20,0.45);

  animation: titleGlow 3s ease-in-out infinite alternate;
}

@keyframes titleGlow {
  0% { text-shadow: 0 0 12px rgba(255,130,70,0.55); }
  100% { text-shadow: 0 0 26px rgba(255,180,120,0.95); }
}

/* SUBTÍTULO */
.hero-sub {
  font-size: 22px;
  color: #ffe7d0;
  opacity: 0.8;
  margin-top: -10px;
  margin-bottom: 30px;
  letter-spacing: 1px;
  animation: subtGlow 4s ease-in-out infinite alternate;
}

@keyframes subtGlow {
  0% { opacity: 0.75; }
  100% { opacity: 1; }
}

/* BOTÓN */
.hero-btn {
  padding: 14px 34px;
  font-size: 20px;
  font-family: "Cinzel", serif;
  font-weight: 700;

  background: linear-gradient(90deg, #ff621a, #ff9b3d);
  border: none;
  border-radius: 12px;

  color: #fff;
  cursor: pointer;
  transition: 0.25s ease-in-out;

  box-shadow: 0 0 12px rgba(255,100,50,0.6);
}

.hero-btn:hover {
  transform: scale(1.08);
  box-shadow: 0 0 25px rgba(255,120,40,1);
  filter: brightness(1.15);
}

.hero-btn:active {
  transform: scale(0.96);
}

</style>
