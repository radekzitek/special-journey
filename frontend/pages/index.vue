<template>
  <div>
    <h1>Welcome to the homepage</h1>
    <AppAlert :message="null" />
    <div v-if="clientReady" class="mt-4">
      <span v-if="isAuthenticated">You are logged in as {{ user?.email }}</span>
      <span v-else>No user is authenticated</span>
    </div>
    <UserManager v-if="clientReady && isAuthenticated" />
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '~/composables/useAuth';
import UserManager from '~/components/UserManager.vue';
import { ref, onMounted } from 'vue';

const clientReady = ref(false);
onMounted(() => { clientReady.value = true; });

const { isAuthenticated, user } = useAuth();
</script>

<style scoped></style>
