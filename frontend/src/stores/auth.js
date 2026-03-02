import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { login as loginApi } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isLoggedIn = computed(() => !!token.value)

  async function login(username, password) {
    // Limpa token antigo antes de tentar autenticar
    localStorage.removeItem('token')
    token.value = null

    const response = await loginApi(username, password)
    token.value = response.data.token

    // O DRF retorna só o token; guardamos o username localmente
    user.value = { username }

    localStorage.setItem('token', token.value)
    localStorage.setItem('user', JSON.stringify(user.value))
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return { token, user, isLoggedIn, login, logout }
})
