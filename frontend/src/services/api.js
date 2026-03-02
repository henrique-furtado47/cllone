import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application.json',
    },
})

// ==== Tasks ====

export const getTasks = () => api.get('/tasks/')
export const getTask = (id) => api.get(`tasks/${id}/`)
export const createTask = (data) => api.post('/tasks/', data)
export const updateTask = (id, data) => api.put(`task/${id}/`, data)
export const deleteTask = (id) => api.delete(`tasks/${id}`)