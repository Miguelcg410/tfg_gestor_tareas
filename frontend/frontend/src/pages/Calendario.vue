<script setup>
import { ref, computed } from "vue";

// =======================
// NOTAS (localStorage)
// =======================
const notas = ref(JSON.parse(localStorage.getItem("notasCalendario") || "{}"));
function guardarNotas() {
  localStorage.setItem("notasCalendario", JSON.stringify(notas.value));
}

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
// Notas
// =======================
const diaSeleccionado = ref("");
const nuevaNota = ref("");
const dialog = ref(false);

function abrirDialog(fechaISO) {
  diaSeleccionado.value = fechaISO;
  nuevaNota.value = "";
  dialog.value = true;
}

function guardarNota() {
  if (!notas.value[diaSeleccionado.value]) {
    notas.value[diaSeleccionado.value] = [];
  }
  notas.value[diaSeleccionado.value].push(nuevaNota.value);
  dialog.value = false;
  guardarNotas();
}

function semanaAnterior() {
  semanaActual.value--;
}

function semanaSiguiente() {
  semanaActual.value++;
}

const diaNotas = computed(() => {
  return notas.value;
});
</script>

<template>
  <div class="calendar-page-wrapper">
    <div class="calendar-page">
      <div class="calendar-inner">
        <!-- CABECERA -->
        <div class="week-header">
          <v-btn icon @click="semanaAnterior"><v-icon>mdi-chevron-left</v-icon></v-btn>
          <h2 class="week-title">
            Semana del {{ formatoFechaSemana(inicioSemana) }}
            al {{ formatoFechaSemana(finSemana) }}
          </h2>
          <v-btn icon @click="semanaSiguiente"><v-icon>mdi-chevron-right</v-icon></v-btn>
        </div>

        <!-- GRID DE LA SEMANA -->
        <div class="week-grid">
          <div
            v-for="dia in semanaCompleta"
            :key="dia.fechaISO"
            class="day-card"
          >
            <h3>{{ dia.nombre }}</h3>
            <p class="date-text">{{ dia.fechaTexto }}</p>
            <v-divider class="my-2" />
            <div class="notes-box">
              <div
                v-for="(nota, i) in diaNotas[dia.fechaISO]"
                :key="i"
                class="note-item"
              >
                {{ nota }}
              </div>
            </div>
            <v-btn block color="primary" class="mt-2" @click="abrirDialog(dia.fechaISO)">
              + Añadir nota
            </v-btn>
          </div>
        </div>
      </div>

      <!-- DIALOGO NOTA -->
      <v-dialog v-model="dialog" max-width="400">
        <v-card>
          <v-card-title>Añadir nota</v-card-title>
          <v-card-text>
            <v-textarea v-model="nuevaNota" label="Contenido de la nota" />
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="dialog = false">Cancelar</v-btn>
            <v-btn text color="primary" @click="guardarNota">Guardar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<style scoped>
/* ========================================
   WRAPPER - Anula estilos del padre
   ======================================== */
.calendar-page-wrapper {
  position: fixed;
  top: 64px;
  left: 0;
  right: 0;
  bottom: 0;
  margin: 0 !important;
  padding: 0 !important;
  max-width: none !important;
}

/* ========================================
   PÁGINA COMPLETA - SIN MÁRGENES
   ======================================== */
.calendar-page {
  background: #0f0f0f;
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  padding: 0 !important;
  margin: 0 !important;
  overflow: hidden;
}

/* Contenedor interno: SIN padding lateral */
.calendar-inner {
  flex: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  overflow: hidden;
}

/* ========================================
   CABECERA
   ======================================== */
.week-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  margin: 20px 0;
  padding: 0;
  flex-shrink: 0;
}

.week-title {
  font-size: 26px;
  font-weight: bold;
  text-align: center;
  color: #fff;
}

.week-header .v-btn {
  height: 44px;
  width: 44px;
}

/* ========================================
   GRID - CERO padding lateral
   ======================================== */
.week-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 12px;
  overflow-y: auto;
  padding: 0 8px 8px 8px;
  margin: 0;
  box-sizing: border-box;
}

/* Scroll personalizado */
.week-grid::-webkit-scrollbar {
  width: 8px;
}

.week-grid::-webkit-scrollbar-thumb {
  background: #333;
  border-radius: 8px;
}

.week-grid::-webkit-scrollbar-track {
  background: #1a1a1a;
}

/* ========================================
   TARJETAS DE DÍAS
   ======================================== */
.day-card {
  background: #181818;
  border-radius: 14px;
  padding: 18px;
  border: 1px solid #2e2e2e;
  display: flex;
  flex-direction: column;
  min-height: 0;
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

/* Caja de notas - crece para llenar espacio */
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

/* Nota individual */
.note-item {
  background: #252525;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 8px;
  color: #ddd;
  font-size: 14px;
  word-wrap: break-word;
}

/* Botón de añadir nota */
.day-card .v-btn {
  flex-shrink: 0;
}

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 1200px) {
  .week-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
}

@media (max-width: 768px) {
  .week-header {
    margin: 16px 0;
  }
  
  .week-title {
    font-size: 20px;
  }
  
  .week-grid {
    gap: 10px;
    padding: 0 6px 6px 6px;
  }
  
  .day-card {
    padding: 14px;
  }
}

@media (max-width: 600px) {
  .week-grid {
    grid-template-columns: 1fr;
    padding: 0 4px 4px 4px;
  }
  
  .day-card {
    min-height: 300px;
  }
}
</style>