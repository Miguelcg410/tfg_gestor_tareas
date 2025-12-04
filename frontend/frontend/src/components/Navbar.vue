<script setup>
import { computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { session } from "../store/session";

// Assets
import Logo from "@/assets/logo/order-dragon-logo.png";
import FlameIcon from "@/assets/icons/flame-icon.png";
import MiniDragon from "@/assets/icons/dragon-mini.png";
import FlameBG from "@/assets/icons/flame-bg.png";

const router = useRouter();
const route = useRoute();
const loggedIn = computed(() => session.token !== null);

function logout() {
  session.logout();
  router.push("/login");
}

// Helper para saber si una ruta está activa
const isActive = (path) => route.path === path;
</script>

<template>
  <v-app-bar height="70" flat class="nav-blur">
    <div class="navbar-layout">

      <!-- IZQUIERDA — LOGO -->
      <div class="nav-left">
        <div class="logo-container" @click="$router.push('/')">
          <div class="dragon-fire-logo">
            <img :src="Logo" class="logo-img" />
          </div>
          <span class="logo-text-smoke">Order Dragon</span>
        </div>
      </div>

      <!-- CENTRO — INICIO CENTRADO -->
      <div class="nav-center">
        <v-btn 
          to="/" 
          class="nav-btn nav-inicio" 
          :class="{ active: isActive('/') }"
          variant="text"
        >
          <span class="icon-flame"></span>
          <span class="btn-text">Inicio</span>
          <span class="fire-trail"></span>
        </v-btn>
      </div>

      <!-- DERECHA — TAREAS / CALENDARIO / SALIR -->
      <div class="nav-right" v-if="loggedIn">
        <v-btn 
          to="/tareas" 
          class="nav-btn nav-side"
          :class="{ active: isActive('/tareas') }"
          variant="text"
        >
          <v-icon left size="20">mdi-format-list-checkbox</v-icon>
          <span class="btn-text">Tareas</span>
        </v-btn>

        <v-btn 
          to="/calendario" 
          class="nav-btn nav-side"
          :class="{ active: isActive('/calendario') }"
          variant="text"
        >
          <v-icon left size="20">mdi-calendar-month</v-icon>
          <span class="btn-text">Calendario</span>
        </v-btn>

        <v-btn 
          color="red" 
          variant="tonal" 
          class="logout-btn" 
          @click="logout"
        >
          <v-icon left size="20">mdi-fire</v-icon>
          <span class="btn-text">Salir</span>
        </v-btn>
      </div>

    </div>
  </v-app-bar>
</template>

<style scoped>
/* ========== GRID PARA CENTRAR INICIO ========== */
.navbar-layout {
  width: 100%;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  padding: 0 30px;
  position: relative;
}

.nav-left {
  justify-self: start;
}

.nav-center {
  justify-self: center;
}

.nav-right {
  justify-self: end;
  display: flex;
  align-items: center;
  gap: 12px;
}

/* ========== NAVBAR FONDO FUEGO ========== */
.nav-blur {
  background: rgba(15, 15, 15, 0.95) !important;
  backdrop-filter: blur(16px) saturate(1.2);
  border-bottom: 2px solid rgba(255, 170, 80, 0.15);
  position: relative;
  overflow: visible;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.nav-blur::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image: url("@/assets/icons/flame-bg.png");
  background-size: 200% 220%;
  background-position: center 100%;
  opacity: 0.35;
  filter: blur(14px) brightness(1.4);
  pointer-events: none;
  z-index: -1;

  animation:
    flameRise 7s linear infinite,
    flameWave 4s ease-in-out infinite;
}

@keyframes flameRise {
  0%   { background-position: center 100%; }
  100% { background-position: center 0%; }
}

@keyframes flameWave {
  0%   { transform: scale(1.02); }
  50%  { transform: scale(1.06); }
  100% { transform: scale(1.02); }
}

/* ========== LOGO ========== */
.logo-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
}

.logo-container:hover {
  transform: scale(1.05);
}

.logo-img {
  width: 60px;
  height: 60px;
  object-fit: contain;
  filter: drop-shadow(0 0 8px rgba(255, 120, 60, 0.6));
  transition: all 0.3s ease;
}

.logo-container:hover .logo-img {
  filter: drop-shadow(0 0 15px rgba(255, 140, 70, 0.9));
  animation: logoPulse 0.6s ease;
}

@keyframes logoPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.dragon-fire-logo {
  position: relative;
}

.dragon-fire-logo::after {
  content: "";
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 36px;
  height: 60px;

  background: radial-gradient(circle,
    rgba(255, 240, 200, 1) 10%,
    rgba(255, 170, 80, 0.95) 40%,
    rgba(255, 100, 30, 0.65) 60%, 
    transparent 100%
  );

  filter: blur(8px);
  animation: softFire 0.22s ease-in-out infinite alternate;
}

@keyframes softFire {
  0%   { transform: translateX(-50%) scale(1); opacity: 0.7; }
  100% { transform: translateX(-50%) scale(1.3); opacity: 1; }
}

.logo-text-smoke {
  margin-left: 12px;
  font-size: 40px;
  font-weight: 700;
  font-family: "Cinzel", serif;
  color: #ffe7cf;
  text-shadow: 
    0 0 15px rgba(255, 170, 80, 0.6),
    0 2px 4px rgba(0, 0, 0, 0.5);
  letter-spacing: 1px;
  transition: all 0.3s ease;
}

.logo-container:hover .logo-text-smoke {
  color: #fff5e6;
  text-shadow: 
    0 0 25px rgba(255, 170, 80, 0.9),
    0 2px 6px rgba(0, 0, 0, 0.6);
}

/* ========== BOTÓN INICIO (CENTRADO) - ÉPICO ========== */
.nav-inicio {
  position: relative;
  font-size: 26px !important;
  font-weight: 800 !important;
  color: #ffe8c8 !important;
  text-shadow: 
    0 0 15px rgba(255, 170, 80, 0.9),
    0 0 30px rgba(255, 140, 60, 0.5);
  letter-spacing: 2px;
  padding: 12px 32px !important;
  border-radius: 16px;
  font-family: "Cinzel", serif;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: visible;
}

.nav-inicio::before {
  content: "";
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, 
    rgba(255, 170, 80, 0.2),
    rgba(255, 120, 50, 0.2),
    rgba(255, 170, 80, 0.2)
  );
  border-radius: 16px;
  opacity: 0;
  transition: opacity 0.4s ease;
  z-index: -1;
}

.nav-inicio:hover::before {
  opacity: 1;
  animation: borderPulse 1.5s ease infinite;
}

@keyframes borderPulse {
  0%, 100% { 
    transform: scale(1);
    opacity: 0.6;
  }
  50% { 
    transform: scale(1.05);
    opacity: 1;
  }
}

.nav-inicio.active {
  background: rgba(255, 170, 80, 0.15) !important;
  border: 2px solid rgba(255, 170, 80, 0.4);
}

.icon-flame {
  width: 30px;
  height: 30px;
  display: inline-block;
  margin-right: 10px;
  background-image: url("@/assets/icons/flame-icon.png");
  background-size: contain;
  background-repeat: no-repeat;
  animation: flameFloat 2.5s ease-in-out infinite;
  filter: drop-shadow(0 0 8px rgba(255, 170, 80, 0.7));
}

@keyframes flameFloat {
  0% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-6px) scale(1.12); }
  100% { transform: translateY(0) scale(1); }
}

.nav-inicio:hover .icon-flame {
  animation: flameIntense 0.4s ease infinite;
}

@keyframes flameIntense {
  0%, 100% { transform: translateY(0) scale(1) rotate(0deg); }
  25% { transform: translateY(-3px) scale(1.15) rotate(-5deg); }
  75% { transform: translateY(-3px) scale(1.15) rotate(5deg); }
}

/* Efecto de fuego debajo */
.nav-inicio::after {
  content: "";
  position: absolute;
  bottom: -15px;
  left: 50%;
  width: 60px;
  height: 60px;
  transform: translateX(-50%);
  opacity: 0;
  background: radial-gradient(circle,
    rgba(255, 255, 180, 1) 0%,
    rgba(255, 160, 60, 0.95) 30%,
    rgba(255, 80, 20, 0.7) 60%,
    transparent 95%
  );
  filter: blur(10px);
  transition: all 0.4s ease;
  pointer-events: none;
}

.nav-inicio:hover::after {
  opacity: 1;
  transform: translateX(-50%) translateY(-6px) scale(1.4);
  animation: fireFlicker 0.3s ease infinite;
}

@keyframes fireFlicker {
  0%, 100% { opacity: 0.9; }
  50% { opacity: 1; }
}

/* Trail de fuego */
.fire-trail {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  transform: translate(-50%, -50%);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.4s ease;
}

.nav-inicio:hover .fire-trail {
  opacity: 0.3;
  animation: trailExpand 0.6s ease-out;
}

@keyframes trailExpand {
  from {
    box-shadow: 0 0 20px 5px rgba(255, 170, 80, 0.8);
    transform: translate(-50%, -50%) scale(0.9);
  }
  to {
    box-shadow: 0 0 60px 20px rgba(255, 170, 80, 0);
    transform: translate(-50%, -50%) scale(1.5);
  }
}

/* ========== BOTONES LATERALES ========== */
.nav-side {
  color: #dcdcdc !important;
  text-transform: none;
  font-size: 16px !important;
  font-weight: 600 !important;
  padding: 10px 20px !important;
  border-radius: 12px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  font-family: "Cinzel", serif;
  letter-spacing: 0.5px;
}

.nav-side::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 170, 80, 0.2);
  transform: translate(-50%, -50%);
  transition: width 0.4s ease, height 0.4s ease;
}

.nav-side:hover::before {
  width: 200%;
  height: 200%;
}

.nav-side:hover {
  color: #ffe8c8 !important;
  background: rgba(255, 170, 80, 0.1) !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 170, 80, 0.2);
}

.nav-side.active {
  color: #ffcc88 !important;
  background: rgba(255, 170, 80, 0.15) !important;
  border: 1px solid rgba(255, 170, 80, 0.3);
  box-shadow: 0 0 15px rgba(255, 170, 80, 0.3);
}

.nav-side:hover .v-icon {
  animation: iconBounce 0.5s ease;
}

@keyframes iconBounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

/* ========== BOTÓN SALIR ========== */
.logout-btn {
  background: linear-gradient(135deg, 
    rgba(220, 38, 38, 0.8) 0%, 
    rgba(153, 27, 27, 0.8) 100%
  ) !important;
  color: white !important;
  font-weight: 700 !important;
  font-size: 16px !important;
  padding: 10px 24px !important;
  border-radius: 12px;
  margin-left: 12px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  font-family: "Cinzel", serif;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

.logout-btn::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.4s ease, height 0.4s ease;
}

.logout-btn:hover::before {
  width: 300%;
  height: 300%;
}

.logout-btn:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 
    0 6px 20px rgba(220, 38, 38, 0.5),
    0 0 30px rgba(255, 100, 100, 0.3);
  background: linear-gradient(135deg, 
    rgba(239, 68, 68, 0.9) 0%, 
    rgba(185, 28, 28, 0.9) 100%
  ) !important;
}

.logout-btn:active {
  transform: translateY(-1px) scale(1.02);
}

.logout-btn .v-icon {
  filter: drop-shadow(0 0 4px rgba(255, 200, 100, 0.6));
}

/* ========== TEXTO BOTONES ========== */
.btn-text {
  position: relative;
  z-index: 1;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 960px) {
  .navbar-layout {
    padding: 0 16px;
  }

  .logo-text-smoke {
    font-size: 32px;
  }
  
  .nav-inicio {
    font-size: 22px !important;
    padding: 10px 24px !important;
  }

  .icon-flame {
    width: 24px;
    height: 24px;
  }
  
  .nav-right {
    gap: 8px;
  }
  
  .nav-side {
    font-size: 14px !important;
    padding: 8px 16px !important;
  }

  .logout-btn {
    font-size: 14px !important;
    padding: 8px 18px !important;
  }
}

@media (max-width: 600px) {
  .navbar-layout {
    grid-template-columns: auto 1fr;
    padding: 0 10px;
  }

  .logo-text-smoke {
    font-size: 24px;
  }
  
  .nav-center {
    display: none;
  }
  
  .nav-right {
    gap: 4px;
  }

  .nav-side .btn-text,
  .logout-btn .btn-text {
    display: none;
  }

  .nav-side,
  .logout-btn {
    padding: 8px 12px !important;
  }
}
</style>