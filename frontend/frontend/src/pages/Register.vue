<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const nombre = ref("");
const email = ref("");
const password = ref("");
const mensaje = ref("");

const router = useRouter();

async function register() {
  try {
    await api.post("/register", {
      nombre: nombre.value,
      email: email.value,
      password: password.value,
    });

    mensaje.value = "Registro exitoso. Redirigiendo…";
    setTimeout(() => router.push("/login"), 1200);

  } catch (error) {
    mensaje.value = error.response?.data?.error || "Error en el registro";
  }
}
</script>

<template>
  <v-container class="d-flex justify-center mt-12">
    <v-card width="420" elevation="8">
      <v-card-title class="text-h5 text-center">
        Crear Cuenta
      </v-card-title>

      <v-card-text>
        <v-text-field
          v-model="nombre"
          label="Nombre"
          variant="outlined"
          prepend-icon="mdi-account"
          required
        />

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
          @click="register"
        >
          Registrarse
        </v-btn>

        <v-btn
          block
          variant="text"
          @click="router.push('/login')"
        >
          Ya tengo cuenta
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>
