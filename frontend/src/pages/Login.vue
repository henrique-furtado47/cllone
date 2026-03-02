<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
console.log('Login.vue renderizado') // Log para verificar renderização
const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleSubmit() {
    error.value = ''
    loading.value = true
    try {
        await authStore.login(username.value, password.value)
        router.push('/')
    } catch (e) {
        error.value = 'Usuário ou senha inválidos.'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="login-wrapper">
        <form class="login-form" @submit.prevent="handleSubmit">
            <h2>Login</h2>

            <div v-if="error" class="error">{{ error }}</div>

            <label for="username">Usuário</label>
            <input
                id="username"
                v-model="username"
                type="text"
                placeholder="Digite seu usuário"
                required
                autocomplete="username"
            />

            <label for="password">Senha</label>
            <input
                id="password"
                v-model="password"
                type="password"
                placeholder="Digite sua senha"
                required
                autocomplete="current-password"
            />

            <button type="submit" :disabled="loading">
                {{ loading ? 'Entrando...' : 'Entrar' }}
            </button>
        </form>
    </div>
</template>

<style scoped>
.login-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

.login-form {
    background-color: var(--secondary-color);
    padding: 2rem;
    border-radius: 15px;
    box-shadow: rgba(0, 0, 0, 0.45) 5px 5px 2.6px;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    width: 320px;
}

.login-form h2 {
    text-align: center;
    color: white;
    margin-bottom: 0.5rem;
}

.login-form label {
    color: var(--text-color);
    font-size: 0.9rem;
}

.login-form input {
    padding: 0.5rem 0.75rem;
    border-radius: 8px;
    border: none;
    outline: none;
    font-size: 1rem;
}

.login-form button {
    margin-top: 0.5rem;
    padding: 0.6rem;
    background-color: var(--primary-color);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    transition: opacity 0.2s;
}

.login-form button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.error {
    background-color: #ff4d4d;
    color: white;
    padding: 0.5rem;
    border-radius: 6px;
    font-size: 0.85rem;
    text-align: center;
}
</style>