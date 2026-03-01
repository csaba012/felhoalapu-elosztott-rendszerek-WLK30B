<template>
  <div class="flex flex-col items-center justify-center min-h-[80vh]">
    <div class="text-center max-w-2xl mx-auto px-4">
      <i class="fas fa-camera text-6xl md:text-8xl text-blue-500 mb-6"></i>
      <h1 class="text-4xl md:text-6xl font-bold mb-4">Üdvözöllek a Galériában!</h1>
      <p class="text-lg md:text-xl text-gray-400 mb-8">
        Töltsd fel, rendszerezd és tárold fényképeidet egyszerűen és biztonságosan.
      </p>
      
      <div v-if="!authStore.isAuthenticated" class="flex flex-col sm:flex-row gap-4 justify-center">
        <router-link to="/register" 
          class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3 rounded-lg transition">
          <i class="fas fa-user-plus mr-2"></i> Regisztráció
        </router-link>
        <router-link to="/login" 
          class="bg-gray-700 hover:bg-gray-600 text-white font-semibold px-8 py-3 rounded-lg transition">
          <i class="fas fa-sign-in-alt mr-2"></i> Belépés
        </router-link>
      </div>
      
      <div v-else>
        <router-link to="/gallery" 
          class="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3 rounded-lg transition">
          <i class="fas fa-images mr-2"></i> Galéria Megnyitása
        </router-link>
      </div>

      <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
        <div class="bg-gray-800 p-6 rounded-lg">
          <i class="fas fa-upload text-3xl text-blue-500 mb-3 mx-auto"></i>
          <h3 class="text-xl font-semibold mb-2">Feltöltés</h3>
          <p class="text-gray-400">Töltsd fel fényképeidet néhány kattintással</p>
        </div>
        <div class="bg-gray-800 p-6 rounded-lg">
          <i class="fas fa-sort text-3xl text-blue-500 mb-3 mx-auto"></i>
          <h3 class="text-xl font-semibold mb-2">Rendszerezés</h3>
          <p class="text-gray-400">Rendezd név vagy dátum szerint a képeidet</p>
        </div>
        <div class="bg-gray-800 p-6 rounded-lg">
          <i class="fas fa-shield-alt text-3xl text-blue-500 mb-3 mx-auto"></i>
          <h3 class="text-xl font-semibold mb-2">Biztonság</h3>
          <p class="text-gray-400">Fényképeid biztonságban vannak</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>
