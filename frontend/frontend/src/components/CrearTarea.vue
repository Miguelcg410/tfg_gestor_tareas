<script setup>
import { ref } from "vue";
import api from "../services/api";

const titulo = ref("");
const descripcion = ref("");
const mensaje = ref("");

async function crearTarea() {
  try {
    await api.post("/tareas", {
      titulo: titulo.value,
      descripcion: descripcion.value
    });

    mensaje.value = "Tarea creada con éxito";

    // limpiar campos
    titulo.value = "";
    descripcion.value = "";

  } catch (error) {
    mensaje.value = error.response?.data?.error || "Error creando tarea";
  }
}
</script>

<template>
  <div style="margin-top: 20px;">
    <h2>Crear nueva tarea</h2>

    <input v-model="titulo" placeholder="Título de la tarea" /><br /><br />
    <textarea v-model="descripcion" placeholder="Descripción"></textarea><br /><br />

    <button @click="crearTarea">Crear tarea</button>

    <p>{{ mensaje }}</p>
  </div>
</template>
