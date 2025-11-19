<script setup>
import { ref } from "vue";
import api from "../services/api";
import { useRouter } from "vue-router";

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

    mensaje.value = "Usuario registrado con éxito";
    setTimeout(() => router.push("/login"), 1000);

  } catch (error) {
    mensaje.value = "Error al registrar usuario";
  }
}
</script>

<template>
  <div style="text-align: center;">
    <h1 style="margin-bottom: 20px;">Registro</h1>

    <div style="display: flex; flex-direction: column; gap: 15px;">

      <input 
        v-model="nombre"
        placeholder="Nombre"
        style="padding: 10px; border-radius: 6px;"
      />

      <input 
        v-model="email"
        placeholder="Email"
        style="padding: 10px; border-radius: 6px;"
      />

      <input 
        v-model="password" 
        type="password" 
        placeholder="Contraseña"
        style="padding: 10px; border-radius: 6px;"
      />

      <button 
        @click="register"
        style="
          padding: 12px;
          background: #1976d2;
          border: none;
          color: white;
          border-radius: 6px;
          cursor: pointer;
          font-size: 16px;
        "
      >
        Registrarse
      </button>

      <p>{{ mensaje }}</p>

    </div>
  </div>
</template>
