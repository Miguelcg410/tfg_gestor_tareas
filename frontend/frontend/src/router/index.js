import { createRouter, createWebHistory } from "vue-router";

// Importar páginas
import Login from "../pages/Login.vue";
import Register from "../pages/Register.vue";
import Tareas from "../pages/Tareas.vue";

const routes = [
  { path: "/", redirect: "/login" },

  { path: "/login", component: Login },
  { path: "/register", component: Register },

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

// Protección de rutas
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  if (to.meta.requiresAuth && !token) {
    return next("/login");
  }

  next();
});

export default router;
