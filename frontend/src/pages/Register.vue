<script setup>
import { register } from '@/services/api'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')
const error = ref('')
const loading = ref(false)

async function handleSubmit() {
    error.value = ''
    loading.value = true
    try {
        const response = await register(
            username.value,
            email.value,
            password.value,
            password2.value,
        )
        // Salva o token e redireciona para o login
        localStorage.setItem('token', response.data.token)
        localStorage.setItem('user', JSON.stringify({ username: username.value }))
        router.push('/')
    } catch (e) {
        if (e.response?.data?.error) {
            error.value = e.response.data.error
        } else {
            error.value = 'Erro ao criar conta. Tente novamente.'
        }
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="register-wrapper">
        <form class="register-form" @submit.prevent="handleSubmit">
            <h2>Criar Conta</h2>

            <div v-if="error" class="error">{{ error }}</div>

            <label for="username">Usuário</label>
            <input
                id="username"
                v-model="username"
                type="text"
                placeholder="Escolha um nome de usuário"
                required
                autocomplete="username"
            />

            <label for="email">E-mail (opcional)</label>
            <input
                id="email"
                v-model="email"
                type="email"
                placeholder="Digite seu e-mail"
                autocomplete="email"
            />

            <label for="password">Senha</label>
            <input
                id="password"
                v-model="password"
                type="password"
                placeholder="Digite sua senha"
                required
                autocomplete="new-password"
            />

            <label for="password2">Confirmar Senha</label>
            <input
                id="password2"
                v-model="password2"
                type="password"
                placeholder="Repita a senha"
                required
                autocomplete="new-password"
            />

            <button type="submit" :disabled="loading">
                {{ loading ? 'Criando...' : 'Criar Conta' }}
            </button>

            <p class="login-link">
                Já tem conta? <router-link to="/login">Entrar</router-link>
            </p>
        </form>
    </div>
</template>

<style scoped>
.register-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

.register-form {
    background-color: var(--secondary-color);
    padding: 2rem;
    border-radius: 15px;
    box-shadow: rgba(0, 0, 0, 0.45) 5px 5px 2.6px;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    width: 320px;
}

.register-form h2 {
    text-align: center;
    color: white;
    margin-bottom: 0.5rem;
}

.register-form label {
    color: var(--text-color);
    font-size: 0.9rem;
}

.register-form input {
    padding: 0.5rem 0.75rem;
    border-radius: 8px;
    border: none;
    outline: none;
    font-size: 1rem;
}

.register-form button {
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

.register-form button:disabled {
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

.login-link {
    text-align: center;
    color: var(--text-color);
    font-size: 0.85rem;
    margin-top: 0.25rem;
}

.login-link a {
    color: var(--primary-color);
    text-decoration: none;
    font-weight: bold;
}

.login-link a:hover {
    text-decoration: underline;
}
</style>
