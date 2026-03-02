<script setup>
import TextBar from './components/textBar.vue'
</script>

<template>
  <div class="container">
    <div class="block">
      <h1>To-do List <i class="fa-solid fa-list"></i></h1>
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
  height: 200px;
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
