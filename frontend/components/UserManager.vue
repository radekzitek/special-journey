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
              <NuxtButton color="red" size="xs" icon="i-heroicons-trash" @click="handleDeleteUser(u.id)" />
            </li>
          </ul>
        </div>
      </NuxtCard>
    </div>

    <RegisterModal
      :show="showCreateUser && clientReady"
      title="Create User"
      submit-label="Create"
      :error-message="createUserError"
      @submit="handleCreateUserSubmit"
      @close="showCreateUser = false"
      @clear-error="clearCreateUserError"
    />

    <!-- User Details/Edit -->
    <div v-if="selectedUser && clientReady" class="w-full md:w-2/3">
      <NuxtCard>
        <template #header>
          <div class="font-bold">User Details</div>
        </template>
        <div class="flex flex-col gap-4">
          <label for="email">Email</label>
          <NuxtInput id="email" v-model="form.email" label="Email" />
          <label for="role">Role</label>
          <NuxtSelect id="role" v-model="form.role" :options="roles" option-label="label" option-value="value" />
          <label for="is_active">Status</label>
          <NuxtSelect id="is_active" v-model="form.is_active" :options="activeOptions" option-label="label" option-value="value" />
          <label for="created_at">Created At</label>
          <NuxtInput id="created_at" :model-value="form.created_at" label="Created At" disabled />
          <label for="updated_at">Updated At</label>
          <NuxtInput id="updated_at" :model-value="form.updated_at" label="Updated At" disabled />
        </div>
        <template #footer>
          <div class="flex gap-2 justify-end mt-4">
            <NuxtButton color="primary" icon="i-heroicons-check" @click="handleUpdateUser">Update</NuxtButton>
            <NuxtButton color="gray" @click="clearSelection">Cancel</NuxtButton>
          </div>
        </template>
      </NuxtCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useUserForm } from '~/composables/useUserForm';
import RegisterModal from '~/components/RegisterModal.vue';

const { 
  form, 
  roles, 
  activeOptions, 
  setFormData, 
  clearForm, 
  updateUser, 
  deleteUser, 
  fetchUserData,
  createUser 
} = useUserForm();

const users = ref([]);
const selectedUser = ref(null);
const showCreateUser = ref(false);
const createUserError = ref<string | null>(null);
const clientReady = ref(false);

// Fetch all users
async function fetchUsers() {
  const userData = await fetchUserData(true); // true = fetch all users
  if (userData) {
    users.value = userData;
  }
}

// Select a user for editing
function selectUser(user) {
  console.log('Selected user:', user);
  selectedUser.value = user;
  setFormData(user);
  console.log('Form after selection:', form);
}

// Clear selection
function clearSelection() {
  selectedUser.value = null;
  clearForm();
}

// Handle user update
async function handleUpdateUser() {
  if (!selectedUser.value) return;
  
  console.log('Updating user ID:', selectedUser.value.id);
  const success = await updateUser(selectedUser.value.id);
  
  if (success) {
    // Refresh the user list to show updated data
    await fetchUsers();
    // Re-select the current user to refresh the form with updated data
    const updatedUserList = users.value;
    const updatedUser = updatedUserList.find(u => u.id === selectedUser.value.id);
    if (updatedUser) {
      selectUser(updatedUser);
    }
    alert('User updated successfully');
  } else {
    alert('Failed to update user. Check console for details.');
  }
}

// Handle user deletion
async function handleDeleteUser(id) {
  const success = await deleteUser(id);
  if (success) {
    if (selectedUser.value && selectedUser.value.id === id) {
      clearSelection();
    }
    await fetchUsers();
  }
}

// Handle user creation submission
async function handleCreateUserSubmit({ email, password, error }: { email?: string, password?: string, error?: string }) {
  if (error) {
    createUserError.value = error;
    return;
  }
  
  const result = await createUser(email!, password!);
  if (result.success) {
    showCreateUser.value = false;
    createUserError.value = null;
    await fetchUsers();
  } else {
    createUserError.value = result.error || 'User creation failed';
  }
}

function clearCreateUserError() {
  createUserError.value = null;
}

onMounted(() => { 
  clientReady.value = true; 
  fetchUsers();
});
</script>

<style scoped>
.max-w-md { max-width: 28rem; }
</style>
