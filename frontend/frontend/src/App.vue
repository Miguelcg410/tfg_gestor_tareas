<script setup>
import Navbar from "./components/Navbar.vue";
</script>

<template>
  <Navbar />

  <main
    style="
      max-width: 800px;
      margin: 30px auto;
      padding: 20px;
      background: #1e1e1e;
      color: white;
      border-radius: 10px;
      box-shadow: 0 0 15px rgba(0,0,0,0.3);
    "
  >
    <router-view />
  </main>
</template>
