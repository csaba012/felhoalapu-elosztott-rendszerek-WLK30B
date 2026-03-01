<template>
  <div class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4" @click.self="$emit('close')">
    <div class="bg-gray-800 rounded-lg p-6 md:p-8 max-w-md w-full">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold">
          <i class="fas fa-upload mr-2"></i> Kép feltöltése
        </h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-white text-2xl">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <form @submit.prevent="handleUpload" class="space-y-4">
        <div v-if="error" class="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded">
          {{ error }}
        </div>

        <div>
          <label for="name" class="block text-sm font-medium mb-2">Kép neve (max. 40 karakter)</label>
          <input 
            v-model="name"
            type="text" 
            id="name"
            required
            maxlength="40"
            class="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Fénykép neve"
          />
          <p class="text-xs text-gray-400 mt-1">{{ name.length }}/40 karakter</p>
        </div>

        <div>
          <label for="file" class="block text-sm font-medium mb-2">Fájl kiválasztása</label>
          <input 
            @change="handleFileChange"
            type="file" 
            id="file"
            required
            accept="image/*"
            class="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:bg-blue-600 file:text-white hover:file:bg-blue-700 file:cursor-pointer"
          />
        </div>

        <div v-if="preview" class="mt-4">
          <p class="text-sm font-medium mb-2">Előnézet:</p>
          <img :src="preview" alt="Preview" class="w-full rounded-lg max-h-64 object-contain bg-gray-700" />
        </div>

        <div class="flex gap-4 pt-4">
          <button 
            type="submit"
            :disabled="loading"
            class="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-semibold py-3 rounded-lg transition"
          >
            <i v-if="loading" class="fas fa-spinner fa-spin mr-2"></i>
            <i v-else class="fas fa-upload mr-2"></i>
            {{ loading ? 'Feltöltés...' : 'Feltöltés' }}
          </button>
          <button 
            type="button"
            @click="$emit('close')"
            class="flex-1 bg-gray-700 hover:bg-gray-600 text-white font-semibold py-3 rounded-lg transition"
          >
            Mégse
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '@/services/api'
import { AxiosError } from 'axios'
import type { ApiError } from '@/types'

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'uploaded'): void
}>()

const name = ref('')
const file = ref<File | null>(null)
const preview = ref<string | null>(null)
const loading = ref(false)
const error = ref('')

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const selectedFile = target.files?.[0]
  if (selectedFile) {
    file.value = selectedFile
    const reader = new FileReader()
    reader.onload = (e) => {
      preview.value = e.target?.result as string
    }
    reader.readAsDataURL(selectedFile)
  }
}

const handleUpload = async () => {
  loading.value = true
  error.value = ''
  
  try {
    if (!file.value) {
      error.value = 'Kérlek válassz ki egy fájlt'
      loading.value = false
      return
    }

    const formData = new FormData()
    formData.append('name', name.value)
    formData.append('file', file.value)
    
    await api.post('/photos', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    emit('uploaded')
    emit('close')
  } catch (err) {
    const axiosError = err as AxiosError<ApiError>
    error.value = axiosError.response?.data?.error || 'Hiba történt a feltöltés során'
  } finally {
    loading.value = false
  }
}
</script>
