<script setup>
import { changePassword, getMe } from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import { onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()

const open = ref(false)
const tab = ref('profile') // 'profile' | 'password'
const menuRef = ref(null)

// Dados do perfil
const profile = ref(null)
const loadingProfile = ref(true)

// Alterar senha
const currentPassword = ref('')
const newPassword = ref('')
const newPassword2 = ref('')
const passwordMsg = ref('')
const passwordError = ref(false)
const savingPassword = ref(false)

async function loadProfile() {
  try {
    loadingProfile.value = true
    const res = await getMe()
    profile.value = res.data
  } catch {
    profile.value = null
  } finally {
    loadingProfile.value = false
  }
}

async function handleChangePassword() {
  passwordMsg.value = ''
  passwordError.value = false
  savingPassword.value = true
  try {
    const res = await changePassword(
      currentPassword.value,
      newPassword.value,
      newPassword2.value,
    )
    // Atualizar token no store
    authStore.token = res.data.token
    localStorage.setItem('token', res.data.token)
    passwordMsg.value = 'Senha alterada com sucesso!'
    currentPassword.value = ''
    newPassword.value = ''
    newPassword2.value = ''
  } catch (e) {
    passwordError.value = true
    passwordMsg.value = e.response?.data?.error || 'Erro ao alterar senha.'
  } finally {
    savingPassword.value = false
  }
}

function handleLogout() {
  authStore.logout()
  open.value = false
  router.push('/login')
}

function toggleMenu() {
  open.value = !open.value
  if (open.value) {
    tab.value = 'profile'
    passwordMsg.value = ''
    loadProfile()
  }
}

// Fechar ao clicar fora
function onClickOutside(e) {
  if (menuRef.value && !menuRef.value.contains(e.target)) {
    open.value = false
  }
}

onMounted(() => document.addEventListener('click', onClickOutside))
onUnmounted(() => document.removeEventListener('click', onClickOutside))

const initials = (name) => {
  if (!name) return '?'
  return name.charAt(0).toUpperCase()
}
</script>

<template>
  <div class="user-menu" ref="menuRef">
    <button class="avatar-btn" @click.stop="toggleMenu" :title="authStore.user?.username">
      {{ initials(authStore.user?.username) }}
    </button>

    <Transition name="dropdown">
      <div v-if="open" class="dropdown">
        <!-- Tabs -->
        <div class="tabs">
          <button :class="{ active: tab === 'profile' }" @click="tab = 'profile'">Perfil</button>
          <button :class="{ active: tab === 'password' }" @click="tab = 'password'">Senha</button>
        </div>

        <!-- Profile Tab -->
        <div v-if="tab === 'profile'" class="tab-content">
          <div v-if="loadingProfile" class="loading">Carregando...</div>
          <template v-else-if="profile">
            <div class="info-row">
              <span class="label">Usuário</span>
              <span class="value">{{ profile.username }}</span>
            </div>
            <div class="info-row">
              <span class="label">E-mail</span>
              <span class="value">{{ profile.email || '—' }}</span>
            </div>
            <div class="info-row">
              <span class="label">Nome</span>
              <span class="value">
                {{ [profile.first_name, profile.last_name].filter(Boolean).join(' ') || '—' }}
              </span>
            </div>
            <div class="teams-section">
              <span class="label">Times</span>
              <div v-if="profile.teams.length" class="teams-list">
                <span v-for="team in profile.teams" :key="team.id" class="team-badge">
                  {{ team.name }}
                </span>
              </div>
              <span v-else class="value">Nenhum time</span>
            </div>
          </template>
        </div>

        <!-- Password Tab -->
        <div v-if="tab === 'password'" class="tab-content">
          <form @submit.prevent="handleChangePassword" class="password-form">
            <input
              v-model="currentPassword"
              type="password"
              placeholder="Senha atual"
              required
              autocomplete="current-password"
            />
            <input
              v-model="newPassword"
              type="password"
              placeholder="Nova senha"
              required
              autocomplete="new-password"
            />
            <input
              v-model="newPassword2"
              type="password"
              placeholder="Confirmar nova senha"
              required
              autocomplete="new-password"
            />
            <div v-if="passwordMsg" :class="['msg', passwordError ? 'msg-error' : 'msg-success']">
              {{ passwordMsg }}
            </div>
            <button type="submit" :disabled="savingPassword" class="btn-save">
              {{ savingPassword ? 'Salvando...' : 'Alterar Senha' }}
            </button>
          </form>
        </div>

        <!-- Logout -->
        <button class="btn-logout" @click="handleLogout">
          <i class="fa-solid fa-right-from-bracket"></i> Sair
        </button>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.user-menu {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 1000;
}

.avatar-btn {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: 2px solid var(--text-color);
  background-color: var(--primary-color);
  color: var(--text-color);
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s, box-shadow 0.15s;
}
.avatar-btn:hover {
  transform: scale(1.08);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
}

.dropdown {
  position: absolute;
  top: 52px;
  right: 0;
  width: 280px;
  background-color: var(--secondary-color);
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Tabs */
.tabs {
  display: flex;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
}
.tabs button {
  flex: 1;
  padding: 0.6rem;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.2s, border-bottom 0.2s;
  border-bottom: 2px solid transparent;
}
.tabs button.active {
  color: var(--text-color);
  border-bottom-color: var(--text-color);
}

/* Tab content */
.tab-content {
  padding: 0.75rem 1rem;
}

.loading {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.85rem;
  text-align: center;
  padding: 1rem 0;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 0.35rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.info-row:last-child {
  border-bottom: none;
}

.label {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.8rem;
  font-weight: 600;
}
.value {
  color: white;
  font-size: 0.85rem;
  text-align: right;
}

/* Teams */
.teams-section {
  padding-top: 0.5rem;
}
.teams-section .label {
  display: block;
  margin-bottom: 0.35rem;
}
.teams-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
}
.team-badge {
  background-color: var(--primary-color);
  color: var(--text-color);
  padding: 0.2rem 0.55rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

/* Password form */
.password-form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.password-form input {
  padding: 0.45rem 0.6rem;
  border-radius: 8px;
  border: none;
  outline: none;
  font-size: 0.9rem;
}

.btn-save {
  padding: 0.5rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.msg {
  font-size: 0.8rem;
  padding: 0.35rem 0.5rem;
  border-radius: 6px;
  text-align: center;
}
.msg-success {
  background-color: rgba(0, 200, 80, 0.2);
  color: #a5ffb0;
}
.msg-error {
  background-color: rgba(255, 77, 77, 0.2);
  color: #ff9e9e;
}

/* Logout */
.btn-logout {
  margin: 0.5rem 1rem 0.75rem;
  padding: 0.5rem;
  background-color: rgba(255, 77, 77, 0.15);
  color: #ff6b6b;
  border: 1px solid rgba(255, 77, 77, 0.3);
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}
.btn-logout:hover {
  background-color: rgba(255, 77, 77, 0.3);
}

/* Transition */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
