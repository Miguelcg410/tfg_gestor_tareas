<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { session } from "../store/session";

// Importamos el logo sin fondo
import Logo from "@/assets/logo/order-dragon-logo.png";

const router = useRouter();
const loggedIn = computed(() => session.token !== null);

function logout() {
  session.logout();
  router.push("/login");
}
</script>

<template>
  <v-app-bar
    height="70"
    flat
    class="nav-blur"
  >
    <v-container class="d-flex align-center">

      <!-- LOGO + NOMBRE -->
      <div class="logo-container" @click="$router.push('/tareas')">
        <img :src="Logo" alt="Order Dragon Logo" class="logo-img" />
        <span class="logo-text">Order Dragon</span>
      </div>

      <v-spacer />

      <!-- SOLO SI ESTÁ LOGUEADO -->
      <template v-if="loggedIn">

        <v-btn
          to="/tareas"
          class="nav-btn"
          variant="text"
        >
          <v-icon left size="18">mdi-format-list-checkbox</v-icon>
          Tareas
        </v-btn>

        <v-btn
          to="/calendario"
          class="nav-btn"
          variant="text"
        >
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
/* ---- NAVBAR ---- */
.nav-blur {
  background: rgba(30, 30, 30, 0.75) !important;
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

/* ---- LOGO Y TEXTO ---- */
.logo-container {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.logo-img {
  width: 62px;
  height: 62px;
  object-fit: contain;
  image-rendering: high-quality;
  filter: drop-shadow(0 0 3px rgba(255, 80, 80, 0.35));
  transition: transform 0.25s ease;
}

.logo-container:hover .logo-img {
  transform: scale(1.07);
}

.logo-text {
  font-size: 50px;
  font-weight: 750;
  margin-left: 10px;
  color: #ffdddd;
  letter-spacing: 1px;
  font-family: "Cinzel", serif; /* Opción medieval premium */
}

/* ---- BOTONES ---- */
.nav-btn {
  color: #cfcfcf !important;
  font-weight: 500;
  margin-right: 10px;
  text-transform: none;
  letter-spacing: .3px;
  transition: 0.25s ease;
}

.nav-btn:hover {
  color: white !important;
  transform: translateY(-1px);
}

/* ---- BOTÓN SALIR ---- */
.logout-btn {
  margin-left: 10px;
  font-weight: 600;
  text-transform: none;
  color: white;
}
</style>
