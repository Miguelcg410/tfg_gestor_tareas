<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../services/api";

// =======================
// NOTA SELECCIONADA
// =======================
const notaSeleccionada = ref(null);
const dialogNota = ref(false);

function abrirNota(nota) {
  notaSeleccionada.value = nota;
  dialogNota.value = true;
}

// =======================
// TAREAS DEL BACKEND
// =======================
const tareas = ref([]);

async function cargarTareas() {
  try {
    const res = await api.get("/tareas");
    tareas.value = res.data;
  } catch (e) {
    console.error("Error cargando tareas para el calendario", e);
  }
}

// Agrupamos tareas por fecha_limite
const diaNotas = computed(() => {
  const mapa = {};
  for (const t of tareas.value) {
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

function formatoFechaSemana(f) {
  return f.toLocaleDateString("es-ES", { day: "numeric", month: "short" });
}

// =======================
// CREAR NOTA
// =======================
const diaSeleccionado = ref("");
const nuevaNota = ref("");
const dialog = ref(false);

function abrirDialog(fechaISO) {
  diaSeleccionado.value = fechaISO;
  nuevaNota.value = "";
  dialog.value = true;
}

async function guardarNota() {
  if (!nuevaNota.value.trim()) return;

  try {
    await api.post("/tareas", {
      titulo: "Nota del calendario",
      descripcion: nuevaNota.value,
      prioridad: "media",
      fecha_limite: diaSeleccionado.value,
    });
    dialog.value = false;
    nuevaNota.value = "";
    await cargarTareas();
  } catch (e) {
    console.error("Error guardando nota", e);
  }
}

// =======================
// EXPANDIR DÍA
// =======================
const diaExpandido = ref(null);

function toggleExpand(fechaISO) {
  diaExpandido.value = diaExpandido.value === fechaISO ? null : fechaISO;
}

// =======================
// NAVEGAR SEMANAS (FALTABA)
// =======================
function semanaAnterior() {
  semanaActual.value--;
}

function semanaSiguiente() {
  semanaActual.value++;
}

// =======================
// INICIO
// =======================
onMounted(() => cargarTareas());
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

          <!-- CAJA DE NOTAS -->
          <div class="notes-box">
            <div
              v-for="(nota, i) in diaNotas[dia.fechaISO]"
              :key="i"
              class="note-item"
              @click.stop="abrirNota(nota)"
            >
              <div class="nota-titulo">{{ nota.titulo }}</div>
              <div class="nota-desc">{{ nota.descripcion }}</div>
              <div class="nota-prio">Prioridad: {{ nota.prioridad }}</div>
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


      <!-- MODAL NOTA AMPLIADA -->
      <v-dialog v-model="dialogNota" max-width="480">
        <v-card class="nota-expandida">

          <div class="sello-arcano"></div>

          <v-card-title class="titulo-expandido">
            {{ notaSeleccionada?.titulo }}
          </v-card-title>

          <v-card-text class="cuerpo-nota">
            <p class="desc-expandida">{{ notaSeleccionada?.descripcion }}</p>

            <p class="meta-expandida">
              Prioridad: <strong>{{ notaSeleccionada?.prioridad }}</strong>
            </p>

            <p class="meta-expandida">
              Fecha: <strong>{{ notaSeleccionada?.fecha_limite }}</strong>
            </p>
          </v-card-text>

          <v-card-actions class="acciones-modal">
            <v-spacer />
            <v-btn color="red" class="cerrar-btn" @click="dialogNota = false">Cerrar</v-btn>
          </v-card-actions>

        </v-card>
      </v-dialog>


      <!-- MODAL AÑADIR NOTA -->
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
/* =======================
   ESTILOS
======================= */

.nota-titulo { font-weight: bold; font-size: 15px; color: #2b1a0c; }
.nota-desc { font-size: 13px; opacity: 0.8; margin-bottom: 6px; }
.nota-prio { font-size: 11px; color: #5a3b1e; }

/* Page */
.calendar-page {
  background: #0f0f0f;
  min-height: calc(100vh - 64px);
  display: flex; justify-content: center;
  padding: 30px 20px;
}

.calendar-inner { max-width: 1400px; width: 100%; }

/* Week header */
.week-header {
  display: flex; align-items: center; justify-content: center;
  gap: 24px; margin-bottom: 24px;
}

.week-title { color: white; }

/* Grid */
.week-grid {
  display: grid;
  grid-template-columns: repeat(7, minmax(180px, 1fr));
  gap: 18px;
}

/* Card */
.day-card {
  background: #181818;
  border-radius: 14px;
  padding: 18px;
  min-height: 420px;
  transition: 0.25s;
  cursor: pointer;
  border: 1px solid #2e2e2e;
}

.day-card.expanded {
  transform: scale(1.08);
  border: 3px solid #c78a3a;
  box-shadow: 0 25px 80px rgba(0,0,0,0.8);
}

/* Notes */
.note-item {
  background-image: url("/textures/postit_ordedragon.png");
  background-size: cover;
  border-radius: 12px;
  border: 2px solid rgba(70,40,20,0.55);
  padding: 14px;
  margin-bottom: 10px;
  font-family: "MedievalSharp";
  font-weight: bold;
  cursor: pointer;
}

.empty-notes { text-align: center; padding: 20px; color: #777; }

/* ==========================
   MODAL EXPANDIDO
========================== */

.nota-expandida {
  position: relative;
  background-image: url("/textures/postit_ordedragon.png");
  background-size: cover;
  border-radius: 24px;
  padding: 20px;
  border: 3px solid rgba(90,40,15,0.85);
  box-shadow: 0 0 22px rgba(255,150,60,0.35),
              0 0 40px rgba(255,100,20,0.18);
}

.sello-arcano {
  position: absolute;
  top: -18px;
  right: -18px;
  width: 110px;
  height: 110px;

  /* 🔥 hace el sello totalmente redondo */
  border-radius: 50%;
  overflow: hidden;

  /* imagen del sello */
  background-image: url("/icons/orderdragon.png");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;

  /* efecto */
  opacity: 0.5;
  animation: spin 8s linear infinite;

  /* luz alrededor */
  box-shadow: 0 0 12px rgba(255, 180, 80, 0.45);
  filter: drop-shadow(0 0 4px rgba(255,200,120,0.35));

  pointer-events: none;
}


@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Modal text */
.titulo-expandido {
  text-align: center;
  font-size: 22px;
  margin-bottom: 10px;
  color: #3b260f;
}

.desc-expandida { font-size: 16px; margin-bottom: 12px; }
.meta-expandida { font-size: 14px; }

/* Cerrar */
.cerrar-btn {
  background: rgba(150,0,0,0.9) !important;
  color: white !important;
  font-weight: bold;
}
</style>
