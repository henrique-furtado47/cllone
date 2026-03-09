import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Injeta o token em toda requisição, exceto em login e register
api.interceptors.request.use((config) => {
  const publicUrls = ['auth/login/', 'auth/register/']
  const isPublic = publicUrls.some((url) => config.url === url)
  if (!isPublic) {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
  }
  return config
})

// ==== Auth ====

export const login = (username, password) => api.post('auth/login/', { username, password })

export const register = (username, email, password, password2) =>
  api.post('auth/register/', { username, email, password, password2 })

export const getMe = () => api.get('auth/me/')
export const updateMe = (data) => api.patch('auth/me/', data)
export const changePassword = (current_password, new_password, new_password2) =>
  api.post('auth/change-password/', { current_password, new_password, new_password2 })

// ==== Tasks ====

export const getTasks = () => api.get('tasks/')
export const getTask = (id) => api.get(`tasks/${id}/`)
export const createTask = (data) => api.post('tasks/', data)
export const updateTask = (id, data) => api.patch(`tasks/${id}/`, data)
export const deleteTask = (id) => api.delete(`tasks/${id}/`)

// ==== Teams ====

export const getTeams = () => api.get('teams/')
export const getTeam = (id) => api.get(`teams/${id}/`)
export const createTeam = (data) => api.post('teams/', data)
export const updateTeam = (id, data) => api.put(`teams/${id}/`, data)
export const deleteTeam = (id) => api.delete(`teams/${id}/`)
export const addTeamMember = (teamId, data) => api.post(`teams/${teamId}/add-member/`, data)
export const removeTeamMember = (teamId, data) => api.post(`teams/${teamId}/remove-member/`, data)
export const changeTeamMemberRole = (teamId, data) => api.post(`teams/${teamId}/change-role/`, data)

// ==== Users ====

export const searchUsers = (query) => api.get(`users/search/?q=${encodeURIComponent(query)}`)

// ==== Memberships ====

export const getMemberships = () => api.get('memberships/')
export const createMembership = (data) => api.post('memberships/', data)
export const deleteMembership = (id) => api.delete(`memberships/${id}/`)

export default api
