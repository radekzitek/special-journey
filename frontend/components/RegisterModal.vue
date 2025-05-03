<!-- eslint-disable vue/html-self-closing -->
<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white text-black p-6 rounded shadow w-80">
      <h2 class="text-lg font-bold mb-2">{{ title }}</h2>
      <AppAlert :message="errorMessage" @close="clearError" />
      <form @submit.prevent="handleSubmit">
        <input
          v-model="email"
          name="email"
          type="email"
          placeholder="Email"
          class="border p-2 w-full mb-2"
          required
          autocomplete="email"
        />
        <input
          v-model="password"
          name="password"
          type="password"
          placeholder="Password"
          class="border p-2 w-full mb-2"
          required
          autocomplete="new-password"
        />
        <input
          v-model="confirm"
          name="confirm"
          type="password"
          placeholder="Confirm Password"
          class="border p-2 w-full mb-2"
          required
          autocomplete="new-password"
        />
        <div class="flex justify-between">
          <button type="submit" class="bg-blue-600 text-white px-3 py-1 rounded">
            {{ submitLabel }}
          </button>
          <button type="button" class="text-gray-600" @click="$emit('close')">
            Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import AppAlert from './AppAlert.vue';

const props = defineProps<{
  show: boolean,
  title?: string,
  submitLabel?: string,
  errorMessage?: string | null
}>();
const emit = defineEmits(['submit', 'close', 'clearError']);

const email = ref('');
const password = ref('');
const confirm = ref('');

watch(() => props.show, (val) => {
  if (val) {
    email.value = '';
    password.value = '';
    confirm.value = '';
  }
});

function handleSubmit() {
  if (password.value !== confirm.value) {
    emit('clearError');
    emit('submit', { error: 'Passwords do not match' });
    return;
  }
  emit('submit', { email: email.value, password: password.value });
}

function clearError() {
  emit('clearError');
}
</script>
