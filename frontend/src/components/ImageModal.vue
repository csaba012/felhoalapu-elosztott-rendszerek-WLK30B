<template>
  <div class="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50 p-4" @click.self="$emit('close')">
    <div class="max-w-6xl w-full">
      <div class="bg-gray-800 rounded-lg overflow-hidden">
        <div class="flex justify-between items-center p-4 border-b border-gray-700">
          <div>
            <h2 class="text-2xl font-bold">{{ photo.name }}</h2>
            <p class="text-sm text-gray-400">
              <i class="fas fa-calendar mr-1"></i>
              {{ formattedDate }}
            </p>
          </div>
          <button @click="$emit('close')" class="text-gray-400 hover:text-white text-2xl">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <div class="p-4 flex justify-center bg-gray-900">
          <img 
            :src="imageUrl" 
            :alt="photo.name"
            class="max-w-full max-h-[70vh] object-contain"
          />
        </div>

        <div class="p-4 flex justify-end gap-4">
          <button 
            @click="handleDelete"
            :disabled="deleting"
            class="bg-red-600 hover:bg-red-700 disabled:bg-gray-600 text-white font-semibold px-6 py-2 rounded-lg transition"
          >
            <i v-if="deleting" class="fas fa-spinner fa-spin mr-2"></i>
            <i v-else class="fas fa-trash mr-2"></i>
            {{ deleting ? 'Törlés...' : 'Törlés' }}
          </button>
        </div>
      </div>

      <div v-if="error" class="mt-4 bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import api from '@/services/api'
import { AxiosError } from 'axios'
import type { Photo, ApiError } from '@/types'

interface Props {
  photo: Photo
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'deleted', id: number): void
}>()

const deleting = ref(false)
const error = ref('')

const imageUrl = computed(() => {
  return `${import.meta.env.API_URL || 'http://localhost:5000'}/uploads/${props.photo.filename}`
})

const formattedDate = computed(() => {
  const date = new Date(props.photo.upload_date)
  return date.toLocaleString('hu-HU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
})

const handleDelete = async () => {
  if (!confirm('Biztosan törölni szeretnéd ezt a képet?')) {
    return
  }
  
  deleting.value = true
  error.value = ''
  
  try {
    await api.delete(`/photos/${props.photo.id}`)
    emit('deleted', props.photo.id)
  } catch (err) {
    const axiosError = err as AxiosError<ApiError>
    error.value = axiosError.response?.data?.error || 'Hiba történt a törlés során'
  } finally {
    deleting.value = false
  }
}
</script>
