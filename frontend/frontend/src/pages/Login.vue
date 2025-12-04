<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { useRouter } from "vue-router";

import api from "../services/api";
import { session } from "../store/session";

const email = ref("");
const password = ref("");
const mensaje = ref("");
const loading = ref(false);
const showPassword = ref(false);

const router = useRouter();

let scene, camera, renderer, dragon, mixer;
let clock = new THREE.Clock();
let animationFrame;

/* ==========================
   LOGIN (MISMO CÓDIGO MEJORADO)
========================== */
async function login() {
  if (loading.value) return;

  if (!email.value.trim() || !password.value.trim()) {
    mensaje.value = "Debes completar todos los campos.";
    return;
  }

  loading.value = true;
  mensaje.value = "";

  try {
    const { data } = await api.post("/login", {
      email: email.value.trim(),
      password: password.value.trim(),
    });

    session.login(data.token);
    localStorage.setItem("token", data.token);
    localStorage.setItem("usuario_id", data.usuario.id);

    mensaje.value = "🔥 ¡Acceso concedido, Guerrero del Fuego!";
    setTimeout(() => router.push("/tareas"), 900);

  } catch {
    mensaje.value = "Credenciales no válidas.";
  } finally {
    loading.value = false;
  }
}

/* ==========================
   3D — Three.js
========================== */
onMounted(() => {
  const canvas = document.getElementById("dragonCanvas");

  /** SCENE **/
  scene = new THREE.Scene();
  scene.background = null; // transparente real

  /** CAMERA **/
  camera = new THREE.PerspectiveCamera(
    45,
    canvas.clientWidth / canvas.clientHeight,
    0.1,
    100
  );
  camera.position.set(0, 1.5, 14);




  /** RENDERER **/
  renderer = new THREE.WebGLRenderer({
    canvas,
    alpha: true,
    antialias: true,
  });
  renderer.setSize(canvas.clientWidth, canvas.clientHeight);
  renderer.setPixelRatio(window.devicePixelRatio);

  /** LIGHTING **/
  const key = new THREE.DirectionalLight(0xffaa66, 2);
  key.position.set(2, 2, 3);

  const fill = new THREE.DirectionalLight(0xff5522, 0.7);
  fill.position.set(-2, 1, -2);

  const ambient = new THREE.AmbientLight(0xffaa66, 0.4);

  scene.add(key, fill, ambient);

  /** DRAGON MODEL **/
  const loader = new GLTFLoader();
const dragonURL = new URL('@/assets/3d/dragon.glb', import.meta.url).href;

loader.load(
  dragonURL,
  (gltf) => {
    console.log("🐉 DRAGÓN CARGADO!");

    dragon = gltf.scene;

    // 👉 Ajustes perfectos
    dragon.scale.set(0.35, 0.35, 0.35);
    dragon.position.set(0, -0.2, -10);
    scene.add(dragon);

    mixer = new THREE.AnimationMixer(dragon);
    if (gltf.animations.length > 0) {
      mixer.clipAction(gltf.animations[0]).play();
    }
  }
);
;




  /** LOOP **/
  const animate = () => {
    animationFrame = requestAnimationFrame(animate);

    const delta = clock.getDelta();

    if (mixer) mixer.update(delta);

    // MOVIMIENTO SUAVE realista (como si flotara en aire caliente)
    if (dragon) {
      dragon.rotation.y = Math.sin(clock.elapsedTime * 0.3) * 0.2;
      dragon.position.y = Math.sin(clock.elapsedTime * 0.8) * 0.04;
    }

    renderer.render(scene, camera);
  };
  animate();

  /** RESIZE **/
  window.addEventListener("resize", resizeCanvas);

  function resizeCanvas() {
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;

    camera.aspect = w / h;
    camera.updateProjectionMatrix();

    renderer.setSize(w, h);
  }
});

onBeforeUnmount(() => {
  cancelAnimationFrame(animationFrame);
  renderer.dispose();
  window.removeEventListener("resize", () => {});
});
</script>
<template>
  <div class="container-3d-login">

    <!-- DRAGÓN 3D -->
    <canvas id="dragonCanvas" class="dragon-3d"></canvas>

    <!-- LOGIN -->
    <v-container class="login-container">
      <div class="login-card-wrapper">

        <v-card class="login-card">

          <v-card-title class="login-header">
            <h1 class="login-title">Acceso al Reino</h1>
          </v-card-title>

          <v-card-text class="login-form">
            <v-text-field 
              v-model="email" 
              label="Correo" 
              variant="outlined" 
            />

            <v-text-field 
              v-model="password" 
              label="Contraseña"
              :type="showPassword ? 'text' : 'password'"
              variant="outlined"
            />

            <v-alert 
              v-if="mensaje" 
              :type="mensaje.includes('🔥') ? 'success' : 'error'"
            >
              {{ mensaje }}
            </v-alert>
          </v-card-text>

          <v-card-actions class="login-actions">
            <div class="actions-wrapper">

              <!-- BOTÓN LOGIN -->
              <v-btn
                block
                class="btn-login"
                :loading="loading"
                :disabled="loading"
                @click="login"
              >
                <v-icon left>mdi-sword-cross</v-icon>
                <span class="btn-text">Entrar al Reino</span>
              </v-btn>

              <!-- DIVISOR -->
              <div class="divider-or">
                <div class="divider-line"></div>
                <span class="divider-text">o</span>
                <div class="divider-line"></div>
              </div>

              <!-- BOTÓN REGISTRO -->
              <v-btn
                block
                class="btn-register"
                variant="outlined"
                @click="router.push('/register')"
              >
                <v-icon left>mdi-account-plus</v-icon>
                <span class="btn-text">Crear Nueva Cuenta</span>
              </v-btn>

            </div>
          </v-card-actions>

        </v-card>

      </div>
    </v-container>

  </div>
</template>

<style scoped>

.container-3d-login {
  position: relative;
  width: 100%;
  min-height: 100vh;
  background: radial-gradient(circle at bottom,
    #140f0c 0%, #0b0908 65%, #000 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

/* CANVAS 3D */
.dragon-3d {
  position: absolute;
  top: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

/* LOGIN CARD */
.login-card {
  background: rgba(25,20,15,0.92) !important;
  border-radius: 16px;
  border: none !important; /* QUITAR BORDE */
  padding: 20px;
  backdrop-filter: blur(14px);
  z-index: 3;
  animation: fadeIn 0.7s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(25px); }
  to { opacity: 1; transform: translateY(0); }
}

.login-title {
  font-family: "Cinzel", serif;
  color: #ffd8a0;
  text-align: center;
  margin-bottom: 10px;
}

/* BOTÓN */
.btn-login {
  background: linear-gradient(135deg, #ff8a3d, #ff5a00) !important;
  color: white !important;
  border-radius: 14px;
  font-family: "Cinzel", serif;
  box-shadow: 0 10px 28px rgba(255,90,0,0.4);
}

.btn-login:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 36px rgba(255,120,20,0.6);
}

</style>
