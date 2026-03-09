<script setup>
import TaskComp from '@/components/taskComp.vue'
import TextBar from '@/components/textBar.vue'
import { ref, onMounted } from 'vue'
import { getTasks } from '@/services/api'

const tasks = ref([])

async function loadTasks() {
  try {
    const response = await getTasks()
    tasks.value = response.data
  } catch (error) {
    console.error('Erro ao carregar tasks:', error)
  }
}

function handleChildAction() {
  loadTasks()
}

onMounted(() => {
  loadTasks()
})
</script>

<template>
  <div class="container">
    <div class="block">
      <h1>To-do List <i class="fa-solid fa-list"></i></h1>
      <TextBar @do-action="handleChildAction" />
      <TaskComp
        v-for="task in tasks"
        :key="task.id"
        :title="task.title"
        :desc="task.description"
        :stat="task.status"
        :id="task.id"
        :runParentFunction="handleChildAction"
        :team="task.team"
      />
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
  width: 60%;
  margin: 5%;
  padding: 1%;
  border-radius: 15px;
  box-shadow: rgba(0, 0, 0, 0.45) 5px 5px 2.6px;
}

.block h1 {
  text-align: center;
  color: white;
}
</style>
