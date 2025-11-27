<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../services/api"; // ⬅️ usamos tu cliente axios

// =======================
// TAREAS DEL BACKEND
// =======================
const tareas = ref([]); // aquí guardamos todas las tareas del usuario

async function cargarTareas() {
  try {
    const res = await api.get("/tareas"); // GET http://localhost:5000/api/tareas
    tareas.value = res.data;
  } catch (e) {
    console.error("Error cargando tareas para el calendario", e);
  }
}

// Agrupamos tareas por fecha_limite -> { "2025-11-28": [tarea1, tarea2], ... }
const diaNotas = computed(() => {
  const mapa = {};
  for (const t of tareas.value) {
    // solo usamos las que tienen fecha_limite
    if (!t.fecha_limite) continue;
    if (!mapa[t.fecha_limite]) mapa[t.fecha_limite] = [];
    mapa[t.fecha_limite].push(t);
  }
  return mapa;
});

// =======================
// FECHAS Y SEMANAS
// =======================
const hoy = new Date();
const semanaActual = ref(0);

function obtenerLunes(offset = 0) {
  const fecha = new Date(hoy);
  const dia = fecha.getDay();
  const lunes = fecha.getDate() - (dia === 0 ? 6 : dia - 1);
  fecha.setDate(lunes + offset * 7);
  return fecha;
}

const semanaCompleta = computed(() => {
  const lunes = obtenerLunes(semanaActual.value);
  const dias = [];
  for (let i = 0; i < 7; i++) {
    const d = new Date(lunes);
    d.setDate(lunes.getDate() + i);
    dias.push({
      fecha: d,
      nombre: d.toLocaleDateString("es-ES", { weekday: "long" }),
      fechaTexto: d.toLocaleDateString("es-ES", { day: "numeric", month: "short" }),
      fechaISO: d.toISOString().split("T")[0],
    });
  }
  return dias;
});

const inicioSemana = computed(() => semanaCompleta.value[0].fecha);
const finSemana = computed(() => semanaCompleta.value[6].fecha);

function formatoFechaSemana(fecha) {
  return fecha.toLocaleDateString("es-ES", { day: "numeric", month: "short" });
}

// =======================
// NOTAS (CREAR DESDE CALENDARIO)
// =======================
const diaSeleccionado = ref("");
const nuevaNota = ref("");
const dialog = ref(false);

function abrirDialog(fechaISO) {
  diaSeleccionado.value = fechaISO;
  nuevaNota.value = "";
  dialog.value = true;
}

// ⬅️ AHORA GUARDAMOS EN EL BACK
async function guardarNota() {
  if (!nuevaNota.value.trim()) return;

  try {
    await api.post("/tareas", {
      titulo: "Nota del calendario",
      descripcion: nuevaNota.value,
      prioridad: "media",
      fecha_limite: diaSeleccionado.value, // clave para el calendario
    });

    dialog.value = false;
    nuevaNota.value = "";
    await cargarTareas(); // recargamos desde el back
  } catch (e) {
    console.error("Error guardando nota del calendario", e);
  }
}

// =======================
// NAVEGACIÓN SEMANAS
// =======================
function semanaAnterior() {
  semanaActual.value--;
}

function semanaSiguiente() {
  semanaActual.value++;
}

// =======================
// EXPANDIR DÍA
// =======================
const diaExpandido = ref(null);

function toggleExpand(fechaISO) {
  diaExpandido.value = diaExpandido.value === fechaISO ? null : fechaISO;
}

// =======================
// INICIO: CARGAR TAREAS
// =======================
onMounted(() => {
  cargarTareas();
});
</script>


<template>
  <div class="calendar-page">
    <div class="calendar-inner">
      
      <!-- CABECERA -->
      <div class="week-header">
        <v-btn icon @click="semanaAnterior">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>

        <h2 class="week-title">
          Semana del {{ formatoFechaSemana(inicioSemana) }}
          al {{ formatoFechaSemana(finSemana) }}
        </h2>

        <v-btn icon @click="semanaSiguiente">
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </div>

      <!-- GRID -->
      <div class="week-grid">
        <div
          v-for="dia in semanaCompleta"
          :key="dia.fechaISO"
          class="day-card"
          :class="{ expanded: diaExpandido === dia.fechaISO }"
          @click="toggleExpand(dia.fechaISO)"
        >
          <h3>{{ dia.nombre }}</h3>
          <p class="date-text">{{ dia.fechaTexto }}</p>

          <v-divider class="my-2" />

          <!-- NOTAS -->
          <div class="notes-box">
            <div
              v-for="(nota, i) in diaNotas[dia.fechaISO]"
              :key="i"
              class="note-item"
            >
              {{ nota }}
            </div>

            <div
              v-if="!diaNotas[dia.fechaISO] || diaNotas[dia.fechaISO].length === 0"
              class="empty-notes"
            >
              No hay notas
            </div>
          </div>

          <!-- BOTÓN AÑADIR -->
          <v-btn block color="primary" class="mt-2" @click.stop="abrirDialog(dia.fechaISO)">
            + Añadir nota
          </v-btn>
        </div>
      </div>

      <!-- DIALOGO -->
      <v-dialog v-model="dialog" max-width="400">
        <v-card class="papiro-modal">
          <v-card-title>Añadir nota</v-card-title>
          <v-card-text>
            <v-textarea v-model="nuevaNota" label="Contenido" />
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="dialog = false">Cancelar</v-btn>
            <v-btn text color="green" @click="guardarNota">Guardar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

    </div>
  </div>
</template>

<style scoped>
/* =====================
   CONTENEDOR PRINCIPAL - CENTRADO
   ===================== */
.calendar-page {
  background: #0f0f0f;
  min-height: calc(100vh - 64px);
  display: flex;
  justify-content: center;
  padding: 30px 20px;
  box-sizing: border-box;
}

.calendar-inner {
  width: 100%;
  max-width: 1400px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* =====================
   CABECERA
   ===================== */
.week-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  margin-bottom: 24px;
  width: 100%;
  animation: fadeWeek .45s ease;
}

.week-title {
  font-size: 26px;
  font-weight: bold;
  color: #fff;
}

/* =====================
   GRID SEMANAL - CENTRADO
   ===================== */
.week-grid {
  display: grid;
  grid-template-columns: repeat(7, minmax(180px, 1fr));
  gap: 18px;
  width: 100%;
  max-width: 1300px;
  box-sizing: border-box;
  animation: fadeWeek .45s ease;
}

@keyframes fadeWeek {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

/* =====================
   DÍA DEL CALENDARIO
   ===================== */
.day-card {
  background: #181818;
  border-radius: 14px;
  border: 1px solid #2e2e2e;
  padding: 18px;
  min-height: 420px;
  display: flex;
  flex-direction: column;
  transition: all .25s ease;
  cursor: pointer;
}

.day-card h3 {
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
  text-transform: capitalize;
}

.date-text {
  color: #888;
  font-size: 14px;
  margin-bottom: 8px;
}

.day-card:hover {
  transform: scale(1.03) rotate(0.3deg);
  border-color: #444;
}

/* EXPANDIDO */
.day-card.expanded {
  transform: scale(1.08) rotate(-0.4deg);
  min-height: 460px;
  z-index: 10;
  border: 3px solid rgba(255, 180, 80, 0.9);
  box-shadow: 0 25px 80px rgba(0,0,0,0.8);
  animation: expandMedieval .35s ease;
}

@keyframes expandMedieval {
  0% { transform: scale(0.92) rotate(0deg); opacity: 0.8; }
  100% { transform: scale(1.08) rotate(-0.4deg); opacity: 1; }
}

/* =====================
   CAJA DE NOTAS
   ===================== */
.notes-box {
  flex: 1;
  overflow-y: auto;
  margin: 10px 0;
  min-height: 100px;
}

.notes-box::-webkit-scrollbar {
  width: 6px;
}

.notes-box::-webkit-scrollbar-thumb {
  background: #333;
  border-radius: 4px;
}

/* =====================
   NOTAS ESTILO POST-IT MEDIEVAL
   ===================== */
.note-item {
  background-image: url("/textures/postit_ordedragon.png");
  background-size: cover;
  background-position: center;
  border-radius: 12px;
  border: 2px solid rgba(70, 40, 20, 0.55);
  padding: 14px;
  margin-bottom: 10px;
  color: #3b260f;
  font-family: "MedievalSharp", cursive;
  font-weight: bold;
  box-shadow: 0 8px 20px rgba(0,0,0,0.35);
  cursor: pointer;
  animation: popIn .35s ease;
  transition: transform .18s ease;
  word-wrap: break-word;
}

.note-item:hover {
  transform: scale(1.05);
}

@keyframes popIn {
  0% { transform: scale(0.75); opacity: 0; }
  80% { transform: scale(1.03); }
  100% { transform: scale(1); opacity: 1; }
}

.empty-notes {
  text-align: center;
  font-style: italic;
  color: #777;
  padding: 20px;
}

/* =====================
   MODAL ESTILO PAPIRO
   ===================== */
.papiro-modal {
  background-image: url("/textures/postit_ordedragon.png");
  background-size: cover;
  border: 3px solid rgba(70,40,20,0.9);
  box-shadow: 0 15px 40px rgba(0,0,0,0.5);
  animation: fadeSlide .35s ease;
}

@keyframes fadeSlide {
  0% { opacity: 0; transform: translateY(20px) scale(0.95); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}

/* =====================
   RESPONSIVE
   ===================== */
@media (max-width: 1200px) {
  .week-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
}

@media (max-width: 768px) {
  .calendar-page {
    padding: 20px 12px;
  }
  
  .week-header {
    margin-bottom: 16px;
  }
  
  .week-title {
    font-size: 20px;
  }
  
  .week-grid {
    gap: 12px;
  }
  
  .day-card {
    padding: 14px;
    min-height: 350px;
  }
}

@media (max-width: 600px) {
  .week-grid {
    grid-template-columns: 1fr;
  }
  
  .day-card {
    min-height: 300px;
  }
}
</style>