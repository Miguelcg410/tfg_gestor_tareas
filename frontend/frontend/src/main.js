import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

// Vuetify
import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

// Iconos
import { aliases, mdi } from "vuetify/iconsets/mdi";
import "@mdi/font/css/materialdesignicons.css";

// Calendario (Vuetify Labs)
import { VCalendar } from "vuetify/labs/VCalendar";

// Crear instancia de Vuetify
const vuetify = createVuetify({
  components: {
    ...components, // <-- IMPORTANTE mantener esto
    VCalendar,     // <-- Añadimos el calendario
  },
  directives,
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: { mdi },
  },
  theme: {
    defaultTheme: "dark",
  },
});

// Crear app
createApp(App)
  .use(router)
  .use(vuetify)
  .mount("#app");
