<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../services/api";

// ----- Estado -----
const focused = ref(new Date()); // fecha que determina la semana mostrada (any day inside the week)
const weekDates = ref([]); // array de fechas (YYYY-MM-DD) para el lunes->domingo de la semana
const tareas = ref([]); // todas las tareas desde backend
const notasPorFecha = ref({}); // notas locales cargadas desde localStorage
const nuevaNotaMap = ref({}); // texto temporal por día para el input

const NOTES_KEY = "gestor_calendario_notes_v1";

// ----- utilidades de fecha -----
function toDateKey(d) {
  if (!d) return null;
  const dt = d instanceof Date ? d : new Date(d);
  // convertir a YYYY-MM-DD en zona local
  const yyyy = dt.getFullYear();
  const mm = String(dt.getMonth() + 1).padStart(2, "0");
  const dd = String(dt.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

function startOfWeek(date) {
  // queremos lunes como primer día
  const d = new Date(date);
  const day = d.getDay(); // 0 dom ... 6 sab
  const diffToMonday = (day === 0) ? -6 : 1 - day; // si domingo -> volver 6 días para lunes
  const monday = new Date(d);
  monday.setDate(d.getDate() + diffToMonday);
  monday.setHours(0,0,0,0);
  return monday;
}

function buildWeekDates(dateInWeek) {
  const monday = startOfWeek(dateInWeek);
  const arr = [];
  for (let i = 0; i < 7; i++) {
    const dd = new Date(monday);
    dd.setDate(monday.getDate() + i);
    arr.push(toDateKey(dd));
  }
  return arr;
}

function formatDayLabel(dateKey) {
  const d = new Date(dateKey);
  // Ej: Lun 10 Feb
  return d.toLocaleDateString("es-ES", { weekday: "short", day: "numeric", month: "short" });
}

function isPast(dateKey) {
  const todayKey = toDateKey(new Date());
  return new Date(dateKey) < new Date(todayKey);
}

// ----- localStorage notas -----
function loadNotes() {
  try {
    const raw = localStorage.getItem(NOTES_KEY);
    notasPorFecha.value = raw ? JSON.parse(raw) : {};
  } catch (e) {
    console.error("Error leyendo notas localStorage", e);
    notasPorFecha.value = {};
  }
}

function saveNotes() {
  try {
    localStorage.setItem(NOTES_KEY, JSON.stringify(notasPorFecha.value));
  } catch (e) {
    console.error("Error guardando notas localStorage", e);
  }
}

function addNote(dateKey) {
  const text = (nuevaNotaMap.value[dateKey] || "").trim();
  if (!text) return;
  if (!notasPorFecha.value[dateKey]) notasPorFecha.value[dateKey] = [];
  notasPorFecha.value[dateKey].push({
    id: Date.now() + Math.floor(Math.random() * 999),
    text,
    created_at: new Date().toISOString()
  });
  nuevaNotaMap.value[dateKey] = "";
  saveNotes();
}

function deleteNote(dateKey, id) {
  if (!notasPorFecha.value[dateKey]) return;
  notasPorFecha.value[dateKey] = notasPorFecha.value[dateKey].filter(n => n.id !== id);
  saveNotes();
}

// ----- tareas (desde backend) -----
async function cargarTareas() {
  try {
    const res = await api.get("/tareas");
    tareas.value = res.data || [];
  } catch (e) {
    console.error("Error cargando tareas:", e);
    tareas.value = [];
  }
}

function tareasParaFecha(dateKey) {
  return tareas.value.filter(t => {
    if (!t.fecha_limite) return false;
    const key = toDateKey(t.fecha_limite);
    return key === dateKey;
  });
}

// ----- navegación semana -----
function shiftWeeks(n) {
  const d = new Date(focused.value);
  d.setDate(d.getDate() + n * 7);
  focused.value = d;
  weekDates.value = buildWeekDates(focused.value);
}

function goToday() {
  focused.value = new Date();
  weekDates.value = buildWeekDates(focused.value);
}

// ----- computed útiles -----
const weekRangeLabel = computed(() => {
  if (!weekDates.value.length) return "";
  const first = new Date(weekDates.value[0]);
  const last = new Date(weekDates.value[6]);
  const formattedFirst = first.toLocaleDateString("es-ES", { day: "numeric", month: "short" });
  const formattedLast = last.toLocaleDateString("es-ES", { day: "numeric", month: "short", year: "numeric" });
  return `${formattedFirst} — ${formattedLast}`;
});

// iniciar
onMounted(async () => {
  weekDates.value = buildWeekDates(focused.value);
  loadNotes();
  await cargarTareas();
  // inicializar inputs vacíos para cada día
  weekDates.value.forEach(k => { nuevaNotaMap.value[k] = ""; });
});
</script>

<template>
  <v-container fluid class="pa-4">
    <!-- cabecera con navegación -->
    <div class="d-flex align-center mb-4 header-row">
      <div class="d-flex align-center">
        <v-btn icon variant="tonal" @click="shiftWeeks(-1)" title="Semana anterior">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
        <v-btn variant="tonal" class="mx-2" @click="goToday">Hoy</v-btn>
        <v-btn icon variant="tonal" @click="shiftWeeks(1)" title="Semana siguiente">
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </div>

      <div class="mx-4 title-range">
        <h3 class="mb-0">Semana: {{ weekRangeLabel }}</h3>
        <div class="text-caption">Lunes → Domingo</div>
      </div>

      <v-spacer />

      <div>
        <v-btn variant="outlined" color="primary" @click="() => { weekDates = buildWeekDates(new Date()); }">
          Reiniciar semana
        </v-btn>
      </div>
    </div>

    <!-- fila semanal horizontal (scrollable) -->
    <div class="week-row" ref="weekRow">
      <div
        v-for="dateKey in weekDates"
        :key="dateKey"
        class="day-card"
        :class="{ past: isPast(dateKey) }"
      >
        <div class="day-header d-flex align-center">
          <div>
            <div class="day-name">{{ formatDayLabel(dateKey) }}</div>
            <div class="day-sub">{{ new Date(dateKey).toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric' }) }}</div>
          </div>
          <v-spacer />
          <div>
            <v-chip small>{{ (tareasParaFecha(dateKey) || []).length }} tareas</v-chip>
          </div>
        </div>

        <div class="day-body">
          <!-- tareas del día -->
          <div v-if="tareasParaFecha(dateKey).length === 0" class="no-tasks text-caption">Sin tareas</div>

          <div v-else>
            <v-list dense class="task-list">
              <v-list-item
                v-for="t in tareasParaFecha(dateKey)"
                :key="t.id"
                class="task-item"
              >
                <v-list-item-content>
                  <v-list-item-title :class="{ overdue: (new Date(t.fecha_limite) < new Date() && !t.completada) }">
                    {{ t.titulo }}
                  </v-list-item-title>
                  <v-list-item-subtitle class="text-caption">{{ t.descripcion }}</v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action>
                  <v-chip small :color="t.prioridad === 'alta' ? 'error' : t.prioridad === 'media' ? 'warning' : 'success'" text-color="white">
                    {{ t.prioridad }}
                  </v-chip>
                </v-list-item-action>
              </v-list-item>
            </v-list>
          </div>

          <v-divider class="my-2"></v-divider>

          <!-- notas del día -->
          <div class="notes-title mb-2">Notas</div>
          <div v-if="!(notasPorFecha[dateKey] && notasPorFecha[dateKey].length)">
            <div class="text-caption">Sin notas</div>
          </div>

          <v-list dense class="notes-list" v-else>
            <v-list-item v-for="n in (notasPorFecha[dateKey] || [])" :key="n.id">
              <v-list-item-content>
                <v-list-item-title class="note-text">{{ n.text }}</v-list-item-title>
                <v-list-item-subtitle class="text-caption">{{ new Date(n.created_at).toLocaleString('es-ES') }}</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn icon small color="red" @click="deleteNote(dateKey, n.id)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>

          <!-- añadir nota inline -->
          <v-textarea
            v-model="nuevaNotaMap[dateKey]"
            rows="2"
            placeholder="Añadir nota..."
            class="mt-2"
            density="compact"
          />
          <v-btn small color="primary" class="mt-2" @click="addNote(dateKey)">Agregar nota</v-btn>
        </div>
      </div>
    </div>
  </v-container>
</template>

<style scoped>
/* layout general */
.header-row .title-range h3 { margin: 0; color: white; }
.header-row .title-range .text-caption { color: rgba(255,255,255,0.6); }

.week-row {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 10px;
  margin-top: 6px;
  -webkit-overflow-scrolling: touch;
}

/* cada día (columna) */
.day-card {
  min-width: 360px;
  max-width: 360px;
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border-radius: 12px;
  padding: 14px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.45);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* día pasado */
.day-card.past {
  opacity: 0.9;
  filter: grayscale(0.02);
}

/* encabezado del día */
.day-header .day-name {
  font-weight: 800;
  font-size: 15px;
  color: white;
}
.day-header .day-sub {
  font-size: 12px;
  color: rgba(255,255,255,0.65);
}

/* body */
.day-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 420px;
  overflow-y: auto;
}

/* tareas */
.task-list .v-list-item {
  padding: 6px 0;
}
.task-item .v-list-item-title {
  font-weight: 700;
  color: white;
}
.overdue {
  text-decoration: line-through;
  color: rgba(255,255,255,0.55);
}

/* notas */
.notes-title {
  font-weight: 700;
  color: white;
}
.note-text {
  color: rgba(255,255,255,0.92);
}

/* textarea */
.v-textarea textarea {
  background: rgba(0,0,0,0.22) !important;
  color: white !important;
  border-radius: 8px;
  padding: 8px;
}

/* botones */
.v-btn {
  text-transform: none;
}

/* responsive: en pantallas pequeñas reduce min-width */
@media (max-width: 900px) {
  .day-card { min-width: 300px; max-width: 300px; }
}
</style>
