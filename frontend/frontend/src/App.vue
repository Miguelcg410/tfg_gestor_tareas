<script setup>
import Navbar from "./components/Navbar.vue";
</script>

<template>
  <v-app>
    <Navbar />

    <v-main>
      <div class="page-container">
        <router-view />
      </div>
    </v-main>
  </v-app>
</template>

<style>
.page-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 20px;
}
</style>
