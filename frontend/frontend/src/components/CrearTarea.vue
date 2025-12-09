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
      fecha_limite: fechaLimite.value || null,
    });

    mensaje.value = "Tarea creada con éxito";

    titulo.value = "";
    descripcion.value = "";
    prioridad.value = "media";
    fechaLimite.value = "";
  } catch (e) {
    mensaje.value = "Error al crear tarea";
  }
}
</script>

<template>
  <v-card class="pa-4 mt-4" elevation="8">
    <v-card-title class="text-h6">
      Crear nueva tarea
    </v-card-title>

    <v-card-text>
      <v-text-field
        v-model="titulo"
        label="Título"
        prepend-icon="mdi-format-title"
        variant="outlined"
        required
      />

      <v-textarea
        v-model="descripcion"
        label="Descripción"
        prepend-icon="mdi-text"
        variant="outlined"
      />

      <v-select
        v-model="prioridad"
        label="Prioridad"
        :items="[
          { title: 'Alta', value: 'alta' },
          { title: 'Media', value: 'media' },
          { title: 'Baja', value: 'baja' },
        ]"
        prepend-icon="mdi-flag"
        variant="outlined"
      />

      <v-text-field
        v-model="fechaLimite"
        label="Fecha límite"
        type="date"
        prepend-icon="mdi-calendar"
        variant="outlined"
      />

      <p v-if="mensaje" class="text-green mt-2">{{ mensaje }}</p>
    </v-card-text>

    <v-card-actions>
      <v-btn block color="primary" @click="crear">
        Crear tarea
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
