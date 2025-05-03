<template>
  <NuxtCard class="max-w-md mx-auto my-6">
    <template #header>
      <div class="text-lg font-bold">User Profile</div>
    </template>
    <div v-if="clientReady" class="flex flex-col gap-4">
      <label for="email">Email</label>
      <NuxtInput id="email" v-model="form.email" label="Email" disabled />
      <label for="role">Role</label>
      <NuxtSelect id="role" v-model="form.role" :options="roles" option-label="label" option-value="value" />
      <label for="is_active">Active</label>
      <NuxtSelect id="is_active" v-model="form.is_active" :options="activeOptions" option-label="label" option-value="value" />
      <label for="created_at">Created At</label>
      <NuxtInput id="created_at" :model-value="form.created_at" label="Created At" disabled />
      <label for="updated_at">Updated At</label>
      <NuxtInput id="updated_at" :model-value="form.updated_at" label="Updated At" disabled />
    </div>
    <div v-else class="h-64 flex items-center justify-center">
      <span class="text-gray-400">Loading...</span>
    </div>
    <template #footer>
      <div v-if="clientReady" class="flex gap-2 justify-end mt-4">
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

const clientReady = ref(false);
onMounted(() => { clientReady.value = true; });

const roles = [
  { label: 'Member', value: 'member' },
  { label: 'Manager', value: 'manager' },
  { label: 'Admin', value: 'admin' }
];
const activeOptions = [
  { label: 'True', value: true },
  { label: 'False', value: false }
];

async function fetchUser() {
  if (!token.value) return;
  const res = await fetch(`http://localhost:8000/users/me`, {
    headers: { Authorization: `Bearer ${token.value}` }
  });
  if (res.ok) {
    const data = await res.json();
    // Explicitly set each property to ensure correct types
    form.value.email = data.email || '';
    form.value.role = data.role || 'member'; // Default to member if null
    form.value.is_active = typeof data.is_active === 'boolean' ? data.is_active : true;
    form.value.created_at = data.created_at || '';
    form.value.updated_at = data.updated_at || '';
  }
}

async function updateUser() {
  if (!token.value) return;
  // Only send updatable fields to the API
  const userData = {
    role: form.value.role,
    is_active: form.value.is_active
  };
  
  await fetch(`http://localhost:8000/users/me`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token.value}`
    },
    body: JSON.stringify(userData)
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
