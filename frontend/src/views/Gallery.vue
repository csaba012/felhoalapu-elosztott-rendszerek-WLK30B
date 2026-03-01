<template>
  <div class="max-w-7xl mx-auto">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
      <h1 class="text-3xl font-bold">
        <i class="fas fa-images mr-2"></i> Galéria
      </h1>
      
      <button 
        @click="showUploadModal = true"
        class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-lg transition w-full md:w-auto"
      >
        <i class="fas fa-upload mr-2"></i> Feltöltés
      </button>
    </div>

    <!-- Upload Modal -->
    <UploadModal 
      v-if="showUploadModal" 
      @close="showUploadModal = false"
      @uploaded="loadPhotos"
    />

    <!-- Image Detail Modal -->
    <ImageModal 
      v-if="selectedPhoto"
      :photo="selectedPhoto"
      @close="selectedPhoto = null"
      @deleted="handlePhotoDeleted"
    />

    <!-- Filters and Sorting -->
    <div class="bg-gray-800 rounded-lg p-4 mb-6 flex flex-col md:flex-row gap-4">
      <div class="flex-1">
        <label class="block text-sm font-medium mb-2">Rendezés</label>
        <select 
          v-model="sortBy"
          class="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="date_desc">Dátum (újabb először)</option>
          <option value="date_asc">Dátum (régebbi először)</option>
          <option value="name_asc">Név (A-Z)</option>
          <option value="name_desc">Név (Z-A)</option>
        </select>
      </div>
    </div>

    <!-- Photos Grid -->
    <div v-if="loading" class="text-center py-12">
      <i class="fas fa-spinner fa-spin text-4xl text-blue-500"></i>
      <p class="mt-4 text-gray-400">Betöltés...</p>
    </div>

    <div v-else-if="sortedPhotos.length === 0" class="text-center py-12">
      <i class="fas fa-images text-6xl text-gray-600 mb-4"></i>
      <p class="text-xl text-gray-400">Még nincsenek fényképek</p>
      <p class="text-gray-500 mt-2">Töltsd fel az első képedet!</p>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <PhotoCard 
        v-for="photo in sortedPhotos" 
        :key="photo.id"
        :photo="photo"
        @click="selectedPhoto = photo"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import PhotoCard from '@/components/PhotoCard.vue'
import UploadModal from '@/components/UploadModal.vue'
import ImageModal from '@/components/ImageModal.vue'
import type { Photo, SortOption } from '@/types'

const photos = ref<Photo[]>([])
const loading = ref(false)
const showUploadModal = ref(false)
const selectedPhoto = ref<Photo | null>(null)
const sortBy = ref<SortOption>('date_desc')

const sortedPhotos = computed(() => {
  const photosCopy = [...photos.value]
  
  switch (sortBy.value) {
    case 'date_asc':
      return photosCopy.sort((a, b) => new Date(a.upload_date).getTime() - new Date(b.upload_date).getTime())
    case 'date_desc':
      return photosCopy.sort((a, b) => new Date(b.upload_date).getTime() - new Date(a.upload_date).getTime())
    case 'name_asc':
      return photosCopy.sort((a, b) => a.name.localeCompare(b.name))
    case 'name_desc':
      return photosCopy.sort((a, b) => b.name.localeCompare(a.name))
    default:
      return photosCopy
  }
})

const loadPhotos = async () => {
  loading.value = true
  try {
    const response = await api.get<Photo[]>('/photos')
    photos.value = response.data
  } catch (error) {
    console.error('Hiba a képek betöltése során:', error)
  } finally {
    loading.value = false
  }
}

const handlePhotoDeleted = (photoId: number) => {
  photos.value = photos.value.filter(p => p.id !== photoId)
  selectedPhoto.value = null
}

onMounted(() => {
  loadPhotos()
})
</script>
