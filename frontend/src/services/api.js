import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:8000/api/',
    headers: {
        'Content-Type': 'application/json',
    },
})

// Injeta o token em toda requisição, exceto no login
api.interceptors.request.use((config) => {
    const isLoginRequest = config.url === 'auth/login/'
    if (!isLoginRequest) {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Token ${token}`
        }
    }
    return config
})

// ==== Auth ====

export const login = (username, password) =>
    api.post('auth/login/', { username, password })

// ==== Tasks ====

export const getTasks = () => api.get('tasks/')
export const getTask = (id) => api.get(`tasks/${id}/`)
export const createTask = (data) => api.post('tasks/', data)
export const updateTask = (id, data) => api.put(`tasks/${id}/`, data)
export const deleteTask = (id) => api.delete(`tasks/${id}/`)

// ==== Teams ====

export const getTeams = () => api.get('teams/')
export const getTeam = (id) => api.get(`teams/${id}/`)
export const createTeam = (data) => api.post('teams/', data)
export const updateTeam = (id, data) => api.put(`teams/${id}/`, data)
export const deleteTeam = (id) => api.delete(`teams/${id}/`)

// ==== Memberships ====

export const getMemberships = () => api.get('memberships/')
export const createMembership = (data) => api.post('memberships/', data)
export const deleteMembership = (id) => api.delete(`memberships/${id}/`)

export default api