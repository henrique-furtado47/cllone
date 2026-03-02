<script setup>
import UserMenu from '@/components/UserMenu.vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore()
</script>

<template>
  <div class="container">
    <UserMenu v-if="authStore.isLoggedIn" />
    <RouterView />
  </div>
</template>
 
