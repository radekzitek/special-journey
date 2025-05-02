import { ref } from 'vue'

const isAuthenticated = ref(false)
const user = ref<{ email: string } | null>(null)
const showLogin = ref(false)
const showRegister = ref(false)
const showReset = ref(false)
const token = ref<string | null>(null)
const errorMessage = ref<string | null>(null)

const API_URL = 'http://localhost:8000/auth'

// Load token from localStorage on startup
if (typeof window !== 'undefined') {
  const savedToken = localStorage.getItem('access_token')
  if (savedToken) {
    token.value = savedToken
    isAuthenticated.value = true
    // Optionally, decode token to get user email
  }
}

async function login(email: string, password: string) {
  errorMessage.value = null
  try {
    const res = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ username: email, password })
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || 'Login failed')
    }
    const data = await res.json()
    token.value = data.access_token
    localStorage.setItem('access_token', data.access_token)
    isAuthenticated.value = true
    user.value = { email }
    showLogin.value = false
  } catch (e: unknown) {
    if (e instanceof Error) {
      errorMessage.value = e.message || 'Reset failed'
    } else {
      errorMessage.value = 'An unknown error occurred'
    }
    isAuthenticated.value = false
    user.value = null
    token.value = null
    localStorage.removeItem('access_token')
    errorMessage.value = e instanceof Error ? e.message || 'Login failed' : 'An unknown error occurred'
  }
}

async function register(email: string, password: string) {
  errorMessage.value = null
  try {
    const res = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || 'Registration failed')
    }
    await login(email, password)
    showRegister.value = false
  } catch (e: unknown) {
    if (e instanceof Error) {
      errorMessage.value = e.message || 'Registration failed'
    } else {
      errorMessage.value = 'An unknown error occurred'
    }
  }
}

async function logout() {
  errorMessage.value = null
  try {
    await fetch(`${API_URL}/logout`, { method: 'POST' })
  } catch {
    // Intentionally ignoring errors during logout
  }
  isAuthenticated.value = false
  user.value = null
  token.value = null
  localStorage.removeItem('access_token')
}

async function resetPassword(email: string, password: string = 'newpassword') {
  errorMessage.value = null
  try {
    const res = await fetch(`${API_URL}/reset-password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || 'Reset failed')
    }
    showReset.value = false
  } catch (e: unknown) {
    if (e instanceof Error) {
      errorMessage.value = e.message || 'Reset failed'
    } else {
      errorMessage.value = 'An unknown error occurred'
    }
  }
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
    resetPassword,
    token,
    errorMessage
  }
}
