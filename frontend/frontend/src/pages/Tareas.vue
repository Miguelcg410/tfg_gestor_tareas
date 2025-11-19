<script setup>
import { ref, computed } from "vue";
import api from "../services/api";
import CrearTarea from "../components/CrearTarea.vue";

const tareas = ref([]);
const mensaje = ref("");
const modoEdicion = ref(null);
const nuevoTitulo = ref("");
const nuevaDescripcion = ref("");
const nuevaPrioridad = ref("");
const nuevaFecha = ref("");

const filtro = ref("todas");

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
      prioridad: nuevaPrioridad.value,
      fecha_limite: nuevaFecha.value,
      completada: tarea.completada
    });

    modoEdicion.value = null;
    await cargarTareas();

  } catch (error) {
    console.error(error);
  }
}

async function cambiarEstado(tarea) {
  try {
    await api.put(`/tareas/${tarea.id}`, {
      titulo: tarea.titulo,
      descripcion: tarea.descripcion,
      prioridad: tarea.prioridad,
      fecha_limite: tarea.fecha_limite,
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
  nuevaPrioridad.value = tarea.prioridad;
  nuevaFecha.value = tarea.fecha_limite;
}

const tareasFiltradas = computed(() => {
  if (filtro.value === "pendientes") {
    return tareas.value.filter(t => !t.completada);
  }
  if (filtro.value === "completadas") {
    return tareas.value.filter(t => t.completada);
  }
  return tareas.value;
});
</script>

<template>
  <div class="contenedor-tareas">

    <h1>Mis tareas</h1>

    <button class="btn-cargar" @click="cargarTareas">Cargar tareas</button>
    <p>{{ mensaje }}</p>

    <div class="filtros">
      <button @click="filtro = 'todas'">Todas</button>
      <button @click="filtro = 'pendientes'">Pendientes</button>
      <button @click="filtro = 'completadas'">Completadas</button>
    </div>

    <div class="crear-box">
      <CrearTarea />
    </div>

    <div class="lista-tareas">
      <div
        v-for="t in tareasFiltradas"
        :key="t.id"
        class="tarea"
        :class="t.prioridad"
      >
        <input type="checkbox" :checked="t.completada" @change="cambiarEstado(t)" />

        <div v-if="modoEdicion !== t.id" class="info">
          <h3>{{ t.titulo }}</h3>
          <p>{{ t.descripcion }}</p>
          <p><strong>Prioridad:</strong> {{ t.prioridad }}</p>
          <p><strong>Fecha límite:</strong> {{ t.fecha_limite || "Sin fecha" }}</p>
        </div>

        <div v-else class="edicion">
          <input v-model="nuevoTitulo" />
          <input v-model="nuevaDescripcion" />
          <select v-model="nuevaPrioridad">
            <option value="alta">Alta</option>
            <option value="media">Media</option>
            <option value="baja">Baja</option>
          </select>
          <input type="date" v-model="nuevaFecha" />
        </div>

        <div class="acciones">
          <button v-if="modoEdicion !== t.id" @click="editar(t)" class="btn-editar">Editar</button>

          <button v-if="modoEdicion === t.id" @click="actualizarTarea(t)" class="btn-guardar">Guardar</button>

          <button v-if="modoEdicion === t.id" @click="modoEdicion = null" class="btn-cancelar">Cancelar</button>

          <button @click="eliminarTarea(t.id)" class="btn-eliminar">Eliminar</button>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.contenedor-tareas {
  max-width: 900px;
  margin: auto;
  padding: 20px;
}

.filtros button {
  margin-right: 10px;
  padding: 7px 15px;
  background: #444;
  border: none;
  border-radius: 5px;
  color: white;
  cursor: pointer;
}

.tarea {
  background: #222;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 15px;
  display: flex;
  gap: 20px;
  border-left: 8px solid #1976d2;
}

/* COLORES POR PRIORIDAD */
.tarea.alta { border-left-color: #e53935; }
.tarea.media { border-left-color: #fbc02d; }
.tarea.baja { border-left-color: #43a047; }

.btn-editar { background: #ffa726; }
.btn-eliminar { background: #e53935; }
.btn-guardar { background: #4caf50; }
.btn-cancelar { background: gray; }

button {
  padding: 7px 12px;
  color: white;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}

input, textarea, select {
  padding: 8px;
  background: #333;
  border: none;
  color: white;
  border-radius: 6px;
}
</style>
