<script setup>
import {
    addTeamMember,
    changeTeamMemberRole,
    createTeam,
    deleteTeam,
    getTeams,
    removeTeamMember,
    searchUsers,
    updateTeam,
} from '@/services/api'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// ── Estado geral ──
const teams = ref([])
const loading = ref(true)
const selectedTeam = ref(null)
const error = ref('')

// ── Criar time ──
const showCreateModal = ref(false)
const newTeamName = ref('')
const newTeamDesc = ref('')
const creating = ref(false)

// ── Editar time ──
const showEditModal = ref(false)
const editTeamName = ref('')
const editTeamDesc = ref('')
const editing = ref(false)

// ── Adicionar membro ──
const showAddMember = ref(false)
const searchQuery = ref('')
const searchResults = ref([])
const searching = ref(false)
const addingMember = ref(false)

// ── Carregar times ──
async function loadTeams() {
  loading.value = true
  try {
    const res = await getTeams()
    teams.value = res.data
    // Se um time estava selecionado, atualizar seus dados
    if (selectedTeam.value) {
      const updated = teams.value.find((t) => t.id === selectedTeam.value.id)
      selectedTeam.value = updated || null
    }
  } catch (e) {
    error.value = 'Erro ao carregar times.'
  } finally {
    loading.value = false
  }
}

// ── Criar time ──
async function handleCreateTeam() {
  if (!newTeamName.value.trim()) return
  creating.value = true
  error.value = ''
  try {
    await createTeam({ name: newTeamName.value.trim(), description: newTeamDesc.value.trim() })
    newTeamName.value = ''
    newTeamDesc.value = ''
    showCreateModal.value = false
    await loadTeams()
  } catch (e) {
    error.value = e.response?.data?.name?.[0] || e.response?.data?.detail || 'Erro ao criar time.'
  } finally {
    creating.value = false
  }
}

// ── Selecionar time ──
function selectTeam(team) {
  selectedTeam.value = team
  showAddMember.value = false
  searchQuery.value = ''
  searchResults.value = []
}

// ── Editar time ──
function openEditModal() {
  editTeamName.value = selectedTeam.value.name
  editTeamDesc.value = selectedTeam.value.description || ''
  showEditModal.value = true
}

async function handleEditTeam() {
  editing.value = true
  error.value = ''
  try {
    await updateTeam(selectedTeam.value.id, {
      name: editTeamName.value.trim(),
      description: editTeamDesc.value.trim(),
    })
    showEditModal.value = false
    await loadTeams()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erro ao editar time.'
  } finally {
    editing.value = false
  }
}

// ── Excluir time ──
async function handleDeleteTeam() {
  if (!confirm(`Tem certeza que deseja excluir o time "${selectedTeam.value.name}"?`)) return
  error.value = ''
  try {
    await deleteTeam(selectedTeam.value.id)
    selectedTeam.value = null
    await loadTeams()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erro ao excluir time.'
  }
}

// ── Buscar usuários ──
let searchTimeout = null
function onSearchInput() {
  clearTimeout(searchTimeout)
  if (searchQuery.value.trim().length < 2) {
    searchResults.value = []
    return
  }
  searchTimeout = setTimeout(async () => {
    searching.value = true
    try {
      const res = await searchUsers(searchQuery.value.trim())
      // Filtrar membros que já estão no time
      const existingIds = selectedTeam.value.memberships.map((m) => m.user_id)
      searchResults.value = res.data.filter((u) => !existingIds.includes(u.id))
    } catch {
      searchResults.value = []
    } finally {
      searching.value = false
    }
  }, 300)
}

// ── Adicionar membro ──
async function handleAddMember(user) {
  addingMember.value = true
  error.value = ''
  try {
    await addTeamMember(selectedTeam.value.id, { username: user.username, role: 'member' })
    searchQuery.value = ''
    searchResults.value = []
    showAddMember.value = false
    await loadTeams()
  } catch (e) {
    error.value = e.response?.data?.error || 'Erro ao adicionar membro.'
  } finally {
    addingMember.value = false
  }
}

// ── Remover membro ──
async function handleRemoveMember(membership) {
  if (!confirm(`Remover ${membership.username} do time?`)) return
  error.value = ''
  try {
    await removeTeamMember(selectedTeam.value.id, { user_id: membership.user_id })
    await loadTeams()
  } catch (e) {
    error.value = e.response?.data?.error || 'Erro ao remover membro.'
  }
}

// ── Alterar role ──
async function handleChangeRole(membership) {
  const newRole = membership.role === 'admin' ? 'member' : 'admin'
  error.value = ''
  try {
    await changeTeamMemberRole(selectedTeam.value.id, {
      user_id: membership.user_id,
      role: newRole,
    })
    await loadTeams()
  } catch (e) {
    error.value = e.response?.data?.error || 'Erro ao alterar papel.'
  }
}

// ── Verificar se o user logado é admin do time selecionado ──
const isAdmin = computed(() => {
  if (!selectedTeam.value) return false
  const me = JSON.parse(localStorage.getItem('user') || '{}')
  return selectedTeam.value.memberships?.some(
    (m) => m.username === me.username && m.role === 'admin',
  )
})

function goHome() {
  router.push('/')
}

onMounted(() => {
  loadTeams()
})
</script>

<template>
  <div class="teams-page">
    <!-- Cabeçalho -->
    <div class="teams-header">
      <button class="back-btn" @click="goHome" title="Voltar">
        <i class="fa-solid fa-arrow-left"></i>
      </button>
      <h1><i class="fa-solid fa-people-group"></i> Meus Times</h1>
      <button class="create-btn" @click="showCreateModal = true">
        <i class="fa-solid fa-plus"></i> Novo Time
      </button>
    </div>

    <!-- Mensagem de erro -->
    <div v-if="error" class="error-banner">
      {{ error }}
      <button @click="error = ''" class="close-error">&times;</button>
    </div>

    <div class="teams-layout">
      <!-- Lista de times -->
      <div class="teams-sidebar">
        <div v-if="loading" class="loading-msg">Carregando...</div>
        <div v-else-if="teams.length === 0" class="empty-msg">
          Você não está em nenhum time.<br />Crie um para começar!
        </div>
        <div
          v-for="team in teams"
          :key="team.id"
          class="team-card"
          :class="{ active: selectedTeam?.id === team.id }"
          @click="selectTeam(team)"
        >
          <div class="team-card-icon">
            <i class="fa-solid fa-users"></i>
          </div>
          <div class="team-card-info">
            <h3>{{ team.name }}</h3>
            <span class="member-count">{{ team.member_count }} membro{{ team.member_count !== 1 ? 's' : '' }}</span>
          </div>
        </div>
      </div>

      <!-- Detalhes do time selecionado -->
      <div class="team-detail" v-if="selectedTeam">
        <div class="detail-header">
          <div>
            <h2>{{ selectedTeam.name }}</h2>
            <p class="team-desc" v-if="selectedTeam.description">{{ selectedTeam.description }}</p>
          </div>
          <div class="detail-actions" v-if="isAdmin">
            <button @click="openEditModal" class="action-btn edit" title="Editar time">
              <i class="fa-solid fa-pen"></i>
            </button>
            <button @click="handleDeleteTeam" class="action-btn delete" title="Excluir time">
              <i class="fa-solid fa-trash"></i>
            </button>
          </div>
        </div>

        <!-- Membros -->
        <div class="members-section">
          <div class="members-header">
            <h3><i class="fa-solid fa-user-group"></i> Membros</h3>
            <button v-if="isAdmin" class="add-member-btn" @click="showAddMember = !showAddMember">
              <i class="fa-solid fa-user-plus"></i> Adicionar
            </button>
          </div>

          <!-- Buscar e adicionar membro -->
          <div v-if="showAddMember" class="add-member-box">
            <input
              v-model="searchQuery"
              @input="onSearchInput"
              type="text"
              placeholder="Buscar usuário por nome..."
              class="search-input"
            />
            <div v-if="searching" class="search-loading">Buscando...</div>
            <div v-if="searchResults.length" class="search-results">
              <div
                v-for="user in searchResults"
                :key="user.id"
                class="search-result-item"
                @click="handleAddMember(user)"
              >
                <span class="result-avatar">{{ user.username.charAt(0).toUpperCase() }}</span>
                <span class="result-name">{{ user.username }}</span>
                <span class="result-email">{{ user.email }}</span>
                <i class="fa-solid fa-plus add-icon"></i>
              </div>
            </div>
            <div v-if="searchQuery.length >= 2 && !searching && searchResults.length === 0" class="no-results">
              Nenhum usuário encontrado.
            </div>
          </div>

          <!-- Lista de membros -->
          <div class="members-list">
            <div v-for="member in selectedTeam.memberships" :key="member.id" class="member-item">
              <div class="member-avatar">{{ member.username.charAt(0).toUpperCase() }}</div>
              <div class="member-info">
                <span class="member-name">{{ member.username }}</span>
                <span class="member-role" :class="member.role">
                  {{ member.role === 'admin' ? 'Admin' : 'Membro' }}
                </span>
              </div>
              <div class="member-actions" v-if="isAdmin">
                <button
                  @click="handleChangeRole(member)"
                  class="role-btn"
                  :title="member.role === 'admin' ? 'Rebaixar para membro' : 'Promover a admin'"
                >
                  <i :class="member.role === 'admin' ? 'fa-solid fa-arrow-down' : 'fa-solid fa-arrow-up'"></i>
                </button>
                <button @click="handleRemoveMember(member)" class="remove-btn" title="Remover membro">
                  <i class="fa-solid fa-xmark"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Placeholder quando nenhum time selecionado -->
      <div class="team-detail placeholder" v-else-if="!loading && teams.length > 0">
        <i class="fa-solid fa-arrow-left"></i>
        <p>Selecione um time para ver os detalhes</p>
      </div>
    </div>

    <!-- Modal Criar Time -->
    <Teleport to="body">
      <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
        <div class="modal">
          <h2>Criar Novo Time</h2>
          <form @submit.prevent="handleCreateTeam">
            <input
              v-model="newTeamName"
              type="text"
              placeholder="Nome do time"
              required
              class="modal-input"
            />
            <textarea
              v-model="newTeamDesc"
              placeholder="Descrição (opcional)"
              class="modal-input modal-textarea"
            ></textarea>
            <div class="modal-actions">
              <button type="button" @click="showCreateModal = false" class="modal-btn cancel">Cancelar</button>
              <button type="submit" :disabled="creating" class="modal-btn confirm">
                {{ creating ? 'Criando...' : 'Criar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- Modal Editar Time -->
    <Teleport to="body">
      <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal = false">
        <div class="modal">
          <h2>Editar Time</h2>
          <form @submit.prevent="handleEditTeam">
            <input
              v-model="editTeamName"
              type="text"
              placeholder="Nome do time"
              required
              class="modal-input"
            />
            <textarea
              v-model="editTeamDesc"
              placeholder="Descrição (opcional)"
              class="modal-input modal-textarea"
            ></textarea>
            <div class="modal-actions">
              <button type="button" @click="showEditModal = false" class="modal-btn cancel">Cancelar</button>
              <button type="submit" :disabled="editing" class="modal-btn confirm">
                {{ editing ? 'Salvando...' : 'Salvar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.teams-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.teams-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.teams-header h1 {
  flex: 1;
  color: #fff;
  font-size: 1.6rem;
  margin: 0;
}

.back-btn {
  background: var(--secondary-color);
  border: none;
  color: #fff;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 1.1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}
.back-btn:hover {
  background: var(--primary-color);
}

.create-btn {
  background: var(--primary-color);
  color: #fff;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-size: 0.95rem;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s;
}
.create-btn:hover {
  background: #004f50;
}

.error-banner {
  background: #e74c3c;
  color: #fff;
  padding: 0.7rem 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.close-error {
  background: none;
  border: none;
  color: #fff;
  font-size: 1.2rem;
  cursor: pointer;
}

.teams-layout {
  display: flex;
  gap: 1.5rem;
  min-height: 500px;
}

/* ── Sidebar ── */
.teams-sidebar {
  width: 300px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.loading-msg,
.empty-msg {
  color: #fff;
  text-align: center;
  padding: 2rem 1rem;
  background: var(--secondary-color);
  border-radius: 12px;
}

.team-card {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  background: var(--secondary-color);
  padding: 1rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}
.team-card:hover {
  background: var(--primary-color);
}
.team-card.active {
  border-color: var(--text-color);
  background: var(--primary-color);
}
.team-card-icon {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 1.1rem;
}
.team-card-info h3 {
  color: #fff;
  margin: 0;
  font-size: 1rem;
}
.member-count {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.8rem;
}

/* ── Detalhe ── */
.team-detail {
  flex: 1;
  background: var(--secondary-color);
  border-radius: 12px;
  padding: 1.5rem;
}
.team-detail.placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.5);
  font-size: 1.1rem;
  gap: 0.5rem;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 1rem;
}
.detail-header h2 {
  color: #fff;
  margin: 0 0 0.3rem 0;
}
.team-desc {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  font-size: 0.9rem;
}

.detail-actions {
  display: flex;
  gap: 0.5rem;
}
.action-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  transition: background 0.2s;
}
.action-btn.edit {
  background: #2980b9;
}
.action-btn.edit:hover {
  background: #1f6fa3;
}
.action-btn.delete {
  background: #e74c3c;
}
.action-btn.delete:hover {
  background: #c0392b;
}

/* ── Membros ── */
.members-section {
  margin-top: 0.5rem;
}
.members-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.members-header h3 {
  color: #fff;
  margin: 0;
  font-size: 1.1rem;
}
.add-member-btn {
  background: var(--primary-color);
  color: #fff;
  border: none;
  padding: 0.4rem 0.9rem;
  border-radius: 8px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background 0.2s;
}
.add-member-btn:hover {
  background: #004f50;
}

/* ── Busca de membro ── */
.add-member-box {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1rem;
}
.search-input {
  width: 100%;
  padding: 0.6rem 0.8rem;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  outline: none;
  box-sizing: border-box;
}
.search-loading {
  color: rgba(255, 255, 255, 0.6);
  padding: 0.5rem 0;
  font-size: 0.85rem;
}
.search-results {
  margin-top: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}
.search-result-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.5rem 0.7rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s;
  color: #fff;
}
.search-result-item:hover {
  background: rgba(255, 255, 255, 0.1);
}
.result-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
}
.result-name {
  font-weight: 600;
}
.result-email {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.8rem;
  flex: 1;
}
.add-icon {
  color: var(--text-color);
}
.no-results {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.85rem;
  padding: 0.5rem 0;
}

/* ── Lista de membros ── */
.members-list {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.member-item {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  background: rgba(0, 0, 0, 0.15);
  padding: 0.7rem 1rem;
  border-radius: 10px;
}
.member-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 700;
  font-size: 0.95rem;
}
.member-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.member-name {
  color: #fff;
  font-weight: 600;
  font-size: 0.95rem;
}
.member-role {
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 4px;
  padding: 0.1rem 0.4rem;
  width: fit-content;
  margin-top: 0.15rem;
}
.member-role.admin {
  background: #f39c12;
  color: #fff;
}
.member-role.member {
  background: rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.8);
}

.member-actions {
  display: flex;
  gap: 0.3rem;
}
.role-btn,
.remove-btn {
  width: 30px;
  height: 30px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 0.8rem;
  transition: background 0.2s;
}
.role-btn {
  background: #2980b9;
}
.role-btn:hover {
  background: #1f6fa3;
}
.remove-btn {
  background: #e74c3c;
}
.remove-btn:hover {
  background: #c0392b;
}

/* ── Modais ── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal {
  background: var(--secondary-color);
  border-radius: 14px;
  padding: 2rem;
  width: 90%;
  max-width: 420px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
.modal h2 {
  color: #fff;
  margin: 0 0 1.2rem 0;
  text-align: center;
}
.modal-input {
  width: 100%;
  padding: 0.65rem 0.8rem;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  margin-bottom: 0.8rem;
  outline: none;
  box-sizing: border-box;
}
.modal-textarea {
  min-height: 80px;
  resize: vertical;
  font-family: inherit;
}
.modal-actions {
  display: flex;
  gap: 0.8rem;
  justify-content: flex-end;
  margin-top: 0.5rem;
}
.modal-btn {
  padding: 0.55rem 1.3rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.modal-btn.cancel {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
}
.modal-btn.cancel:hover {
  background: rgba(255, 255, 255, 0.25);
}
.modal-btn.confirm {
  background: var(--primary-color);
  color: #fff;
}
.modal-btn.confirm:hover {
  background: #004f50;
}
.modal-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ── Responsivo ── */
@media (max-width: 768px) {
  .teams-layout {
    flex-direction: column;
  }
  .teams-sidebar {
    width: 100%;
  }
}
</style>
