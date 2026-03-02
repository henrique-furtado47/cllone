<script setup>
import TextBar from '@/components/textBar.vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="container">
    <div class="block">
      <div class="header">
        <h1>To-do List <i class="fa-solid fa-list"></i></h1>
        <div class="user-info">
          <span>{{ auth.user?.username }}</span>
          <button class="logout-btn" @click="logout">Sair</button>
        </div>
      </div>
      <TextBar />
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.block {
  background-color: var(--secondary-color);
  width: 40%;
  margin: 5%;
  padding: 1.5%;
  border-radius: 15px;
  box-shadow: rgba(0, 0, 0, 0.45) 5px 5px 2.6px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.block h1 {
  color: white;
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--text-color);
  font-size: 0.9rem;
}

.logout-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.3rem 0.75rem;
  cursor: pointer;
  font-size: 0.85rem;
  transition: opacity 0.2s;
}

.logout-btn:hover {
  opacity: 0.8;
}
</style>
