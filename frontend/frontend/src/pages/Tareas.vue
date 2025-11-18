<script setup>
import { ref } from "vue";
import api from "../services/api";

const tareas = ref([]);
const mensaje = ref("");
const modoEdicion = ref(null); // ID de la tarea que se está editando
const nuevoTitulo = ref("");
const nuevaDescripcion = ref("");

async function cargarTareas() {
  try {
    const res = await api.get("/tareas");
    tareas.value = res.data;
    mensaje.value = "Tareas cargadas correctamente";
  } catch (error) {
    mensaje.value = "Error cargando tareas";
  }
}

async function eliminarTarea(id) {
  try {
    await api.delete(`/tareas/${id}`);
    tareas.value = tareas.value.filter(t => t.id !== id);
  } catch (error) {
    console.error(error);
  }
}

async function actualizarTarea(tarea) {
  try {
    await api.put(`/tareas/${tarea.id}`, {
      titulo: nuevoTitulo.value,
      descripcion: nuevaDescripcion.value,
      completada: tarea.completada
    });

    modoEdicion.value = null;
    cargarTareas();

  } catch (error) {
    console.error(error);
  }
}

async function cambiarEstado(tarea) {
  try {
    await api.put(`/tareas/${tarea.id}`, {
      titulo: tarea.titulo,
      descripcion: tarea.descripcion,
      completada: !tarea.completada
    });

    tarea.completada = !tarea.completada;
  } catch (error) {
    console.error(error);
  }
}

function editar(tarea) {
  modoEdicion.value = tarea.id;
  nuevoTitulo.value = tarea.titulo;
  nuevaDescripcion.value = tarea.descripcion;
}
</script>

<template>
  <div>
    <h2>Mis tareas</h2>

    <button @click="cargarTareas">Cargar tareas</button>

    <p>{{ mensaje }}</p>

    <ul>
      <li v-for="t in tareas" :key="t.id">

        <!-- Checkbox de completada -->
        <input type="checkbox" :checked="t.completada" @change="cambiarEstado(t)" />

        <!-- Vista normal -->
        <span v-if="modoEdicion !== t.id">
          <strong :style="{ textDecoration: t.completada ? 'line-through' : 'none' }">
            {{ t.titulo }}
          </strong>
          – {{ t.descripcion }}
        </span>

        <!-- Modo edición -->
        <span v-else>
          <input v-model="nuevoTitulo" placeholder="Nuevo título" />
          <input v-model="nuevaDescripcion" placeholder="Nueva descripción" />
          <button @click="actualizarTarea(t)">Guardar</button>
          <button @click="modoEdicion = null">Cancelar</button>
        </span>

        <!-- Botones -->
        <button v-if="modoEdicion !== t.id" @click="editar(t)">Editar</button>
        <button @click="eliminarTarea(t.id)">Eliminar</button>

      </li>
    </ul>
  </div>
</template>
