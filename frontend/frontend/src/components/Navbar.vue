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
  <v-app-bar color="primary" dark flat>
    <v-app-bar-title>Gestor de Tareas</v-app-bar-title>

    <v-spacer></v-spacer>

    <v-btn v-if="loggedIn" variant="text" @click="router.push('/tareas')">
      Tareas
    </v-btn>

    <v-btn v-if="!loggedIn" variant="text" @click="router.push('/login')">
      Login
    </v-btn>

    <v-btn v-if="!loggedIn" variant="text" @click="router.push('/register')">
      Registro
    </v-btn>

    <v-btn
      v-if="loggedIn"
      color="red"
      class="ml-4"
      variant="elevated"
      @click="logout"
    >
      Cerrar Sesión
    </v-btn>
  </v-app-bar>
</template>
