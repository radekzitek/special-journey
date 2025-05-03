<!-- eslint-disable vue/html-self-closing -->
<template>
  <div
    class="flex bg-black text-white align-middle p-4 items-center justify-between"
  >
    <div class="flex items-center">
      <NuxtIcon
        name="material-symbols-wind-power"
        size="32"
        class="text-green-400 me-2"
      />
      AI Performance Hub
    </div>
    <div>
      <template v-if="!isAuthenticated">
        <button
          class="text-white bg-green-600 px-3 py-1 rounded me-2"
          @click="showLogin = true"
        >
          Login
        </button>
        <button
          class="text-white bg-blue-600 px-3 py-1 rounded"
          @click="showRegister = true"
        >
          Register
        </button>
      </template>
      <template v-else>
        <span class="me-2">{{ user?.email }}</span>
        <button
          class="text-white bg-gray-600 px-3 py-1 rounded me-2"
          @click="showReset = true"
        >
          Reset Password
        </button>
        <button class="text-white bg-red-600 px-3 py-1 rounded" @click="logout">
          Logout
        </button>
      </template>
    </div>

    <!-- Login Modal -->
    <div
      v-if="showLogin"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white text-black p-6 rounded shadow w-80">
        <h2 class="text-lg font-bold mb-2">Login</h2>
        <AppAlert :message="errorMessage" @close="clearError" />
        <form
          @submit.prevent="
            login(
              ($event.target as HTMLFormElement)?.email.value,
              ($event.target as HTMLFormElement)?.password.value
            )
          "
        >
          <input
            name="email"
            type="email"
            placeholder="Email"
            class="border p-2 w-full mb-2"
            required
            autocomplete="email"
          />
          <input
            name="password"
            type="password"
            placeholder="Password"
            class="border p-2 w-full mb-2"
            required
            autocomplete="current-password"
          />
          <div class="flex justify-between">
            <button
              type="submit"
              class="bg-green-600 text-white px-3 py-1 rounded"
            >
              Login
            </button>
            <button
              type="button"
              class="text-gray-600"
              @click="showLogin = false"
            >
              Cancel
            </button>
          </div>
        </form>
        <button
          class="text-blue-600 mt-2 underline"
          @click="
            showLogin = false;
            showReset = true;
          "
        >
          Forgot password?
        </button>
      </div>
    </div>

    <!-- Register Modal -->
    <div
      v-if="showRegister"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white text-black p-6 rounded shadow w-80">
        <h2 class="text-lg font-bold mb-2">Register</h2>
        <AppAlert :message="errorMessage" @close="clearError" />
        <form @submit.prevent="registerHandler">
          <input
            v-model="regEmail"
            name="email"
            type="email"
            placeholder="Email"
            class="border p-2 w-full mb-2"
            required
            autocomplete="email"
          />
          <input
            v-model="regPassword"
            name="password"
            type="password"
            placeholder="Password"
            class="border p-2 w-full mb-2"
            required
            autocomplete="new-password"
          />
          <input
            v-model="regConfirm"
            name="confirm"
            type="password"
            placeholder="Confirm Password"
            class="border p-2 w-full mb-2"
            required
            autocomplete="new-password"
          />
          <div class="flex justify-between">
            <button
              type="submit"
              class="bg-blue-600 text-white px-3 py-1 rounded"
            >
              Register
            </button>
            <button
              type="button"
              class="text-gray-600"
              @click="showRegister = false"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Password Reset Modal -->
    <div
      v-if="showReset"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white text-black p-6 rounded shadow w-80">
        <h2 class="text-lg font-bold mb-2">Reset Password</h2>
        <AppAlert :message="errorMessage" @close="clearError" />
        <form
          @submit.prevent="
            resetPassword(
              ($event.target as HTMLFormElement)?.email?.value || ''
            )
          "
        >
          <input
            name="email"
            type="email"
            placeholder="Email"
            class="border p-2 w-full mb-2"
            required
            autocomplete="email"
          />
          <div class="flex justify-between">
            <button
              type="submit"
              class="bg-gray-600 text-white px-3 py-1 rounded"
            >
              Send Reset Link
            </button>
            <button
              type="button"
              class="text-gray-600"
              @click="showReset = false"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppAlert from "~/components/AppAlert.vue";
import { useAuth } from "~/composables/useAuth";
import { ref } from "vue";

const {
  isAuthenticated,
  user,
  showLogin,
  showRegister,
  showReset,
  login,
  register,
  logout,
  resetPassword,
  errorMessage,
} = useAuth();

function clearError() {
  errorMessage.value = null;
}

const regEmail = ref("");
const regPassword = ref("");
const regConfirm = ref("");

function registerHandler(e: Event) {
  e.preventDefault();
  if (regPassword.value !== regConfirm.value) {
    errorMessage.value = "Passwords do not match";
    return;
  }
  register(regEmail.value, regPassword.value);
}
</script>

<style scoped></style>
