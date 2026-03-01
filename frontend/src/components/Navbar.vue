<template>
  <nav class="bg-gray-800 shadow-lg">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center py-4">
        <router-link to="/" class="flex items-center space-x-2 text-xl font-bold text-white">
          <i class="fa-solid fa-image"></i>
          <span>Galéria</span>
        </router-link>

        <!-- Mobile menu button -->
        <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden text-gray-300 hover:text-white">
          <i class="fas" :class="mobileMenuOpen ? 'fa-times' : 'fa-bars'" />
        </button>

        <!-- Desktop menu -->
        <div class="hidden md:flex items-center space-x-4">
          <router-link v-if="!authStore.isAuthenticated" to="/login" 
            class="text-gray-300 hover:text-white transition">
            Belépés
          </router-link>
          <router-link v-if="!authStore.isAuthenticated" to="/register" 
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition">
            Regisztráció
          </router-link>
          
          <template v-if="authStore.isAuthenticated">
            <router-link to="/gallery" 
              class="text-gray-300 hover:text-white transition">
              <i class="fas fa-images mr-1"></i> Galéria
            </router-link>
            <button @click="handleLogout" 
              class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded transition">
              <i class="fas fa-sign-out-alt mr-1"></i> Kilépés
            </button>
          </template>
        </div>
      </div>

      <!-- Mobile menu -->
      <div v-if="mobileMenuOpen" class="md:hidden pb-4 space-y-2">
        <router-link v-if="!authStore.isAuthenticated" to="/login" 
          @click="mobileMenuOpen = false"
          class="block text-gray-300 hover:text-white py-2">
          Belépés
        </router-link>
        <router-link v-if="!authStore.isAuthenticated" to="/register" 
          @click="mobileMenuOpen = false"
          class="block bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
          Regisztráció
        </router-link>
        
        <template v-if="authStore.isAuthenticated">
          <router-link to="/gallery" 
            @click="mobileMenuOpen = false"
            class="block text-gray-300 hover:text-white py-2">
            <i class="fas fa-images mr-1"></i> Galéria
          </router-link>
          <button @click="handleLogout" 
            class="w-full text-left bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded">
            <i class="fas fa-sign-out-alt mr-1"></i> Kilépés
          </button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const mobileMenuOpen = ref(false)

const handleLogout = () => {
  authStore.logout()
  mobileMenuOpen.value = false
  router.push('/')
}
</script>
