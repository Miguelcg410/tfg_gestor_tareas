<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../services/api";

/* ======================================================
   FORMATOS DE FECHA (FIX PRINCIPAL)
====================================================== */
function toISODateLocal(date) {
  const d = new Date(date);
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
  return d.toISOString().split("T")[0];
}

/* ======================================================
   ESTADO Y MODOS
====================================================== */
const modoVista = ref("semana");

/* ======================================================
   NOTAS
====================================================== */
const notaSeleccionada = ref(null);
const dialogNota = ref(false);
const editando = ref(false);

const notaEditada = ref({
  titulo: "",
  descripcion: "",
  prioridad: "",
});

function abrirNota(nota) {
  notaSeleccionada.value = nota;
  notaEditada.value = {
    titulo: nota.titulo,
    descripcion: nota.descripcion,
    prioridad: nota.prioridad,
  };
  editando.value = false;
  dialogNota.value = true;
}

async function guardarCambiosNota() {
  if (!notaSeleccionada.value) return;

  try {
    await api.put(`/tareas/${notaSeleccionada.value.id}`, {
      ...notaEditada.value,
      fecha_limite: notaSeleccionada.value.fecha_limite,
    });

    dialogNota.value = false;
    await cargarTareas();
  } catch (e) {
    console.error("Error actualizando nota", e);
  }
}

async function eliminarNota() {
  if (!notaSeleccionada.value) return;

  if (!confirm("¿Seguro que quieres eliminar esta nota?")) return;

  try {
    await api.delete(`/tareas/${notaSeleccionada.value.id}`);
    dialogNota.value = false;
    await cargarTareas();
  } catch (e) {
    console.error("Error eliminando nota", e);
  }
}

/* ======================================================
   TAREAS DEL BACKEND
====================================================== */
const tareas = ref([]);

async function cargarTareas() {
  try {
    const res = await api.get("/tareas");

    tareas.value = res.data.map(t => ({
      ...t,
      fecha_limite: toISODateLocal(t.fecha_limite)
    }));
  } catch (e) {
    console.error("Error cargando tareas", e);
  }
}

const diaNotas = computed(() => {
  const mapa = {};
  for (const t of tareas.value) {
    if (!t.fecha_limite) continue;
    if (!mapa[t.fecha_limite]) mapa[t.fecha_limite] = [];
    mapa[t.fecha_limite].push(t);
  }
  return mapa;
});

/* ======================================================
   VISTA SEMANAL
====================================================== */

const hoy = new Date();
const semanaActual = ref(0);

function obtenerLunes(offset) {
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
      fechaISO: toISODateLocal(d),
    });
  }

  return dias;
});

const inicioSemana = computed(() => semanaCompleta.value[0].fecha);
const finSemana = computed(() => semanaCompleta.value[6].fecha);

/* ======================================================
   VISTA MENSUAL
====================================================== */

const mesActual = ref(new Date().getMonth());
const anioActual = ref(new Date().getFullYear());

const mesCompleto = computed(() => {
  const primerDia = new Date(anioActual.value, mesActual.value, 1);
  const ultimoDia = new Date(anioActual.value, mesActual.value + 1, 0);

  const dias = [];

  const diaSemana = primerDia.getDay() || 7;
  for (let i = diaSemana - 2; i >= 0; i--) {
    const d = new Date(primerDia);
    d.setDate(d.getDate() - i - 1);
    dias.push({
      fecha: d,
      dia: d.getDate(),
      fechaISO: toISODateLocal(d),
      mesActual: false,
    });
  }

  for (let i = 1; i <= ultimoDia.getDate(); i++) {
    const d = new Date(anioActual.value, mesActual.value, i);
    dias.push({
      fecha: d,
      dia: i,
      fechaISO: toISODateLocal(d),
      mesActual: true,
    });
  }

  while (dias.length < 42) {
    const last = dias[dias.length - 1].fecha;
    const d = new Date(last);
    d.setDate(d.getDate() + 1);

    dias.push({
      fecha: d,
      dia: d.getDate(),
      fechaISO: toISODateLocal(d),
      mesActual: false,
    });
  }

  return dias;
});

const nombreMes = computed(() => {
  const fecha = new Date(anioActual.value, mesActual.value, 1);
  return fecha.toLocaleDateString("es-ES", { month: "long", year: "numeric" });
});

function mesAnterior() {
  if (mesActual.value === 0) {
    mesActual.value = 11;
    anioActual.value--;
  } else mesActual.value--;
}

function mesSiguiente() {
  if (mesActual.value === 11) {
    mesActual.value = 0;
    anioActual.value++;
  } else mesActual.value++;
}

/* ======================================================
   CREAR NOTAS
====================================================== */
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

/* ======================================================
   EXPANDIR DÍA
====================================================== */
const diaExpandido = ref(null);

function toggleExpand(fechaISO) {
  diaExpandido.value = diaExpandido.value === fechaISO ? null : fechaISO;
}

/* ======================================================
   NAVEGAR
====================================================== */
function semanaAnterior() { semanaActual.value--; }
function semanaSiguiente() { semanaActual.value++; }

/* ======================================================
   INICIO
====================================================== */
onMounted(() => cargarTareas());
</script>

<template>
  <div class="calendar-page">
    <div class="calendar-inner">

      <!-- CABECERA -->
      <div class="week-header">
        <v-btn icon class="nav-week-btn" @click="modoVista === 'semana' ? semanaAnterior() : mesAnterior()">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>

        <div class="header-center">
  <h2 class="week-title">
    {{ modoVista === "semana"
      ? `Semana del ${inicioSemana.toLocaleDateString('es-ES')} al ${finSemana.toLocaleDateString('es-ES')}`
      : nombreMes
    }}
  </h2>
</div>

<div class="view-right">
  <div class="view-selector">
    <v-btn
      :class="['view-btn', { active: modoVista === 'semana' }]"
      @click="modoVista = 'semana'"
      size="small"
    >
      <v-icon left size="18">mdi-calendar-week</v-icon>
      Semana
    </v-btn>

    <v-btn
      :class="['view-btn', { active: modoVista === 'mes' }]"
      @click="modoVista = 'mes'"
      size="small"
    >
      <v-icon left size="18">mdi-calendar-month</v-icon>
      Mes
    </v-btn>
  </div>
</div>


        <v-btn icon class="nav-week-btn" @click="modoVista === 'semana' ? semanaSiguiente() : mesSiguiente()">
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </div>

      <!-- ================= VISTA SEMANAL ================= -->
      <div v-if="modoVista === 'semana'" class="week-grid">
        <div
          v-for="dia in semanaCompleta"
          :key="dia.fechaISO"
          class="day-card"
          :class="{ expanded: diaExpandido === dia.fechaISO }"
          @click="toggleExpand(dia.fechaISO)"
        >
          <div class="day-header">
            <h3 class="day-name">{{ dia.nombre }}</h3>
            <p class="date-text">{{ dia.fechaTexto }}</p>
          </div>

          <v-divider class="my-2 divider-custom" />

          <div class="notes-box">
            <div
              v-for="(nota, i) in diaNotas[dia.fechaISO]"
              :key="i"
              class="note-item"
              @click.stop="abrirNota(nota)"
            >
              <div class="nota-titulo">{{ nota.titulo }}</div>
              <div class="nota-desc">{{ nota.descripcion }}</div>
              <div class="nota-prio">
                <span class="prio-badge" :class="`prio-${nota.prioridad}`">
                  {{ nota.prioridad }}
                </span>
              </div>
            </div>

            <div v-if="!diaNotas[dia.fechaISO]" class="empty-notes">
              📜 No hay notas
            </div>
          </div>

          <v-btn block class="add-note-btn mt-2" @click.stop="abrirDialog(dia.fechaISO)">
            <v-icon left>mdi-plus-circle</v-icon>
            Añadir nota
          </v-btn>
        </div>
      </div>

      <!-- ================= VISTA MENSUAL ================= -->
      <div v-else class="month-view">

        <div class="month-header">
          <div class="day-name-cell">Lun</div>
          <div class="day-name-cell">Mar</div>
          <div class="day-name-cell">Mié</div>
          <div class="day-name-cell">Jue</div>
          <div class="day-name-cell">Vie</div>
          <div class="day-name-cell">Sáb</div>
          <div class="day-name-cell">Dom</div>
        </div>

        <div class="month-grid">
          <div
            v-for="dia in mesCompleto"
            :key="dia.fechaISO"
            class="month-day-card"
            :class="{
              'not-current-month': !dia.mesActual,
              'has-notes': diaNotas[dia.fechaISO]
            }"
            @click="abrirDialog(dia.fechaISO)"
          >
            <div class="month-day-number">{{ dia.dia }}</div>

            <div class="month-notes-mini">
              <div
                v-for="(nota, i) in (diaNotas[dia.fechaISO] || []).slice(0, 3)"
                :key="i"
                class="mini-note"
                :class="`mini-note-${nota.prioridad}`"
                @click.stop="abrirNota(nota)"
              >
                {{ nota.titulo }}
              </div>

              <div
                v-if="diaNotas[dia.fechaISO] && diaNotas[dia.fechaISO].length > 3"
                class="more-notes"
              >
                +{{ diaNotas[dia.fechaISO].length - 3 }} más
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- MODAL NOTA -->
      <v-dialog v-model="dialogNota" max-width="520">
        <v-card class="nota-expandida">
          
          <v-card-title class="titulo-expandido">
            🐉 {{ editando ? "Editar Nota" : notaSeleccionada?.titulo }}
          </v-card-title>

          <v-card-text class="cuerpo-nota">

            <template v-if="!editando">
              <div class="desc-expandida">{{ notaSeleccionada?.descripcion }}</div>

              <div class="meta-info">
                <div class="meta-item">
                  <v-icon size="18">mdi-flag</v-icon>
                  Prioridad:
                  <span class="prio-badge-modal" :class="`prio-${notaSeleccionada?.prioridad}`">
                    {{ notaSeleccionada?.prioridad }}
                  </span>
                </div>

                <div class="meta-item">
                  <v-icon size="18">mdi-calendar</v-icon>
                  Fecha: <strong>{{ notaSeleccionada?.fecha_limite }}</strong>
                </div>
              </div>
            </template>

            <template v-else>
              <v-text-field label="Título" v-model="notaEditada.titulo" variant="outlined" class="mb-3" />

              <v-textarea label="Descripción" v-model="notaEditada.descripcion" variant="outlined" rows="4" />

              <v-select
                label="Prioridad"
                v-model="notaEditada.prioridad"
                :items="['alta','media','baja']"
                variant="outlined"
              />
            </template>

          </v-card-text>

          <v-card-actions class="acciones-modal">
            <v-spacer />

            <v-btn class="cerrar-btn" @click="dialogNota = false">
              <v-icon left>mdi-close-circle</v-icon>
              Cerrar
            </v-btn>

            <v-btn class="delete-btn" @click="eliminarNota">
              <v-icon left>mdi-trash-can</v-icon>
              Eliminar
            </v-btn>

            <v-btn v-if="!editando" class="save-btn" @click="editando = true">
              <v-icon left>mdi-pencil</v-icon>
              Editar
            </v-btn>

            <v-btn v-else class="save-btn" @click="guardarCambiosNota">
              <v-icon left>mdi-content-save</v-icon>
              Guardar
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- MODAL AÑADIR NOTA -->
      <v-dialog v-model="dialog" max-width="450">
        <v-card class="papiro-modal">
          <v-card-title class="modal-title">
            <v-icon left>mdi-feather</v-icon>
            Añadir nota
          </v-card-title>

          <v-card-text>
            <v-textarea v-model="nuevaNota" label="Escribe tu nota aquí..." rows="4" variant="outlined" />
          </v-card-text>

          <v-card-actions class="modal-actions">
            <v-btn text class="cancel-btn" @click="dialog = false">
              Cancelar
            </v-btn>
            <v-btn class="save-btn" @click="guardarNota">
              <v-icon left>mdi-content-save</v-icon>
              Guardar
            </v-btn>
          </v-card-actions>

        </v-card>
      </v-dialog>

    </div>
  </div>
</template>

<style scoped>
/* =======================
   PAGE & LAYOUT
======================= */
.calendar-page {
  background: #0f0f0f;
  min-height: calc(100vh - 64px);
  display: flex;
  justify-content: center;
  padding: 30px 20px;
}

.calendar-inner {
  max-width: 1400px;
  width: 100%;
}

/* =======================
   WEEK HEADER
======================= */
.week-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 30px;
  margin-bottom: 30px;
  animation: fadeSlideDown 0.6s ease;
}

@keyframes fadeSlideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.week-title {
  color: #ffe7cf;
  font-size: 28px;
  font-weight: 700;
  font-family: "Cinzel", serif;
  text-shadow: 0 0 15px rgba(255, 170, 80, 0.5);
  letter-spacing: 0.5px;
}

.nav-week-btn {
  background: rgba(255, 170, 80, 0.1) !important;
  border: 2px solid rgba(255, 170, 80, 0.3);
  transition: all 0.3s ease;
}

.nav-week-btn:hover {
  background: rgba(255, 170, 80, 0.25) !important;
  border-color: rgba(255, 170, 80, 0.6);
  transform: scale(1.1);
  box-shadow: 0 0 20px rgba(255, 170, 80, 0.4);
}

/* =======================
   WEEK GRID
======================= */
.week-grid {
  display: grid;
  grid-template-columns: repeat(7, minmax(180px, 1fr));
  gap: 20px;
  animation: fadeIn 0.8s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* =======================
   DAY CARD
======================= */
.day-card {
  background: linear-gradient(145deg, #1a1a1a 0%, #151515 100%);
  border-radius: 16px;
  padding: 20px;
  min-height: 450px;
  border: 2px solid #2e2e2e;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
}

/* Brillo sutil en hover */
.day-card::before {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,170,80,0.08) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.day-card:hover::before {
  opacity: 1;
}

.day-card:hover {
  transform: translateY(-8px) scale(1.02);
  border-color: rgba(255, 170, 80, 0.5);
  box-shadow: 
    0 12px 30px rgba(0, 0, 0, 0.5),
    0 0 25px rgba(255, 170, 80, 0.15);
}

/* EXPANDIDO */
.day-card.expanded {
  transform: scale(1.08) rotate(-0.5deg);
  border: 3px solid rgba(255, 180, 80, 0.9);
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.7),
    0 0 40px rgba(255, 170, 80, 0.4);
  z-index: 100;
  animation: expandPulse 0.4s ease;
}

@keyframes expandPulse {
  0% {
    transform: scale(0.95);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1.08) rotate(-0.5deg);
  }
}

/* =======================
   DAY HEADER
======================= */
.day-header {
  margin-bottom: 12px;
}

.day-name {
  color: #ffe7cf;
  font-size: 20px;
  font-weight: 700;
  text-transform: capitalize;
  margin-bottom: 4px;
  font-family: "Cinzel", serif;
}

.date-text {
  color: #999;
  font-size: 14px;
  font-weight: 500;
}

.divider-custom {
  border-color: rgba(255, 170, 80, 0.2) !important;
}

/* =======================
   NOTES BOX
======================= */
.notes-box {
  flex: 1;
  overflow-y: auto;
  margin: 12px 0;
  padding-right: 4px;
}

.notes-box::-webkit-scrollbar {
  width: 6px;
}

.notes-box::-webkit-scrollbar-thumb {
  background: rgba(255, 170, 80, 0.3);
  border-radius: 10px;
}

.notes-box::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 170, 80, 0.5);
}

/* =======================
   NOTE ITEM
======================= */
.note-item {
  background-image: url("/textures/postit_ordedragon.png");
  background-size: cover;
  border-radius: 14px;
  border: 2px solid rgba(70, 40, 20, 0.6);
  padding: 16px;
  margin-bottom: 12px;
  font-family: "MedievalSharp", cursive;
  cursor: pointer;
  position: relative;
  transition: all 0.25s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.note-item:hover {
  transform: translateY(-3px) scale(1.03) rotate(1deg);
  box-shadow: 
    0 8px 20px rgba(0, 0, 0, 0.4),
    0 0 15px rgba(255, 170, 80, 0.2);
  border-color: rgba(255, 140, 60, 0.8);
}

.nota-titulo {
  font-weight: bold;
  font-size: 16px;
  color: #2b1a0c;
  margin-bottom: 6px;
}

.nota-desc {
  font-size: 13px;
  color: #3b260f;
  opacity: 0.85;
  margin-bottom: 8px;
  line-height: 1.4;
}

.nota-prio {
  display: flex;
  align-items: center;
  gap: 4px;
}

.prio-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.prio-alta {
  background: rgba(220, 38, 38, 0.2);
  color: #991b1b;
  border: 1px solid rgba(220, 38, 38, 0.4);
}

.prio-media {
  background: rgba(234, 179, 8, 0.2);
  color: #854d0e;
  border: 1px solid rgba(234, 179, 8, 0.4);
}

.prio-baja {
  background: rgba(34, 197, 94, 0.2);
  color: #166534;
  border: 1px solid rgba(34, 197, 94, 0.4);
}

.empty-notes {
  text-align: center;
  padding: 40px 20px;
  color: #666;
  font-style: italic;
  font-size: 15px;
}

/* =======================
   ADD NOTE BUTTON
======================= */
.add-note-btn {
  background: linear-gradient(135deg, #ff9b4d 0%, #ff7e1f 100%) !important;
  color: white !important;
  font-weight: 700;
  text-transform: none;
  letter-spacing: 0.5px;
  border-radius: 12px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(255, 126, 31, 0.3);
}

.add-note-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 126, 31, 0.5);
  background: linear-gradient(135deg, #ffab5d 0%, #ff8e2f 100%) !important;
}

/* =======================
   MODAL NOTA EXPANDIDA
======================= */
.nota-expandida {
  position: relative;
  background-image: url("/textures/postit_ordedragon.png");
  background-size: cover;
  border-radius: 24px;
  padding: 30px;
  border: 4px solid rgba(90, 40, 15, 0.9);
  box-shadow: 
    0 0 30px rgba(255, 150, 60, 0.4),
    0 0 60px rgba(255, 100, 20, 0.2);
  animation: modalAppear 0.4s ease;
}

@keyframes modalAppear {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.sello-arcano {
  position: absolute;
  top: -20px;
  right: -20px;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background-image: url("/icons/orderdragon.png");
  background-size: cover;
  background-position: center;
  opacity: 0.6;
  animation: spinSeal 10s linear infinite;
  box-shadow: 0 0 20px rgba(255, 180, 80, 0.5);
  filter: drop-shadow(0 0 8px rgba(255, 200, 120, 0.4));
}

@keyframes spinSeal {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.titulo-expandido {
  text-align: center;
  font-size: 26px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #3b260f;
  font-family: "Cinzel", serif;
}

.desc-expandida {
  font-size: 17px;
  line-height: 1.6;
  margin-bottom: 20px;
  color: #2b1a0c;
  padding: 15px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  border: 1px solid rgba(139, 90, 43, 0.3);
}

.meta-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 15px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  color: #3b260f;
}

.prio-badge-modal {
  padding: 4px 12px;
  border-radius: 14px;
  font-weight: bold;
  font-size: 12px;
  text-transform: uppercase;
}

.cerrar-btn {
  background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%) !important;
  color: white !important;
  font-weight: 700;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.cerrar-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
}

/* =======================
   MODAL AÑADIR NOTA
======================= */
.papiro-modal {
  background-image: url("/textures/postit_ordedragon.png");
  background-size: cover;
  border-radius: 20px;
  border: 3px solid rgba(70, 40, 20, 0.85);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.modal-title {
  font-family: "Cinzel", serif;
  font-size: 22px;
  color: #3b260f;
  text-align: center;
}

.modal-actions {
  padding: 16px 24px;
  justify-content: flex-end;
  gap: 10px;
}

.cancel-btn {
  color: #8b5a2b !important;
}

.save-btn {
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important;
  color: white !important;
  font-weight: 700;
  border-radius: 10px;
}

.save-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(22, 163, 74, 0.4);
}
.delete-btn {
  background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%) !important;
  color: white !important;
  font-weight: 700;
  border-radius: 10px;
}

.delete-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
}
/* =======================
   VISTA MENSUAL FIX
======================= */

.month-view {
  animation: fadeIn 0.8s ease;
}

.month-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
  margin-bottom: 12px;
}

.day-name-cell {
  text-align: center;
  font-family: "Cinzel", serif;
  font-size: 16px;
  font-weight: 700;
  color: #ffcc88;
  padding: 12px;
  background: rgba(255, 170, 80, 0.1);
  border-radius: 10px;
  border: 1px solid rgba(255, 170, 80, 0.2);
}

.month-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.month-day-card {
  background: linear-gradient(145deg, #1a1a1a 0%, #151515 100%);
  border: 2px solid #2e2e2e;
  border-radius: 12px;
  padding: 12px;
  min-height: 120px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.month-day-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 170, 80, 0.5);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
}

.month-day-card.not-current-month {
  opacity: 0.3;
}

.month-day-card.has-notes {
  border-color: rgba(255, 170, 80, 0.4);
  background: linear-gradient(145deg, #1f1a15 0%, #1a1510 100%);
}

.month-day-number {
  font-family: "Cinzel", serif;
  font-size: 18px;
  font-weight: 700;
  color: #ffe7cf;
  margin-bottom: 8px;
}

.month-notes-mini {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.mini-note {
  font-family: "Cinzel", serif;
  font-size: 11px;
  padding: 4px 8px;
  border-radius: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: all 0.2s ease;
  cursor: pointer;
}

.mini-note:hover {
  transform: scale(1.05);
  z-index: 10;
}

.mini-note-alta {
  background: rgba(220, 38, 38, 0.3);
  color: #ff6b6b;
  border-left: 3px solid #dc2626;
}

.mini-note-media {
  background: rgba(234, 179, 8, 0.3);
  color: #ffd666;
  border-left: 3px solid #eab308;
}

.mini-note-baja {
  background: rgba(34, 197, 94, 0.3);
  color: #66ff99;
  border-left: 3px solid #22c55e;
}

.more-notes {
  font-size: 10px;
  color: #999;
  text-align: center;
  margin-top: 4px;
  font-style: italic;
}

/* =======================
   RESPONSIVE
======================= */
@media (max-width: 1200px) {
  .week-grid {
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  }
}

@media (max-width: 768px) {
  .calendar-page {
    padding: 20px 12px;
  }

  .week-title {
    font-size: 20px;
  }

  .week-grid {
    gap: 14px;
  }

  .day-card {
    min-height: 380px;
  }
}

@media (max-width: 600px) {
  .week-grid {
    grid-template-columns: 1fr;
  }
}
</style>
