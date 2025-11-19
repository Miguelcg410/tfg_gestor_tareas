<script setup>
import { ref } from "vue";
import api from "../services/api";
import { useRouter } from "vue-router";
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

    session.login(res.data.token); // Guardar token en store
    mensaje.value = "Inicio de sesión correcto";

    router.push("/tareas"); // Redirigir
  } catch (error) {
    mensaje.value = "Credenciales incorrectas";
  }
}
</script>

<template>
  <div style="text-align: center;">
    <h1 style="margin-bottom: 20px;">Iniciar sesión</h1>

    <div style="display: flex; flex-direction: column; gap: 15px;">

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
        @click="login"
        style="
          padding: 12px;
          background: #4caf50;
          border: none;
          color: white;
          border-radius: 6px;
          cursor: pointer;
          font-size: 16px;
        "
      >
        Entrar
      </button>

      <p>{{ mensaje }}</p>

    </div>
  </div>
</template>
