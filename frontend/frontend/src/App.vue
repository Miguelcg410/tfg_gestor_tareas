<script setup>
import { ref } from 'vue'
import axios from 'axios'

const mensaje = ref("Presiona el botón para probar la API")

async function probarAPI() {
  try {
    const response = await axios.get("http://127.0.0.1:5000/api")
    mensaje.value = response.data.mensaje
  } catch (error) {
    mensaje.value = "Error conectando con la API"
    console.error(error)
  }
}
</script>

<template>
  <div style="padding: 40px; font-size: 22px;">
    <h1>Prueba de conexión con Flask</h1>

    <button @click="probarAPI" 
            style="padding: 10px 20px; font-size: 20px; cursor: pointer;">
      Probar API
    </button>

    <p style="margin-top: 20px;">{{ mensaje }}</p>
  </div>
</template>
