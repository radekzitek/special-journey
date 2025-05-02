<template>
  <div v-if="message" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
    <span class="block sm:inline">{{ message }}</span>
    <button class="absolute top-0 bottom-0 right-0 px-4 py-3" @click="$emit('close')">
      <span class="text-2xl">&times;</span>
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{ message: string | null }>()
defineEmits<{
  (e: 'close'): void
}>()
</script>

<style scoped>
button {
  background: transparent;
  border: none;
  cursor: pointer;
}
</style>
