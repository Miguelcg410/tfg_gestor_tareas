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

function toggleExpand(t) {
  t.expanded = !t.expanded;
}

// ==============================
// CARGAR TAREAS
// ==============================
async function cargarTareas() {
  try {
    const res = await api.get("/tareas");
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
  <v-container class="mt-8 tareas-container">

    <!-- HEADER MEJORADO -->
    <div class="header-epic mb-6">
      <div class="header-left">
        <div class="icon-wrapper">
          <v-icon size="42" class="header-icon">mdi-sword-cross</v-icon>
          <div class="icon-glow"></div>
        </div>
        <div class="header-text">
          <h2 class="titulo-principal">Mis Tareas</h2>
          <p class="subtitulo">Gestiona tus misiones épicas</p>
        </div>
      </div>

      <div class="header-actions">
        <v-btn 
          class="btn-reload" 
          variant="tonal" 
          @click="cargarTareas"
        >
          <v-icon left>mdi-reload</v-icon>
          Recargar
        </v-btn>
        <v-btn 
          class="btn-all" 
          @click="setFiltro('all')"
        >
          <v-icon left>mdi-view-grid</v-icon>
          Ver todas
        </v-btn>
      </div>
    </div>

    <!-- MENSAJE -->
    <v-alert 
      v-if="mensaje" 
      class="mensaje-alert mb-4"
      type="info"
      variant="tonal"
      closable
    >
      {{ mensaje }}
    </v-alert>

    <!-- CREAR TAREA -->
    <div class="crear-wrapper mb-6">
      <CrearTarea />
    </div>

    <!-- EMPTY STATE MEJORADO -->
    <div v-if="tareas.length === 0" class="empty-state-epic">
      <div class="empty-icon-wrapper">
        <v-icon size="120" class="empty-icon">mdi-scroll-text</v-icon>
        <div class="empty-glow"></div>
      </div>
      <h3 class="empty-title">No hay tareas todavía</h3>
      <p class="empty-subtitle">Comienza tu aventura creando tu primera tarea épica</p>
    </div>

    <!-- DASHBOARD MEJORADO -->
    <div v-else class="dashboard-section">
      <v-row dense class="mb-6">

        <v-col cols="12" sm="6" md="3">
          <div 
            class="dash-card dash-all" 
            @click="setFiltro('all')"
          >
            <div class="dash-icon-wrapper">
              <v-icon size="40" class="dash-icon">mdi-format-list-checks</v-icon>
              <div class="dash-glow"></div>
            </div>
            <div class="dash-content">
              <div class="dash-number">{{ totalTareas }}</div>
              <div class="dash-label">Total</div>
            </div>
            <div class="dash-corner"></div>
          </div>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <div 
            class="dash-card dash-completed" 
            @click="setFiltro('completed')"
          >
            <div class="dash-icon-wrapper">
              <v-icon size="40" class="dash-icon">mdi-checkbox-marked-circle</v-icon>
              <div class="dash-glow"></div>
            </div>
            <div class="dash-content">
              <div class="dash-number">{{ tareasCompletadas }}</div>
              <div class="dash-label">Completadas</div>
            </div>
            <div class="dash-corner"></div>
          </div>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <div 
            class="dash-card dash-pending" 
            @click="setFiltro('pending')"
          >
            <div class="dash-icon-wrapper">
              <v-icon size="40" class="dash-icon">mdi-progress-clock</v-icon>
              <div class="dash-glow"></div>
            </div>
            <div class="dash-content">
              <div class="dash-number">{{ tareasPendientes }}</div>
              <div class="dash-label">Pendientes</div>
            </div>
            <div class="dash-corner"></div>
          </div>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <div 
            class="dash-card dash-alta" 
            @click="setFiltro('alta')"
          >
            <div class="dash-icon-wrapper">
              <v-icon size="40" class="dash-icon">mdi-alert-circle</v-icon>
              <div class="dash-glow"></div>
            </div>
            <div class="dash-content">
              <div class="dash-number">{{ tareasAlta }}</div>
              <div class="dash-label">Alta prioridad</div>
            </div>
            <div class="dash-corner"></div>
          </div>
        </v-col>

      </v-row>

      <!-- LISTADO MEJORADO -->
      <div class="lista-section" id="lista-tareas">
        <transition-group name="fade-slide" tag="div" class="tareas-grid">

          <div v-for="t in filteredTareas" :key="t.id" class="tarea-wrapper">

            <div
              class="task-card-epic"
              :class="{ 
                expanded: t.expanded,
                completada: t.completada
              }"
              @click="toggleExpand(t)"
              :style="{ borderLeftColor: colorPrioridad(t.prioridad) }"
            >

              <!-- MODO EDICIÓN -->
              <div v-if="modoEdicion === t.id" class="edit-mode" @click.stop>
                <div class="edit-header">
                  <v-icon>mdi-pencil</v-icon>
                  <span>Editando tarea</span>
                </div>
                
                <v-text-field 
                  v-model="nuevoTitulo" 
                  label="Título" 
                  variant="outlined"
                  class="mb-3"
                />
                <v-textarea 
                  v-model="nuevaDescripcion" 
                  label="Descripción" 
                  variant="outlined"
                  rows="3"
                />

                <div class="edit-actions">
                  <v-btn 
                    class="btn-save" 
                    @click="guardarCambios(t)"
                  >
                    <v-icon left>mdi-content-save</v-icon>
                    Guardar
                  </v-btn>
                  <v-btn 
                    class="btn-cancel" 
                    variant="outlined"
                    @click="modoEdicion = null"
                  >
                    <v-icon left>mdi-close</v-icon>
                    Cancelar
                  </v-btn>
                </div>
              </div>

              <!-- MODO NORMAL -->
              <div v-else class="task-content">

                <!-- CHECKBOX -->
                <div class="task-checkbox" @click.stop>
                  <v-checkbox 
                    :model-value="t.completada" 
                    @update:model-value="() => cambiarEstado(t)"
                    color="success"
                    hide-details
                  />
                </div>

                <!-- BODY -->
                <div class="task-body">
                  <div class="task-header-row">
                    <h3 class="task-title" :class="{ done: t.completada }">
                      {{ t.titulo }}
                    </h3>
                    <div class="priority-badge" :style="{ 
                      backgroundColor: colorPrioridad(t.prioridad),
                      boxShadow: `0 0 12px ${colorPrioridad(t.prioridad)}40`
                    }">
                      <v-icon size="14" class="mr-1">mdi-flag</v-icon>
                      {{ t.prioridad }}
                    </div>
                  </div>

                  <transition name="expand">
                    <div v-if="t.expanded" class="task-description">
                      <v-icon size="16" class="mr-1">mdi-text</v-icon>
                      {{ t.descripcion || 'Sin descripción' }}
                    </div>
                  </transition>

                  <div class="task-footer">
                    <div class="date-badge">
                      <v-icon size="16" class="mr-1">mdi-calendar</v-icon>
                      {{ formatoFecha(t.fecha_limite) }}
                    </div>
                  </div>
                </div>

                <!-- ACTIONS -->
                <div class="task-actions" @click.stop>
                  <v-btn 
                    icon 
                    size="small"
                    class="action-btn btn-edit"
                    @click="editar(t)"
                  >
                    <v-icon size="20">mdi-pencil</v-icon>
                  </v-btn>

                  <v-btn 
                    icon 
                    size="small"
                    class="action-btn btn-delete"
                    @click="eliminarTarea(t.id)"
                  >
                    <v-icon size="20">mdi-delete</v-icon>
                  </v-btn>
                </div>

              </div>

            </div>

          </div>

        </transition-group>
      </div>

    </div>

  </v-container>
</template>

<style scoped>
/* ========================================
   CONTENEDOR PRINCIPAL
======================================== */
.tareas-container {
  max-width: 1400px;
  animation: fadeIn 0.6s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* ========================================
   HEADER ÉPICO
======================================== */
.header-epic {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  background: linear-gradient(135deg, rgba(255, 170, 80, 0.1) 0%, rgba(255, 120, 50, 0.05) 100%);
  border-radius: 20px;
  border: 2px solid rgba(255, 170, 80, 0.2);
  position: relative;
  overflow: hidden;
}

.header-epic::before {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 170, 80, 0.05) 0%, transparent 70%);
  animation: headerGlow 3s ease infinite;
}

@keyframes headerGlow {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(10%, 10%); }
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
  position: relative;
  z-index: 1;
}

.icon-wrapper {
  position: relative;
}

.header-icon {
  color: #ffaa50 !important;
  filter: drop-shadow(0 0 8px rgba(255, 170, 80, 0.6));
  animation: iconFloat 3s ease infinite;
}

@keyframes iconFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-5px) rotate(5deg); }
}

.icon-glow {
  position: absolute;
  inset: -10px;
  background: radial-gradient(circle, rgba(255, 170, 80, 0.3), transparent);
  filter: blur(15px);
  animation: glowPulse 2s ease infinite;
}

@keyframes glowPulse {
  0%, 100% { opacity: 0.5; transform: scale(0.9); }
  50% { opacity: 1; transform: scale(1.1); }
}

.titulo-principal {
  font-family: "Cinzel", serif;
  font-size: 36px;
  font-weight: 800;
  color: #ffe7cf;
  text-shadow: 
    0 0 20px rgba(255, 170, 80, 0.6),
    0 2px 4px rgba(0, 0, 0, 0.5);
  letter-spacing: 2px;
  margin: 0;
}

.subtitulo {
  font-size: 14px;
  color: #ffcc88;
  opacity: 0.9;
  margin: 4px 0 0 0;
  font-family: "Cinzel", serif;
}

.header-actions {
  display: flex;
  gap: 12px;
  position: relative;
  z-index: 1;
}

.btn-reload,
.btn-all {
  font-family: "Cinzel", serif;
  font-weight: 600;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.btn-reload {
  background: rgba(255, 170, 80, 0.2) !important;
  color: #ffaa50 !important;
}

.btn-reload:hover {
  background: rgba(255, 170, 80, 0.3) !important;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 170, 80, 0.3);
}

.btn-all {
  background: linear-gradient(135deg, #ff9b4d 0%, #ff7e1f 100%) !important;
  color: white !important;
}

.btn-all:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 126, 31, 0.4);
}

/* ========================================
   EMPTY STATE ÉPICO
======================================== */
.empty-state-epic {
  text-align: center;
  padding: 80px 20px;
  position: relative;
}

.empty-icon-wrapper {
  position: relative;
  display: inline-block;
  margin-bottom: 30px;
}

.empty-icon {
  color: rgba(255, 170, 80, 0.3) !important;
  animation: emptyFloat 3s ease infinite;
}

@keyframes emptyFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

.empty-glow {
  position: absolute;
  inset: -20px;
  background: radial-gradient(circle, rgba(255, 170, 80, 0.2), transparent);
  filter: blur(30px);
  animation: glowPulse 2s ease infinite;
}

.empty-title {
  font-family: "Cinzel", serif;
  font-size: 28px;
  color: #ffe7cf;
  margin-bottom: 12px;
}

.empty-subtitle {
  color: #ffcc88;
  font-size: 16px;
  opacity: 0.8;
}

/* ========================================
   DASHBOARD CARDS MEJORADAS
======================================== */
.dash-card {
  position: relative;
  border-radius: 20px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  min-height: 140px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.dash-card::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.dash-card:hover::before {
  opacity: 1;
}

.dash-card:hover {
  transform: translateY(-12px) scale(1.03);
  box-shadow: 0 25px 60px rgba(0,0,0,0.6);
}

.dash-icon-wrapper {
  position: relative;
  display: inline-block;
  margin-bottom: 12px;
}

.dash-icon {
  position: relative;
  z-index: 1;
}

.dash-glow {
  position: absolute;
  inset: -10px;
  background: radial-gradient(circle, currentColor, transparent);
  opacity: 0.3;
  filter: blur(15px);
}

.dash-content {
  position: relative;
  z-index: 1;
}

.dash-number {
  font-size: 32px;
  font-weight: 900;
  margin-bottom: 6px;
  font-family: "Cinzel", serif;
}

.dash-label {
  font-size: 14px;
  opacity: 0.9;
  font-weight: 600;
  font-family: "Cinzel", serif;
}

.dash-corner {
  position: absolute;
  top: 0;
  right: 0;
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.05);
  clip-path: polygon(100% 0, 100% 100%, 0 0);
}

/* COLORES MEJORADOS */
.dash-all {
  background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
  color: white;
  border: 2px solid rgba(30, 136, 229, 0.5);
}

.dash-completed {
  background: linear-gradient(135deg, #43a047 0%, #2e7d32 100%);
  color: white;
  border: 2px solid rgba(67, 160, 71, 0.5);
}

.dash-pending {
  background: linear-gradient(135deg, #fb8c00 0%, #f57c00 100%);
  color: white;
  border: 2px solid rgba(251, 140, 0, 0.5);
}

.dash-alta {
  background: linear-gradient(135deg, #e53935 0%, #c62828 100%);
  color: white;
  border: 2px solid rgba(229, 57, 53, 0.5);
}

/* ========================================
   TARJETAS DE TAREAS MEJORADAS
======================================== */
.tareas-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.tarea-wrapper {
  animation: slideIn 0.4s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.task-card-epic {
  background-image: url("/textures/quemado.jpg");
  background-size: cover;
  background-position: center;
  border-radius: 16px;
  border-left: 6px solid;
  border-right: 2px solid rgba(80, 40, 10, 0.5);
  border-top: 2px solid rgba(80, 40, 10, 0.5);
  border-bottom: 2px solid rgba(80, 40, 10, 0.5);
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
}

.task-card-epic::before {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(255, 170, 80, 0.1), transparent 60%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.task-card-epic:hover::before {
  opacity: 1;
}

.task-card-epic:hover {
  transform: translateX(8px) scale(1.02);
  box-shadow: 
    0 12px 35px rgba(0, 0, 0, 0.5),
    -8px 0 20px rgba(255, 170, 80, 0.2);
}

.task-card-epic.expanded {
  transform: scale(1.03);
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.6),
    0 0 40px rgba(255, 170, 80, 0.2);
}

.task-card-epic.completada {
  opacity: 0.7;
  filter: grayscale(0.3);
}

.task-content {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.task-checkbox {
  flex-shrink: 0;
}

.task-body {
  flex: 1;
  min-width: 0;
}

.task-header-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.task-title {
  font-family: "Cinzel", serif;
  font-size: 22px;
  font-weight: 800;
  color: #3b260f;
  text-shadow: 1px 1px 2px rgba(255, 210, 140, 0.5);
  letter-spacing: 0.5px;
  margin: 0;
  transition: all 0.3s ease;
}

.task-title.done {
  text-decoration: line-through;
  opacity: 0.5;
}

.priority-badge {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  color: white;
  font-family: "Cinzel", serif;
  letter-spacing: 0.5px;
  border: 2px solid rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.task-card-epic:hover .priority-badge {
  transform: scale(1.1);
}

.task-description {
  font-family: 'MedievalSharp', cursive;
  color: #4a2b18;
  font-size: 15px;
  line-height: 1.6;
  padding: 12px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  border: 1px solid rgba(80, 40, 10, 0.3);
  margin-bottom: 12px;
  display: flex;
  align-items: start;
}

.task-footer {
  display: flex;
  align-items: center;
  gap: 12px;
}

.date-badge {
  display: flex;
  align-items: center;
  background: rgba(110, 50, 20, 0.3);
  border: 2px solid rgba(150, 80, 30, 0.6);
  border-radius: 10px;
  padding: 6px 12px;
  font-family: 'Cinzel', serif;
  color: #3a1f0a;
  font-weight: 600;
  font-size: 13px;
}

.task-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex-shrink: 0;
}

.action-btn {
  background: rgba(255, 255, 255, 0.1) !important;
  border: 2px solid rgba(80, 40, 10, 0.3);
  transition: all 0.3s ease;
}

.btn-edit:hover {
  background: rgba(251, 140, 0, 0.2) !important;
  border-color: #fb8c00;
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 4px 15px rgba(251, 140, 0, 0.3);
}

.btn-delete:hover {
  background: rgba(229, 57, 53, 0.2) !important;
  border-color: #e53935;
  transform: scale(1.1) rotate(-5deg);
  box-shadow: 0 4px 15px rgba(229, 57, 53, 0.3);
}

/* ========================================
   MODO EDICIÓN
======================================== */
.edit-mode {
  padding: 20px;
}

.edit-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  color: #3b260f;
  font-family: "Cinzel", serif;
  font-size: 18px;
  font-weight: 600;
}

.edit-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.btn-save {
  background: linear-gradient(135deg, #43a047 0%, #2e7d32 100%) !important;
  color: white !important;
  font-weight: 700;
  font-family: "Cinzel", serif;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.btn-save:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(67, 160, 71, 0.4);
}

.btn-cancel {
  font-family: "Cinzel", serif;
  color: #8b5a2b !important;
  border-color: rgba(139, 90, 43, 0.5) !important;
}

/* ========================================
   ANIMACIONES DE TRANSICIÓN
======================================== */
.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
  margin: 0;
  padding: 0;
}

.expand-enter-to,
.expand-leave-from {
  opacity: 1;
  max-height: 200px;
}

.fade-slide-enter-active {
  transition: all 0.4s cubic-bezier(0.2, 0.9, 0.2, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}

/* ========================================
   RESPONSIVE
======================================== */
@media (max-width: 960px) {
  .header-epic {
    flex-direction: column;
    gap: 20px;
  }

  .titulo-principal {
    font-size: 28px;
  }

  .task-content {
    flex-wrap: wrap;
  }

  .task-actions {
    flex-direction: row;
    width: 100%;
    justify-content: flex-end;
  }
}

@media (max-width: 600px) {
  .titulo-principal {
    font-size: 24px;
  }

  .dash-number {
    font-size: 26px;
  }

  .task-title {
    font-size: 18px;
  }

  .header-actions {
    flex-direction: column;
    width: 100%;
  }

  .btn-reload,
  .btn-all {
    width: 100%;
  }
}
</style>