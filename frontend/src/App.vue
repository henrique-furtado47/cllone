<script setup>
import TaskComp from './components/taskComp.vue'
import TextBar from './components/textBar.vue'
</script>

<template>
  <div class="container">
    <div class="block">
      <h1>To-do List <i class="fa-solid fa-list"></i></h1>
      <TextBar />
      <TaskComp />
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
