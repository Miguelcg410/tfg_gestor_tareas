<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { session } from "../store/session";

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

      <!-- LOGO -->
      <div class="d-flex align-center cursor-pointer" @click="$router.push('/tareas')">
        <v-icon size="32" color="primary">mdi-check-circle</v-icon>
        <span class="logo-text ml-3">Task Manager Pro</span>
      </div>

      <v-spacer />

      <!-- SOLO LOGUEADO -->
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
/* Fondo moderno con blur */
.nav-blur {
  background: rgba(30, 30, 30, 0.75) !important;
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

/* Logo */
.logo-text {
  font-size: 22px;
  font-weight: 700;
  color: white;
}

/* Botones de navegación */
.nav-btn {
  color: #cfcfcf !important;
  font-weight: 500;
  margin-right: 8px;
  text-transform: none;
  letter-spacing: .3px;
  transition: 0.25s ease;
}

.nav-btn:hover {
  color: white !important;
  transform: translateY(-1px);
}

/* Botón de logout */
.logout-btn {
  margin-left: 10px;
  font-weight: 600;
  color: white;
  text-transform: none;
}

.cursor-pointer {
  cursor: pointer;
}
</style>
