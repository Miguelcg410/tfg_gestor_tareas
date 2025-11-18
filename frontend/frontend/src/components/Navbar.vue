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
  <nav
    style="
      background: #222;
      padding: 15px;
      display: flex;
      justify-content: center;
      gap: 20px;
      color: white;
      font-size: 18px;
    "
  >
    <!-- Si NO está logueado -->
    <template v-if="!loggedIn">
      <router-link to="/login" style="color: white;">Login</router-link>
      <router-link to="/register" style="color: white;">Registro</router-link>
    </template>

    <!-- Si está logueado -->
    <template v-else>
      <router-link to="/tareas" style="color: white;">Tareas</router-link>
      <button
        @click="logout"
        style="background: none; border: none; color: white; cursor: pointer;"
      >
        Cerrar sesión
      </button>
    </template>
  </nav>
</template>
