<script setup>
import { ref } from "vue";
import api from "../services/api";

const nombre = ref("");
const email = ref("");
const password = ref("");
const mensaje = ref("");

async function registrar() {
  try {
    await api.post("/register", {
      nombre: nombre.value,
      email: email.value,
      password: password.value
    });

    mensaje.value = "Usuario registrado con éxito";

  } catch (error) {
    mensaje.value = error.response?.data?.error || "Error registrando usuario";
  }
}
</script>

<template>
  <div style="margin-top: 20px;">
    <h2>Registro</h2>

    <input v-model="nombre" placeholder="Nombre" /><br /><br />
    <input v-model="email" placeholder="Email" /><br /><br />
    <input v-model="password" type="password" placeholder="Contraseña" /><br /><br />

    <button @click="registrar">Registrarse</button>

    <p>{{ mensaje }}</p>
  </div>
</template>
