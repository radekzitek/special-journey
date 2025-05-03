<template>
  <div class="flex flex-col md:flex-row gap-8">
    <!-- User List -->
    <div class="w-full md:w-1/3">
      <NuxtCard>
        <template #header>
          <div class="font-bold">Users</div>
        </template>
        <div>
          <NuxtButton color="primary" class="mb-2 w-full" @click="showCreateUser = true">+ Create User</NuxtButton>
          <ul>
            <li v-for="u in users" :key="u.id" class="flex items-center justify-between border-b py-2">
              <span class="cursor-pointer" @click="selectUser(u)">{{ u.email }}</span>
              <NuxtButton color="red" size="xs" icon="i-heroicons-trash" @click="deleteUser(u.id)" />
            </li>
          </ul>
        </div>
      </NuxtCard>
    </div>

    <RegisterModal
      :show="showCreateUser"
      title="Create User"
      submit-label="Create"
      :error-message="createUserError"
      @submit="handleCreateUserSubmit"
      @close="showCreateUser = false"
      @clear-error="clearCreateUserError"
    />

    <!-- User Details/Edit -->
    <div v-if="selectedUser" class="w-full md:w-2/3">
      <NuxtCard>
        <template #header>
          <div class="font-bold">User Details</div>
        </template>
        <div class="flex flex-col gap-4">
          <NuxtInput v-model="form.email" label="Email" />
          <NuxtInput v-model="form.role" label="Role" />
          <NuxtInput v-model="form.is_active" label="Status" />
          <NuxtInput :model-value="form.created_at" label="Created At" disabled />
          <NuxtInput :model-value="form.updated_at" label="Updated At" disabled />
        </div>
        <template #footer>
          <div class="flex gap-2 justify-end mt-4">
            <NuxtButton color="primary" icon="i-heroicons-check" @click="updateUser">Update</NuxtButton>
            <NuxtButton color="gray" @click="clearSelection">Cancel</NuxtButton>
          </div>
        </template>
      </NuxtCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { useAuth } from '~/composables/useAuth';
import RegisterModal from '~/components/RegisterModal.vue';

const { token } = useAuth();
const users = ref([]);
const selectedUser = ref(null);
const creating = ref(false);
const form = reactive({ email: '', role: '', is_active: true, created_at: '', updated_at: '' });
const showCreateUser = ref(false);
const createUserError = ref<string | null>(null);

async function fetchUsers() {
  if (!token.value) return;
  const res = await fetch('http://localhost:8000/users', {
    headers: { Authorization: `Bearer ${token.value}` }
  });
  if (res.ok) users.value = await res.json();
}

function selectUser(u) {
  creating.value = false;
  selectedUser.value = u;
  Object.assign(form, u);
}

// Removed unused startCreate function

async function updateUser() {
  if (!token.value || !selectedUser.value) return;
  await fetch(`http://localhost:8000/users/${selectedUser.value.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token.value}`
    },
    body: JSON.stringify(form)
  });
  await fetchUsers();
}

async function deleteUser(id) {
  if (!token.value) return;
  await fetch(`http://localhost:8000/users/${id}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token.value}` }
  });
  if (selectedUser.value && selectedUser.value.id === id) clearSelection();
  await fetchUsers();
}

async function createUser(email: string, password: string) {
  if (!token.value) return;
  try {
    const res = await fetch('http://localhost:8000/users', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token.value}`
      },
      body: JSON.stringify({ email, password })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'User creation failed');
    }
    showCreateUser.value = false;
    createUserError.value = null;
    await fetchUsers();
  } catch (e: unknown) {
    if (e instanceof Error) {
      createUserError.value = e.message || 'User creation failed';
    } else {
      createUserError.value = 'User creation failed';
    }
  }
}

function handleCreateUserSubmit({ email, password, error }: { email?: string, password?: string, error?: string }) {
  if (error) {
    createUserError.value = error;
    return;
  }
  createUser(email!, password!);
}

function clearCreateUserError() {
  createUserError.value = null;
}

function clearSelection() {
  creating.value = false;
  selectedUser.value = null;
  form.email = '';
  form.role = '';
  form.is_active = true;
  form.created_at = '';
  form.updated_at = '';
}

onMounted(fetchUsers);
</script>

<style scoped>
.max-w-md { max-width: 28rem; }
</style>
