<script setup>
import TaskComp from '../components/taskComp.vue'
import TextBar from '../components/textBar.vue'

let tasks = [
  {
    title: 'Tarefa 1',
    id: 1,
  },
  {
    title: 'Tarefa 2',
    id: 2,
  },
  {
    title: 'Tarefa 3',
    id: 3,
  },
  {
    title: 'Tarefa 4',
    id: 4,
  },
]
</script>

<template>
  <div class="container">
    <div class="block">
      <h1>To-do List <i class="fa-solid fa-list"></i></h1>
      <TextBar />
      <TaskComp v-for="task in tasks" :key="task.id" :title="task.title" />
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
  padding: 1%;
  border-radius: 15px;
  box-shadow: rgba(0, 0, 0, 0.45) 5px 5px 2.6px;
}

.block h1 {
  text-align: center;
  color: white;
}
</style>
