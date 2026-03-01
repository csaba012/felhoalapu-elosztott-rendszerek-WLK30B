<template>
  <div class="flex items-center justify-center min-h-[80vh] px-4">
    <div class="w-full max-w-md">
      <div class="bg-gray-800 rounded-lg shadow-xl p-8">
        <h2 class="text-3xl font-bold text-center mb-6">
          <i class="fas fa-user-plus mr-2"></i> Regisztráció
        </h2>

        <form @submit.prevent="handleRegister" class="space-y-6">
          <div v-if="error" class="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded">
            {{ error }}
          </div>

          <div v-if="success" class="bg-green-900/50 border border-green-500 text-green-200 px-4 py-3 rounded">
            {{ success }}
          </div>

          <div>
            <label for="email" class="block text-sm font-medium mb-2">E-mail cím</label>
            <input 
              v-model="email"
              type="email" 
              id="email"
              required
              class="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="pelda@email.com"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium mb-2">Jelszó (min. 8 karakter)</label>
            <input 
              v-model="password"
              type="password" 
              id="password"
              required
              minlength="8"
              class="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="••••••••"
            />
          </div>

          <div>
            <label for="confirmPassword" class="block text-sm font-medium mb-2">Jelszó megerősítése</label>
            <input 
              v-model="confirmPassword"
              type="password" 
              id="confirmPassword"
              required
              class="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="••••••••"
            />
          </div>

          <button 
            type="submit"
            :disabled="loading"
            class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-semibold py-3 rounded-lg transition"
          >
            <i v-if="loading" class="fas fa-spinner fa-spin mr-2"></i>
            <i v-else class="fas fa-user-plus mr-2"></i>
            {{ loading ? 'Betöltés...' : 'Regisztráció' }}
          </button>
        </form>

        <p class="text-center mt-6 text-gray-400">
          Már van fiókod? 
          <router-link to="/login" class="text-blue-500 hover:text-blue-400">
            Jelentkezz be
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { AxiosError } from 'axios'
import type { ApiError } from '@/types'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const handleRegister = async () => {
  loading.value = true
  error.value = ''
  success.value = ''
  
  if (password.value !== confirmPassword.value) {
    error.value = 'A két jelszó nem egyezik'
    loading.value = false
    setTimeout(() => {
      error.value = ''
    }, 3000)
    return
  }
  
  try {
    await authStore.register({ email: email.value, password: password.value })
    success.value = 'Sikeres regisztráció! Átirányítás...'
    setTimeout(() => {
      router.push('/login')
    }, 1000)
  } catch (err) {
    const axiosError = err as AxiosError<ApiError>
    error.value = axiosError.response?.data?.error || 'Regisztrációs hiba történt'
    setTimeout(() => {
      error.value = ''
    }, 3000)
  } finally {
    loading.value = false
  }
}
</script>