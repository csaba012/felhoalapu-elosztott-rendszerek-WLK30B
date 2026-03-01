<template>
  <div 
    @click="$emit('click')"
    class="bg-gray-800 rounded-lg overflow-hidden shadow-lg hover:shadow-2xl transition-all cursor-pointer transform hover:scale-105"
  >
    <div class="aspect-square bg-gray-700 relative">
      <img 
        :src="imageUrl" 
        :alt="photo.name"
        class="w-full h-full object-cover"
        loading="lazy"
      />
    </div>
    <div class="p-4">
      <h3 class="font-semibold text-lg truncate mb-1">{{ photo.name }}</h3>
      <p class="text-sm text-gray-400">
        <i class="fas fa-calendar mr-1"></i>
        {{ formattedDate }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Photo } from '@/types'

interface Props {
  photo: Photo
}

const props = defineProps<Props>()

defineEmits<{
  (e: 'click'): void
}>()

const imageUrl = computed(() => {
  return `${import.meta.env.API_URL || 'http://localhost:5000'}/uploads/${props.photo.filename}`
})

const formattedDate = computed(() => {
  const date = new Date(props.photo.upload_date)
  return date.toLocaleString('hu-HU', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
})
</script>
