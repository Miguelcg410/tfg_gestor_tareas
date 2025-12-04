<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const nombre = ref("");
const email = ref("");
const password = ref("");
const mensaje = ref("");
const loading = ref(false);

const router = useRouter();

async function register() {

  // VALIDACIÓN BÁSICA (evita errores)
  if (!nombre.value || !email.value || !password.value) {
    mensaje.value = "Completa todos los campos.";
    return;
  }

  loading.value = true;
  mensaje.value = "";

  try {
    // 👈 CAMBIO IMPORTANTE: el backend espera "name"
    await api.post("/register", {
    nombre: nombre.value,   // 👈 el backend quiere “nombre”
    email: email.value,
    password: password.value,
});


    mensaje.value = "🔥 Registro exitoso. Redirigiendo…";

    setTimeout(() => {
      router.push("/login");
    }, 1200);

  } catch (error) {
    mensaje.value =
      error.response?.data?.error ||
      "❌ No se pudo registrar el usuario.";
  } finally {
    loading.value = false;
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

        <!-- Nombre -->
        <v-text-field
          v-model="nombre"
          label="Nombre"
          prepend-icon="mdi-account"
          variant="outlined"
          required
        />

        <!-- Email -->
        <v-text-field
          v-model="email"
          label="Email"
          prepend-icon="mdi-email"
          type="email"
          variant="outlined"
          required
        />

        <!-- Contraseña -->
        <v-text-field
          v-model="password"
          label="Contraseña"
          prepend-icon="mdi-lock"
          type="password"
          variant="outlined"
          required
        />

        <!-- Mensaje -->
        <p
          v-if="mensaje"
          class="text-center mt-2"
          :style="{ color: mensaje.includes('🔥') ? 'green' : 'red' }"
        >
          {{ mensaje }}
        </p>

      </v-card-text>

      <v-card-actions class="d-flex flex-column">

        <!-- Botón registrar -->
        <v-btn
          block
          color="orange-darken-2"
          class="mb-2"
          :loading="loading"
          @click="register"
        >
          Registrarse
        </v-btn>

        <!-- Volver -->
        <v-btn block variant="text" @click="router.push('/login')">
          Ya tengo cuenta
        </v-btn>

      </v-card-actions>

    </v-card>
  </v-container>
</template>
