import { createRouter, createWebHistory } from "vue-router";

// Importar páginas
import Login from "../pages/Login.vue";
import Register from "../pages/Register.vue";
import Tareas from "../pages/Tareas.vue";
import Calendario from "../pages/Calendario.vue";
import { session } from "../store/session";   // <-- IMPORTANTE

const routes = [
  { path: "/", redirect: "/login" },

  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/calendario", component: Calendario, meta: { requiresAuth: true } },
  // Ruta protegida
  { 
    path: "/tareas", 
    component: Tareas,
    meta: { requiresAuth: true }
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Protección de rutas usando session
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !session.token) {
    return next("/login");
  }
  next();
});

export default router;
