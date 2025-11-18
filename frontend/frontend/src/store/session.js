import { reactive } from "vue";

export const session = reactive({
  token: localStorage.getItem("token") || null,

  login(token) {
    this.token = token;
    localStorage.setItem("token", token);
  },

  logout() {
    this.token = null;
    localStorage.removeItem("token");
  }
});
