<script setup>
import { createTask } from '@/services/api'
import { ref, nextTick } from 'vue'
import { defineEmits } from 'vue'
const emit = defineEmits(['do-action'])
function triggerParent() {
  emit('do-action')
}

const isOpen = ref(false)
const searchValue = ref('')
const responseText = ref('')
const showResponse = ref(false)

const boxWidth = ref(50)

function toggleState(state) {
  boxWidth.value = state ? 300 : 50
}

async function handleSubmit(e) {
  e.preventDefault()

  toggleState(!isOpen.value)
  isOpen.value = !isOpen.value

  if (!isOpen.value) {
    handleRequest()
  } else {
    await nextTick()
    document.querySelector('.search-box')?.focus()
  }
}

function handleKeypress(e) {
  if (e.key === 'Enter') {
    toggleState(false)
    isOpen.value = false
    handleRequest()
  }
}

function handleBlur() {
  toggleState(false)
  isOpen.value = false
}

async function handleRequest() {
  const value = searchValue.value
  searchValue.value = ''

  if (value.length > 0) {
    await createTask({
      title: value,
      description: 'teste',
      status: 'todo',
      team: 1,
      assignee: 1,
    })
    triggerParent()
  }
}
</script>
<template>
  <div class="container">
    <div
      class="search-box-container"
      :style="{
        width: boxWidth + 'px',
        transition: 'width 0.6s cubic-bezier(.68,-0.55,.27,1.55)',
      }"
    >
      <button class="submit" @mousedown="handleSubmit">
        <i class="fa fa-solid fa-pen"></i>
      </button>

      <input
        class="search-box"
        type="text"
        v-model="searchValue"
        @keypress="handleKeypress"
        @blur="handleBlur"
      />
    </div>

    <h3
      class="response"
      :style="{
        opacity: showResponse ? 1 : 0,
        transition: 'opacity 0.3s ease',
      }"
    ></h3>
  </div>
</template>
<style scoped>
html,
body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: 'Ubuntu', sans-serif;
}

body {
  background-color: #ffecb3;
  overflow: hidden;
}

* {
  box-sizing: border-box;
}

.container {
  display: block;
  text-align: center;
  width: 100%;
  margin: 10% 0 0 0;
  transform: translateY(-50%);
  -moz-transform: translateY(-50%);
  -webkit-transform: translateY(-50%);
  -o-transform: translateY(-50%);
  -ms-transform: translateY(-50%);
}

.container:before {
  content: '';
  display: block;
  position: absolute;
  width: 150%;
  height: 100%;
  top: 0;
  left: -25%;
  transform: rotate(-3deg);
  -moz-transform: rotate(-3deg);
  -webkit-transform: rotate(-3deg);
  -o-transform: rotate(-3deg);
  -ms-transform: rotate(-3deg);
  z-index: -1;
}

h1 {
  font-family: 'Lato';
  font-size: 1.3em;
  color: white;
  letter-spacing: 1px;
  margin-bottom: 50px;
}

h3 {
  display: block;
  height: 19px;
  margin-top: 30px;
  font-family: 'Lato';
  font-size: 1em;
  color: white;
  opacity: 0;
}

.search-box-container {
  display: inline-block;
  box-sizing: content-box;
  height: 50px;
  width: 50px;
  padding: 0;
  background-color: white;
  border: 3px solid var(--primary-color);
  border-radius: 28px; /* (50px + 6px) / 2 */
  overflow: hidden;
}

.search-box-container * {
  display: inline-block;
  margin: 0;
  height: 100%;
  padding: 5px;
  border: 0;
  outline: none;
}

.search-box {
  width: calc(100% - 50px);
  padding: 0 20px;
  float: left;
  font-family: 'Ubuntu', sans-serif;
  font-size: 1em;
  color: var(--primary-color);
  background-color: white;
}

.submit {
  float: right;
  width: 50px;
  left: 0;
  top: 0;
  font-size: 1.2em;
  text-align: center;
  cursor: pointer;
  background-color: white;
}

.fa {
  display: inline !important;
  line-height: 100%;
  pointer-events: none;
  color: var(--primary-color);
}
</style>
