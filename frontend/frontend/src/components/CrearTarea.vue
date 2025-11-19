<script setup>
import { ref } from "vue";
import api from "../services/api";

const titulo = ref("");
const descripcion = ref("");
const prioridad = ref("media");
const fechaLimite = ref("");
const mensaje = ref("");

async function crear() {
  try {
    await api.post("/tareas", {
      titulo: titulo.value,
      descripcion: descripcion.value,
      prioridad: prioridad.value,
      fecha_limite: fechaLimite.value
    });

    mensaje.value = "Tarea creada con éxito";

    titulo.value = "";
    descripcion.value = "";
    prioridad.value = "media";
    fechaLimite.value = "";

  } catch (error) {
    mensaje.value = error.response?.data?.error || "Error al crear tarea";
  }
}
</script>

<template>
  <div>
    <h2>Crear nueva tarea</h2>

    <input v-model="titulo" placeholder="Título de la tarea" />

    <textarea v-model="descripcion" placeholder="Descripción"></textarea>

    <label>Prioridad</label>
    <select v-model="prioridad">
      <option value="alta">Alta</option>
      <option value="media">Media</option>
      <option value="baja">Baja</option>
    </select>

    <label>Fecha límite</label>
    <input type="date" v-model="fechaLimite" />

    <button @click="crear">Crear tarea</button>

    <p>{{ mensaje }}</p>
  </div>
</template>

<style scoped>
input, textarea, select {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  border-radius: 6px;
  background: #333;
  border: none;
  color: white;
}

button {
  padding: 10px;
  width: 100%;
  border: none;
  border-radius: 6px;
  background: #4caf50;
  color: white;
  cursor: pointer;
}

label {
  display: block;
  margin-bottom: 5px;
}
</style>
