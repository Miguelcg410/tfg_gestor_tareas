import { createRouter, createWebHistory } from "vue-router";
import { session } from "../store/session";

// Importar páginas
import Login from "../pages/Login.vue";
import Register from "../pages/Register.vue";
import Tareas from "../pages/Tareas.vue";
import Calendario from "../pages/Calendario.vue";

const routes = [
  {
    path: "/",
    name: "Inicio",
    component: () => import("@/pages/Inicio.vue"),
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
  {
    path: "/tareas",
    name: "Tareas",
    component: Tareas,
  },
  {
    path: "/calendario",
    name: "Calendario",
    component: Calendario,
  }
];

// ⬅️ AQUÍ ESTABA EL ERROR: FALTABA CREAR EL ROUTER
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// (Opcional) Proteger rutas si quieres
router.beforeEach((to, from, next) => {
  if (to.name !== "Login" && !session.token) {
    return next("/login");
  }
  next();
});

export default router;
