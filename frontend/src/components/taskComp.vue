<script>
export default {
  props: ['title', 'desc', 'stat', 'id', 'runParentFunction'],
}
</script>
<template>
  <div class="task">
    <div class="item">
      <h3>
        <button><i class="fa-solid fa-check"></i></button> {{ title }}
      </h3>
    </div>
    <div class="item dir">
      <h3>
        <button><i class="fa-solid fa-eye"></i></button>
        <button><i class="fa fa-solid fa-pen-to-square"></i></button>
        <button><i class="fa-solid fa-trash"></i></button>
      </h3>
    </div>
  </div>
</template>
<style scoped>
.task {
  background-color: white;
  color: var(--primary-color);
  padding: 10px 20px;
  border-radius: 15px;
  border: 3px solid var(--primary-color);
  justify-content: space-between;
  display: flex;
}

.item {
  width: 40%;
}

.dir {
  text-align: right;
}

button {
  border: none;
  background: transparent;
  margin: 0 10px;
  font-size: large;
  transition: 0.25s;
  color: var(--primary-color);
}

button:hover {
  transform: scale(1.2);
  cursor: pointer;
  color: red;
}
</style>
