<script setup>
import { ref, onMounted, computed } from "vue";
import api from "../services/api";
import CrearTarea from "../components/CrearTarea.vue";

const tareas = ref([]);
const mensaje = ref("");
const modoEdicion = ref(null);
const nuevoTitulo = ref("");
const nuevaDescripcion = ref("");
const filtro = ref("all"); // all | completed | pending | alta | proximas

// ==============================
// CARGAR TAREAS
// ==============================
async function cargarTareas() {
  try {
    const res = await api.get("/tareas");
    tareas.value = res.data;
    mensaje.value = "Tareas cargadas correctamente";
  } catch (e) {
    console.error(e);
    mensaje.value = "Error cargando tareas";
  }
}

onMounted(() => {
  cargarTareas();
});

// ==============================
// CAMBIAR ESTADO (COMPLETADA)
// ==============================
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
  } catch (e) {
    console.error(e);
  }
}

// ==============================
// ELIMINAR TAREA
// ==============================
async function eliminarTarea(id) {
  try {
    await api.delete(`/tareas/${id}`);
    tareas.value = tareas.value.filter((t) => t.id !== id);
  } catch (e) {
    console.error(e);
  }
}

// ==============================
// EDITAR / GUARDAR
// ==============================
function editar(t) {
  modoEdicion.value = t.id;
  nuevoTitulo.value = t.titulo;
  nuevaDescripcion.value = t.descripcion;
}

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
    await cargarTareas();
  } catch (e) {
    console.error(e);
  }
}

// ==============================
// UTILIDADES
// ==============================
function colorPrioridad(p) {
  return p === "alta" ? "#ef5350" : p === "media" ? "#ffb74d" : "#66bb6a";
}

function formatoFecha(f) {
  if (!f) return "-";
  try {
    return new Date(f).toLocaleDateString("es-ES");
  } catch {
    return f;
  }
}

// ==============================
// DASHBOARD (RESUMEN)
// ==============================
const totalTareas = computed(() => tareas.value.length);
const tareasCompletadas = computed(() => tareas.value.filter((t) => t.completada).length);
const tareasPendientes = computed(() => tareas.value.filter((t) => !t.completada).length);
const tareasAlta = computed(() => tareas.value.filter((t) => t.prioridad === "alta").length);
const tareasProximas = computed(() => {
  const hoy = new Date();
  return tareas.value.filter((t) => {
    if (!t.fecha_limite) return false;
    const fecha = new Date(t.fecha_limite);
    const diff = (fecha - hoy) / (1000 * 60 * 60 * 24);
    return diff <= 3 && diff >= 0;
  }).length;
});

// ==============================
// FILTRADO y SCROLL
// ==============================
const filteredTareas = computed(() => {
  switch (filtro.value) {
    case "completed":
      return tareas.value.filter((t) => t.completada);
    case "pending":
      return tareas.value.filter((t) => !t.completada);
    case "alta":
      return tareas.value.filter((t) => t.prioridad === "alta");
    case "proximas": {
      const hoy = new Date();
      return tareas.value.filter((t) => {
        if (!t.fecha_limite) return false;
        const fecha = new Date(t.fecha_limite);
        const diff = (fecha - hoy) / (1000 * 60 * 60 * 24);
        return diff <= 3 && diff >= 0;
      });
    }
    case "all":
    default:
      return tareas.value;
  }
});

function setFiltro(nuevo) {
  filtro.value = nuevo || "all";
  // scroll to list after UI updates
  setTimeout(() => {
    const el = document.getElementById("lista-tareas");
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  }, 80);
}

function clearFiltro() {
  filtro.value = "all";
}
</script>

<template>
  <v-container class="mt-6">

    <!-- HEADER -->
    <div class="d-flex align-center mb-6">
      <v-icon color="primary" class="mr-3" large>mdi-briefcase-check</v-icon>
      <div>
        <h2 class="text-h4 mb-0">Mis tareas</h2>
        <div class="text-caption text-grey">Interfaz renovada · rápida · clara</div>
      </div>

      <v-spacer />

      <v-btn color="primary" @click="cargarTareas">
        <v-icon left>mdi-reload</v-icon>Recargar
      </v-btn>
    </div>

    <p v-if="mensaje">{{ mensaje }}</p>

    <!-- CREAR -->
    <CrearTarea />

    <!-- empty state -->
    <div v-if="tareas.length === 0" class="empty-state">
      <v-icon size="88" color="grey lighten-1">mdi-clipboard-check-outline</v-icon>
      <h3 class="mt-3">No hay tareas todavía</h3>
      <p class="text-grey">Crea tu primera tarea usando el formulario de arriba.</p>
    </div>

    <!-- dashboard + list -->
    <div v-else>

      <!-- DASHBOARD -->
      <v-row dense class="mb-6">

        <v-col cols="12" sm="6" md="3">
          <v-card class="dashboard-card" elevation="8" @click="setFiltro('all')">
            <div class="dash-icon"><v-icon size="28">mdi-format-list-checks</v-icon></div>
            <div class="dash-number">{{ totalTareas }}</div>
            <div class="dash-label">Total</div>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <v-card class="dashboard-card" elevation="8" @click="setFiltro('completed')">
            <div class="dash-icon"><v-icon size="28">mdi-checkbox-marked-circle-outline</v-icon></div>
            <div class="dash-number">{{ tareasCompletadas }}</div>
            <div class="dash-label">Completadas</div>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <v-card class="dashboard-card" elevation="8" @click="setFiltro('pending')">
            <div class="dash-icon"><v-icon size="28">mdi-progress-clock</v-icon></div>
            <div class="dash-number">{{ tareasPendientes }}</div>
            <div class="dash-label">Pendientes</div>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <v-card class="dashboard-card" elevation="8" @click="setFiltro('alta')">
            <div class="dash-icon"><v-icon size="28">mdi-alert-circle-outline</v-icon></div>
            <div class="dash-number">{{ tareasAlta }}</div>
            <div class="dash-label">Alta prioridad</div>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <v-card class="dashboard-card" elevation="8" @click="setFiltro('proximas')">
            <div class="dash-icon"><v-icon size="28">mdi-timer-sand</v-icon></div>
            <div class="dash-number">{{ tareasProximas }}</div>
            <div class="dash-label">Próximas (≤3d)</div>
          </v-card>
        </v-col>

      </v-row>

      <!-- filtro activo -->
      <div class="d-flex align-center mb-4" v-if="filtro !== 'all'">
        <v-chip small color="primary" text-color="white" class="mr-2">Filtrando: {{ filtro }}</v-chip>
        <v-btn small variant="tonal" @click="clearFiltro">Quitar filtro</v-btn>
      </div>

      <!-- LISTADO -->
      <v-row dense id="lista-tareas">
        <transition-group name="fade-slide" tag="div" class="w-100">
          <v-col v-for="t in filteredTareas" :key="t.id" cols="12">
            <v-card class="task-card" elevation="6" :style="{ borderLeft: '6px solid ' + colorPrioridad(t.prioridad) }">

              <!-- edit mode -->
              <div v-if="modoEdicion === t.id" class="pa-3">
                <v-text-field v-model="nuevoTitulo" label="Nuevo título" dense />
                <v-textarea v-model="nuevaDescripcion" label="Nueva descripción" dense />

                <div class="d-flex mt-2">
                  <v-btn color="green" class="mr-2" @click="guardarCambios(t)">Guardar</v-btn>
                  <v-btn color="grey" @click="modoEdicion = null">Cancelar</v-btn>
                </div>
              </div>

              <!-- normal mode -->
              <div v-else class="pa-3 d-flex align-center">

                <div class="left-col d-flex align-center">
                  <v-checkbox :model-value="t.completada" @update:model-value="() => cambiarEstado(t)" />
                </div>

                <div class="body-col" style="flex:1;">
                  <div class="d-flex align-center">
                    <div class="task-title" :class="{ done: t.completada }">{{ t.titulo }}</div>
                    <v-chip class="ml-3" small :style="{ backgroundColor: colorPrioridad(t.prioridad), color: 'white' }">{{ t.prioridad }}</v-chip>
                  </div>
                  <div class="task-desc text-caption text-grey mt-2">{{ t.descripcion }}</div>
                </div>

                <div class="right-col d-flex align-center">
                  <div class="date-badge mr-3">{{ formatoFecha(t.fecha_limite) }}</div>
                  <v-btn icon small color="orange" @click="editar(t)"><v-icon>mdi-pencil</v-icon></v-btn>
                  <v-btn icon small color="red" @click="eliminarTarea(t.id)"><v-icon>mdi-delete</v-icon></v-btn>
                </div>
              </div>

            </v-card>
          </v-col>
        </transition-group>
      </v-row>
    </div>
  </v-container>
</template>

<style scoped>
/* dashboard cards */
.dashboard-card {
  border-radius: 14px;
  padding: 18px;
  cursor: pointer;
  transition: transform .22s ease, box-shadow .22s ease;
  background: linear-gradient(135deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}
.dashboard-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 14px 30px rgba(0,0,0,0.45);
}
.dash-icon { background: rgba(255,255,255,0.02); padding: 6px; border-radius: 8px; }
.dash-number { font-size: 20px; font-weight: 700; }
.dash-label { color: rgba(255,255,255,0.6); font-size: 13px; }

/* empty state */
.empty-state { text-align: center; margin-top: 28px; color: rgba(255,255,255,0.85); }

/* task card */
.task-card {
  border-radius: 12px;
  transition: transform .2s ease, box-shadow .2s ease;
  overflow: hidden;
  background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.015));
}
.task-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 18px 40px rgba(0,0,0,0.5);
}
.task-title { font-weight: 700; font-size: 16px; }
.task-title.done { text-decoration: line-through; opacity: 0.6; }
.task-desc { color: rgba(255,255,255,0.7); }

.left-col { width: 46px; display:flex; align-items:center; justify-content:center; }
.body-col { padding-left: 8px; padding-right: 12px; }
.right-col { display:flex; align-items:center; gap:8px; }

.date-badge {
  background: rgba(0,0,0,0.25);
  padding: 6px 8px;
  border-radius: 8px;
  font-size: 12px;
  color: rgba(255,255,255,0.9);
}

/* animations */
.fade-slide-enter-active { transition: all 350ms cubic-bezier(.2,.8,.2,1); }
.fade-slide-leave-active { transition: all 220ms ease; opacity: 0; transform: translateY(6px); }
.fade-slide-enter-from { opacity: 0; transform: translateY(8px); }
.fade-slide-enter-to { opacity: 1; transform: translateY(0); }

.task-col { margin-bottom: 12px; }

/* utility */
.ml-3 { margin-left: 12px; }
.clickable-card { cursor: pointer; }
</style>
