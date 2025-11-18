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
  <div>
    <h1>Login</h1>

    <input v-model="email" placeholder="Email" />
    <br /><br />

    <input v-model="password" type="password" placeholder="Contraseña" />
    <br /><br />

    <button @click="login">Entrar</button>

    <p>{{ mensaje }}</p>
  </div>
</template>
