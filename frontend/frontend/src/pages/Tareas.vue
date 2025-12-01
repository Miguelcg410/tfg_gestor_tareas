<script setup>
import { ref, onMounted, computed } from "vue";
import api from "../services/api";
import CrearTarea from "../components/CrearTarea.vue";

const tareas = ref([]);
const mensaje = ref("");
const modoEdicion = ref(null);
const nuevoTitulo = ref("");
const nuevaDescripcion = ref("");
const filtro = ref("all");

// AGREGADO: propiedad expanded para animación
function toggleExpand(t) {
  t.expanded = !t.expanded;
}

// ==============================
// CARGAR TAREAS
// ==============================
async function cargarTareas() {
  try {
    const res = await api.get("/tareas");

    // inicializamos expanded
    tareas.value = res.data.map(t => ({ ...t, expanded: false }));

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
// CAMBIAR ESTADO
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
// ELIMINAR
// ==============================
async function eliminarTarea(id) {
  try {
    await api.delete(`/tareas/${id}`);
    tareas.value = tareas.value.filter((x) => x.id !== id);
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
// DASHBOARD
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
// FILTROS
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
    default:
      return tareas.value;
  }
});

function setFiltro(nuevo) {
  filtro.value = nuevo;
  setTimeout(() => {
    const el = document.getElementById("lista-tareas");
    if (el) el.scrollIntoView({ behavior: "smooth" });
  }, 100);
}

function clearFiltro() {
  filtro.value = "all";
}
</script>

<template>
  <v-container class="mt-8">

    <!-- HEADER con icono NUEVO y SIN "Material Design Pro" -->
    <div class="d-flex align-center mb-6">
      <div class="header-left d-flex align-center">
        <v-icon size="36" class="mr-3" color="primary">mdi-notebook-outline</v-icon>
        <div>
          <h2 class="text-h4 mb-0">Mis tareas</h2>
        </div>
      </div>

      <v-spacer />

      <div class="d-flex align-center">
        <v-btn class="mr-3" color="primary" variant="tonal" @click="cargarTareas">
          <v-icon left>mdi-reload</v-icon>
          Recargar
        </v-btn>
        <v-btn color="secondary" @click="setFiltro('all')">Ver todas</v-btn>
      </div>
    </div>

    <p v-if="mensaje" class="mb-4">{{ mensaje }}</p>

    <!-- CREAR -->
    <CrearTarea />

    <!-- EMPTY -->
    <div v-if="tareas.length === 0" class="empty-state pa-8">
      <v-icon size="96" color="grey lighten-1">mdi-clipboard-check-outline</v-icon>
      <h3 class="mt-3">No hay tareas todavía</h3>
      <p class="text-grey">Crea tu primera tarea usando el formulario de arriba.</p>
    </div>

    <!-- DASHBOARD -->
    <div v-else>
      <v-row dense class="mb-6">

        <v-col cols="12" sm="6" md="3">
          <v-card class="dash-card dash-all" elevation="12" @click="setFiltro('all')">
            <div class="dash-inner">
              <v-icon size="36">mdi-format-list-checks</v-icon>
              <div class="dash-number">{{ totalTareas }}</div>
              <div class="dash-label">Total</div>
            </div>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <v-card class="dash-card dash-completed" elevation="12" @click="setFiltro('completed')">
            <div class="dash-inner">
              <v-icon size="36">mdi-checkbox-marked-circle</v-icon>
              <div class="dash-number">{{ tareasCompletadas }}</div>
              <div class="dash-label">Completadas</div>
            </div>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <v-card class="dash-card dash-pending" elevation="12" @click="setFiltro('pending')">
            <div class="dash-inner">
              <v-icon size="36">mdi-progress-clock</v-icon>
              <div class="dash-number">{{ tareasPendientes }}</div>
              <div class="dash-label">Pendientes</div>
            </div>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <v-card class="dash-card dash-alta" elevation="12" @click="setFiltro('alta')">
            <div class="dash-inner">
              <v-icon size="36">mdi-alert-circle</v-icon>
              <div class="dash-number">{{ tareasAlta }}</div>
              <div class="dash-label">Alta prioridad</div>
            </div>
          </v-card>
        </v-col>

      </v-row>

      <!-- LISTADO -->
      <v-row dense id="lista-tareas">
        <transition-group name="fade-slide" tag="div" class="w-100">

          <v-col v-for="t in filteredTareas" :key="t.id" cols="12">

            <v-card
              class="task-card"
              elevation="8"
              :class="{ expanded: t.expanded }"
              @click="toggleExpand(t)"
              :style="{ borderLeft: '6px solid ' + colorPrioridad(t.prioridad) }"
            >

              <!-- EDITANDO -->
              <div v-if="modoEdicion === t.id" class="pa-4">
                <v-text-field v-model="nuevoTitulo" label="Nuevo título" dense />
                <v-textarea v-model="nuevaDescripcion" label="Nueva descripción" dense />

                <div class="d-flex mt-2">
                  <v-btn color="green" class="mr-2" @click="guardarCambios(t)">Guardar</v-btn>
                  <v-btn color="grey" @click="modoEdicion = null">Cancelar</v-btn>
                </div>
              </div>

              <!-- NORMAL -->
              <div v-else class="pa-4 d-flex align-center">

                <div class="left-col d-flex align-center" @click.stop>
                  <v-checkbox :model-value="t.completada" @update:model-value="()=> cambiarEstado(t)" />
                </div>

                <div class="body-col" style="flex: 1;">
                  <div class="d-flex align-center">
                    <div class="task-title" :class="{ done: t.completada }">{{ t.titulo }}</div>
                    <v-chip class="ml-3" small :style="{ backgroundColor: colorPrioridad(t.prioridad), color: 'white' }">
                      {{ t.prioridad }}
                    </v-chip>
                  </div>

                  <div v-if="t.expanded" class="task-desc text-caption text-grey mt-2">
                    {{ t.descripcion }}
                  </div>
                </div>

                <div class="right-col d-flex align-center">
                  <div class="date-badge mr-3">{{ formatoFecha(t.fecha_limite) }}</div>

                  <v-btn icon small color="orange" @click.stop="editar(t)">
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>

                  <v-btn icon small color="red" @click.stop="eliminarTarea(t.id)">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
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
/********************************************
 CARD EXPAND (nuevo)
********************************************/
.task-card {
  border-radius: 14px;
  overflow: hidden;
  transition: transform .25s ease, box-shadow .25s ease;
  background-image: url("/textures/quemado.jpg");
  background-size: cover;
  background-position: center;
  border: 3px solid rgba(80,40,10,0.65);
  box-shadow: 0 8px 25px rgba(0,0,0,0.6);
  filter: brightness(1.05) contrast(1.1);
}


.task-card.expanded {
  transform: scale(1.03);
  box-shadow: 0 30px 60px rgba(0,0,0,0.55);
  padding-bottom: 20px;
}

/********************************************
 MATERIAL DESIGN PRO — YA NO APARECE
********************************************/

/* DASHBOARD */
.dash-card {
  border-radius: 16px;
  padding: 18px;
  cursor: pointer;
  transition: transform .26s cubic-bezier(.2,.9,.2,1), box-shadow .26s ease;
  background: linear-gradient(135deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  min-height: 96px;
}
.dash-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 22px 50px rgba(0,0,0,0.55);
}

.dash-inner {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.dash-number {
  font-size: 24px;
  font-weight: 800;
  margin-top: 6px;
}
.dash-label {
  opacity: 0.75;
  font-size: 13px;
}

/* COLORES */
.dash-all {
  background: linear-gradient(135deg, #1e88e5, #1565c0);
  color: white;
}
.dash-completed {
  background: linear-gradient(135deg, #43a047, #2e7d32);
  color: white;
}
.dash-pending {
  background: linear-gradient(135deg, #fb8c00, #f57c00);
  color: white;
}
.dash-alta {
  background: linear-gradient(135deg, #e53935, #c62828);
  color: white;
}

/* TEXTOS */
.task-title {
  font-weight: 700;
  font-size: 20px;
  color: #3a1f0a;
  font-family: 'Cinzel', serif;
  text-shadow: 1px 1px 1px rgba(255,210,140,0.4);
}

.task-title.done {
  text-decoration: line-through;
  opacity: 0.6;
}

/* FECHA */
.date-badge {
  background: rgba(255,255,255,0.05);
  padding: 6px 10px;
  border-radius: 8px;
  font-size: 12px;
}

/* EMPTY */
.empty-state {
  text-align: center;
  color: rgba(255,255,255,0.85);
}

/* ANIMACIONES */
.fade-slide-enter-active {
  transition: all 380ms cubic-bezier(.2,.9,.2,1);
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}
/* PAPEL / PAPIRO MEDIEVAL PARA LAS TAREAS */
.task-card {
  background-image: url("/textures/quemado.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  border-radius: 12px;
  border: 2px solid rgba(80, 50, 20, 0.7);
  box-shadow: 0 12px 45px rgba(0,0,0,0.55);
  padding: 14px;
  transition: all .25s ease;
}

/* Cuando se expande */
.task-card.expanded {
  transform: scale(1.04);
  box-shadow: 0 20px 60px rgba(0,0,0,0.6);
}

/* TÍTULO ESTILO RUNAS MEDIEVALES */
.task-title {
  font-family: "Cinzel", serif;
  font-weight: 800;
  letter-spacing: 1px;
  color: #3b260f;
}

/* DESCRIPCIÓN */
.task-desc {
  font-family: 'MedievalSharp', cursive;
  color: #4a2b18;
  font-size: 14px;
  opacity: 0.9;
}


/* CHIP DE PRIORIDAD ESTILO SELLO */
.v-chip {
  border-radius: 6px !important;
  padding: 4px 10px !important;
  font-family: 'Cinzel', serif;
  border: 1px solid rgba(50,25,10,0.5);
  box-shadow: inset 0 0 8px rgba(0,0,0,0.3);
}


/* FECHA COMO ETIQUETA DE PERGAMINO */
.date-badge {
  background: rgba(110,50,20,0.25);
  border: 2px solid rgba(150,80,30,0.65);
  font-family: 'Cinzel', serif;
  color: #3a1f0a;
}


</style>
