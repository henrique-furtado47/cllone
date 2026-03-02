import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application.json',
    },
})

// ==== Tasks ====

export const getTasks = () => api.get('/tasks/')
export const getTask = (id) => api.get(`/tasks/${id}/`)
export const createTask = (data) => api.post('/tasks/', data)
export const updateTask = (id, data) => api.put(`/tasks/${id}/`, data)
export const deleteTask = (id) => api.delete(`/tasks/${id}`)

// ==== Teams ====

export const getTeams = () => api.get('/teams/')
export const getTeam = (id) => api.get(`/teams/${id}/`)
export const createTeam = (data) => api.post('/teams/', data)
export const updateTeam = (id, data) => api.put(`/teams/${id}/`, data)
export const deleteTeam = (id) => api.delete(`/teams/${id}`)

// ==== Memberships ====

export const getMemberships = () => api.get('/memberships/')
export const createMemberships = (data) => api.post('/memberships/', data)
export const deleteMemberships = (id) => api.delete(`/memberships/${id}`)

export default api