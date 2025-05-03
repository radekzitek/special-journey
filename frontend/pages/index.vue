<template>
  <div>
    <h1>Welcome to the homepage</h1>
    <AppAlert :message="null" />
    <div class="mt-4">
      <span v-if="isAuthenticated">You are logged in as {{ user?.email }}</span>
      <span v-else>No user is authenticated</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '~/composables/useAuth';
const { isAuthenticated, user } = useAuth();
</script>

<style scoped></style>
