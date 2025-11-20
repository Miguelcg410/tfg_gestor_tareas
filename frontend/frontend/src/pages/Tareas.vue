<script setup>
import { ref } from "vue";
import api from "../services/api";
import CrearTarea from "../components/CrearTarea.vue";

// VARIABLES
const tareas = ref([]);
const mensaje = ref("");
const modoEdicion = ref(null);
const nuevoTitulo = ref("");
const nuevaDescripcion = ref("");

// CARGAR TAREAS
async function cargarTareas() {
  try {
    const res = await api.get("/tareas");
    tareas.value = res.data;
    mensaje.value = "Tareas cargadas correctamente";
  } catch {
    mensaje.value = "Error cargando tareas";
  }
}

// EDITAR ESTADO (checkbox)
async function cambiarEstado(t) {
  try {
    await api.put(`/tareas/${t.id}`, {
      titulo: t.titulo,
      descripcion: t.descripcion,
      prioridad: t.prioridad,
      fecha_limite: t.fecha_limite,
      completada: !t.completada,
    });
    t.completada = !t.completada;
  } catch (error) {
    console.error(error);
  }
}

// ELIMINAR
async function eliminarTarea(id) {
  try {
    await api.delete(`/tareas/${id}`);
    tareas.value = tareas.value.filter(t => t.id !== id);
  } catch (error) {
    console.error(error);
  }
}

// ACTIVAR MODO EDICIÓN
function editar(t) {
  modoEdicion.value = t.id;
  nuevoTitulo.value = t.titulo;
  nuevaDescripcion.value = t.descripcion;
}

// GUARDAR CAMBIOS
async function guardarCambios(t) {
  try {
    await api.put(`/tareas/${t.id}`, {
      titulo: nuevoTitulo.value,
      descripcion: nuevaDescripcion.value,
      prioridad: t.prioridad,
      fecha_limite: t.fecha_limite,
      completada: t.completada,
    });

    modoEdicion.value = null;
    cargarTareas();
  } catch (error) {
    console.error(error);
  }
}

// COLORES DE PRIORIDAD
function colorPrioridad(p) {
  return p === "alta"
    ? "red"
    : p === "media"
    ? "orange"
    : "green";
}

</script>

<template>
  <v-container class="mt-6">

    <h2 class="text-h5 mb-4">Mis tareas</h2>

    <v-btn color="primary" @click="cargarTareas" class="mb-4">
      Cargar tareas
    </v-btn>

    <p>{{ mensaje }}</p>

    <CrearTarea />

    <v-row dense class="mt-6">

      <!-- LISTA DE TAREAS -->
      <v-col
        v-for="t in tareas"
        :key="t.id"
        cols="12"
      >
        <v-card class="pa-4" elevation="6">

          <!-- MODO EDICIÓN -->
          <div v-if="modoEdicion === t.id">

            <v-text-field
              v-model="nuevoTitulo"
              label="Nuevo título"
            />

            <v-textarea
              v-model="nuevaDescripcion"
              label="Nueva descripción"
            />

            <v-btn color="green" class="mr-2" @click="guardarCambios(t)">
              Guardar
            </v-btn>

            <v-btn color="grey" @click="modoEdicion = null">
              Cancelar
            </v-btn>
          </div>

          <!-- MODO NORMAL -->
          <div v-else>

            <v-card-title class="d-flex align-center">

              <v-checkbox
                v-model="t.completada"
                @change="cambiarEstado(t)"
              />

              <span :style="{ textDecoration: t.completada ? 'line-through' : 'none' }">
                {{ t.titulo }}
              </span>

              <v-chip class="ml-4" :color="colorPrioridad(t.prioridad)" text-color="white">
                {{ t.prioridad }}
              </v-chip>

              <v-spacer />

              <v-icon class="mr-1">mdi-calendar</v-icon>
              <span>{{ t.fecha_limite }}</span>

            </v-card-title>

            <v-card-text>
              {{ t.descripcion }}
            </v-card-text>

            <v-card-actions>
              <v-btn
                icon="mdi-pencil"
                color="orange"
                @click="editar(t)"
              />
              <v-btn
                icon="mdi-delete"
                color="red"
                @click="eliminarTarea(t.id)"
              />
            </v-card-actions>

          </div>

        </v-card>
      </v-col>
    </v-row>

  </v-container>
</template>

