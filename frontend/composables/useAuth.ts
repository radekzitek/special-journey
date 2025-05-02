import { ref } from 'vue'

const isAuthenticated = ref(false)
const user = ref<{ email: string } | null>(null)

const showLogin = ref(false)
const showRegister = ref(false)
const showReset = ref(false)

function login(email: string, password: string) {
  // Placeholder for backend API call
  isAuthenticated.value = true
  user.value = { email }
  showLogin.value = false
}

function register(email: string, password: string) {
  // Placeholder for backend API call
  isAuthenticated.value = true
  user.value = { email }
  showRegister.value = false
}

function logout() {
  isAuthenticated.value = false
  user.value = null
}

function resetPassword(email: string) {
  // Placeholder for backend API call
  showReset.value = false
}

export function useAuth() {
  return {
    isAuthenticated,
    user,
    showLogin,
    showRegister,
    showReset,
    login,
    register,
    logout,
    resetPassword
  }
}
