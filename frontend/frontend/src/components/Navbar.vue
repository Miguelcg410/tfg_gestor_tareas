<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { session } from "../store/session";

import Logo from "@/assets/logo/order-dragon-logo.png";
import MiniDragon from "@/assets/icons/dragon-mini.png";
import FlameBG from "@/assets/icons/flame-bg.png";

const router = useRouter();
const loggedIn = computed(() => session.token !== null);

function logout() {
  session.logout();
  router.push("/login");
}
</script>
<template>
  <v-app-bar height="70" flat class="nav-blur">
    <v-container class="d-flex align-center">

      <!-- LOGO + TEXTO -->
      <div class="logo-container" @click="$router.push('/')">
        <div class="dragon-fire-logo">
          <img :src="Logo" class="logo-img">
        </div>
        <span class="logo-text-smoke">Order Dragon</span>
      </div>

      <!-- 🔥 BOTÓN INICIO ANIMADO SIEMPRE VISIBLE -->
      <v-btn to="/" class="nav-btn nav-inicio" variant="text">
        <span class="icon-dragon-home"></span>
        Inicio
      </v-btn>

      <v-spacer />

      <template v-if="loggedIn">

        <!-- 🐉 MINI DRAGÓN ANTES DE TAREAS -->
        <div class="dragon-tareas"></div>

        <v-btn to="/tareas" class="nav-btn" variant="text">
          <v-icon left size="18">mdi-format-list-checkbox</v-icon>
          Tareas
        </v-btn>

        <v-btn to="/calendario" class="nav-btn" variant="text">
          <v-icon left size="18">mdi-calendar-month</v-icon>
          Calendario
        </v-btn>

        <v-btn
          color="red"
          variant="tonal"
          class="logout-btn"
          @click="logout"
        >
          <v-icon left size="18">mdi-logout</v-icon>
          Salir
        </v-btn>

      </template>

    </v-container>
  </v-app-bar>
</template>

<style scoped>

/* ---------------------------------------------------
   🔥 FONDO DE FUEGO REAL EN EL NAVBAR
---------------------------------------------------- */
.nav-blur {
  background: rgba(15, 15, 15, 0.92) !important;
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255,255,255,0.06);
  position: relative;
  overflow: visible;
}

.nav-blur::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image: url("@/assets/icons/flame-bg.png");
  background-size: 180% 200%;
  background-position: center 100%;
  opacity: 0.33;
  filter: blur(12px) brightness(1.4);
  pointer-events: none;
  z-index: -1;

  animation:
    flameRise 6s linear infinite,
    flameWave 3.5s ease-in-out infinite,
    flameHeat 2.2s ease-in-out infinite alternate;
}

@keyframes flameRise {
  0%   { background-position: center 100%; }
  100% { background-position: center 0%; }
}
@keyframes flameWave {
  0%   { transform: scale(1.02) skewX(1deg); }
  50%  { transform: scale(1.05) skewX(-2deg); }
  100% { transform: scale(1.02) skewX(1deg); }
}
@keyframes flameHeat {
  0%   { filter: blur(10px) brightness(1.3); }
  100% { filter: blur(14px) brightness(1.6); }
}

/* ---------------------------------------------------
   🐲 LOGO + FUEGO SUAVE
---------------------------------------------------- */
.logo-container {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.logo-img {
  width: 60px;
  height: 60px;
  object-fit: contain;
  filter: drop-shadow(0 0 6px rgba(255,120,60,0.5));
  transition: transform .25s;
}

.logo-container:hover .logo-img {
  transform: scale(1.06);
}

/* 🔥 fuego suave debajo del logo */
.dragon-fire-logo {
  position: relative;
}

.dragon-fire-logo::after {
  content: "";
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  width: 34px;
  height: 58px;

  background: radial-gradient(circle at 50% 80%,
    rgba(255,240,200,1) 10%,
    rgba(255,170,80,0.9) 40%,
    rgba(255,100,30,0.6) 60%,
    transparent 100%
  );

  filter: blur(7px);
  animation: softFire 0.22s ease-in-out infinite alternate;
}

@keyframes softFire {
  0%   { transform: translateX(-50%) scale(1); opacity: 0.7; }
  100% { transform: translateX(-50%) scale(1.25) opacity(1); }
}

/* ---------------------------------------------------
   ✨ TEXTO ANIMADO (humo + brillo)
---------------------------------------------------- */
.logo-text-smoke {
  margin-left: 10px;
  font-size: 40px;
  font-weight: 700;
  font-family: "Cinzel", serif;
  color: #ffe7cf;
  position: relative;
  animation: titleGlow 2.8s ease-in-out infinite alternate;
}

@keyframes titleGlow {
  0% { text-shadow: 0 0 6px rgba(255,150,100,0.3); }
  100% { text-shadow: 0 0 14px rgba(255,180,140,0.75); }
}

/* ---------------------------------------------------
   🔥 BOTÓN "INICIO" DRAGÓN + FUEGO
---------------------------------------------------- */
.nav-inicio {
  position: relative;
  overflow: visible;
  margin-left: 25px;
  color: #ffe8c8 !important;
  font-weight: 600;
  transition: .25s;
}

/* Mini dragón */
.icon-dragon-home {
  width: 22px;
  height: 22px;
  display: inline-block;
  margin-right: 6px;
  background-image: url("@/assets/icons/dragon-mini.png");
  background-size: contain;
  background-repeat: no-repeat;
  filter: drop-shadow(0 0 6px rgba(255,160,80,0.9));
  animation: dragonFloatMini 3s ease-in-out infinite;
}

@keyframes dragonFloatMini {
  0% { transform: translateY(0) rotate(-4deg); }
  50% { transform: translateY(-4px) rotate(3deg); }
  100% { transform: translateY(0) rotate(-4deg); }
}

/* Fuego debajo del botón */
.nav-inicio::after {
  content: "";
  position: absolute;
  bottom: -7px;
  left: 50%;
  width: 20px;
  height: 30px;
  transform: translateX(-50%);
  background: radial-gradient(circle,
    rgba(255,200,140,1) 15%,
    rgba(255,140,50,0.9) 40%,
    rgba(255,80,20,0.5) 60%,
    transparent 100%
  );
  opacity: 0;
  filter: blur(6px);
  transition: .25s;
}

.nav-inicio:hover::after {
  opacity: 1;
  transform: translateX(-50%) translateY(-3px) scale(1.2);
}

.nav-inicio:hover {
  color: white !important;
  text-shadow: 0 0 12px rgba(255,200,120,0.9);
  transform: translateY(-2px);
}

/* ---------------------------------------------------
   🐉 MINI DRAGÓN FLOTANTE ANTES DE TAREAS
---------------------------------------------------- */
.dragon-tareas {
  width: 40px;
  height: 40px;
  margin-right: 6px;
  background-image: url("@/assets/icons/dragon-mini.png");
  background-size: contain;
  background-repeat: no-repeat;
  filter: drop-shadow(0 0 6px rgba(255,120,50,0.8));
  animation: dragonFloat 3s ease-in-out infinite;
}

@keyframes dragonFloat {
  0% { transform: translateY(0px) rotate(-4deg); }
  50% { transform: translateY(-5px) rotate(4deg); }
  100% { transform: translateY(0px) rotate(-4deg); }
}

/* ---------------------------------------------------
   BOTONES
---------------------------------------------------- */
.nav-btn {
  color: #dcdcdc !important;
  font-weight: 500;
  margin-right: 10px;
  text-transform: none;
  transition: .25s;
}

.nav-btn:hover {
  color: white !important;
  transform: translateY(-2px);
}

.logout-btn {
  margin-left: 10px;
  font-weight: 600;
  text-transform: none;
  color: white;
}

</style>
