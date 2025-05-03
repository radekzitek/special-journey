<template>
  <NuxtCard class="max-w-md mx-auto my-6">
    <template #header>
      <div class="text-lg font-bold">User Profile</div>
    </template>
    <div class="flex flex-col gap-4">
      <NuxtInput v-model="form.email" label="Email" disabled />
      <NuxtInput v-model="form.role" label="Role" />
      <NuxtInput v-model="form.is_active" label="Status" />
      <NuxtInput :model-value="form.created_at" label="Created At" disabled />
      <NuxtInput :model-value="form.updated_at" label="Updated At" disabled />
    </div>
    <template #footer>
      <div class="flex gap-2 justify-end mt-4">
        <NuxtButton color="primary" icon="i-heroicons-check" @click="updateUser">Update</NuxtButton>
        <NuxtButton color="red" icon="i-heroicons-trash" @click="deleteUser">Delete</NuxtButton>
      </div>
    </template>
  </NuxtCard>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import { useAuth } from '~/composables/useAuth';

const { user, token, logout } = useAuth();
const form = ref({
  email: user.value?.email || '',
  role: '',
  is_active: '',
  created_at: '',
  updated_at: ''
});

async function fetchUser() {
  if (!token.value) return;
  const res = await fetch(`http://localhost:8000/users/me`, {
    headers: { Authorization: `Bearer ${token.value}` }
  });
  if (res.ok) {
    const data = await res.json();
    form.value = { ...data };
  }
}

async function updateUser() {
  if (!token.value) return;
  await fetch(`http://localhost:8000/users/me`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token.value}`
    },
    body: JSON.stringify(form.value)
  });
  await fetchUser();
}

async function deleteUser() {
  if (!token.value) return;
  await fetch(`http://localhost:8000/users/me`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token.value}` }
  });
  logout();
}

onMounted(fetchUser);
watch(() => user.value?.email, fetchUser);
</script>

<style scoped>
.max-w-md { max-width: 28rem; }
</style>
