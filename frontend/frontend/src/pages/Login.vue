<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
import { session } from "../store/session";

const email = ref("");
const password = ref("");
const mensaje = ref("");

const router = useRouter();

async function login() {
  try {
    const res = await api.post("/login", {
      email: email.value,
      password: password.value,
    });

    session.login(res.data.token);
    router.push("/tareas");
  } catch (e) {
    mensaje.value = "Credenciales incorrectas";
  }
}
</script>

<template>
  <v-container class="d-flex justify-center mt-12">
    <v-card width="420" elevation="8">
      <v-card-title class="text-h5 text-center">
        Iniciar Sesión
      </v-card-title>

      <v-card-text>
        <v-text-field
          v-model="email"
          label="Email"
          variant="outlined"
          prepend-icon="mdi-email"
          type="email"
          required
        />

        <v-text-field
          v-model="password"
          label="Contraseña"
          variant="outlined"
          prepend-icon="mdi-lock"
          type="password"
          required
        />

        <p v-if="mensaje" class="text-red text-center mt-2">{{ mensaje }}</p>
      </v-card-text>

      <v-card-actions class="d-flex flex-column">
        <v-btn
          block
          color="primary"
          class="mb-2"
          @click="login"
        >
          Entrar
        </v-btn>

        <v-btn
          block
          variant="text"
          @click="router.push('/register')"
        >
          Crear cuenta
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>
