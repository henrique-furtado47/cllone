<script>
import { deleteTask, getTeam, updateTask } from '@/services/api'

export default {
  data() {
    return {
      team_name: '',
    }
  },
  props: ['title', 'desc', 'stat', 'id', 'runParentFunction', 'team'],
  methods: {
    async getTeamName() {
      try {
        const response = await getTeam(this.team)
        this.team_name = response.data.name
      } catch (error) {
        console.error('Erro ao coletar nome do time:', error)
      }
    },
    async deleteTaskHandler() {
      if (confirm('Tem certeza que deseja excluir esta tarefa?')) {
        try {
          await deleteTask(this.id)
          this.runParentFunction()
        } catch (error) {
          console.error('Erro ao deletar tarefa:', error)
          alert('Erro ao excluir a tarefa')
        }
      }
    },
    async updateTaskHandler() {
      const newTitle = prompt('Digite o novo título da tarefa:', this.title)
      if (newTitle !== null && newTitle.trim() !== '') {
        try {
          await updateTask(this.id, { title: newTitle })
          this.runParentFunction()
        } catch (error) {
          console.error('Erro ao atualizar tarefa:', error)
          alert('Erro ao atualizar a tarefa')
        }
      }
    },
    async updateTaskStatus() {
      if (this.stat == 'todo') {
        try {
          await updateTask(this.id, { status: 'in_progress' })
          this.runParentFunction()
        } catch (error) {
          console.error('Erro ao atualizar tarefa:', error)
          alert('Erro ao atualizar a tarefa')
        }
      } else if (this.stat == 'in_progress') {
        try {
          await updateTask(this.id, { status: 'done' })
          this.runParentFunction()
        } catch (error) {
          console.error('Erro ao atualizar tarefa:', error)
          alert('Erro ao atualizar a tarefa')
        }
      } else {
        try {
          await updateTask(this.id, { status: 'todo' })
          this.runParentFunction()
        } catch (error) {
          console.error('Erro ao atualizar tarefa:', error)
          alert('Erro ao atualizar a tarefa')
        }
      }
    },
  },
  mounted() {
    this.getTeamName()
  },
}
</script>
<template>
  <div class="task">
    <div class="item esq">
      <h3>
        <button @click="updateTaskStatus">
          <i v-if="stat == 'done'" class="fa-solid fa-check"></i
          ><i v-if="stat == 'todo'" class="fa-solid fa-x"></i>
          <i v-if="stat == 'in_progress'" class="fa-solid fa-spinner"></i>
        </button>
        {{ title }}
      </h3>
    </div>
    <div class="item dir">
      <h3>
        <p v-if="team_name != ''" class="flavour-text">{{ team_name }}</p>
        <p v-if="stat == 'todo'" class="flavour-text">A fazer</p>
        <p v-if="stat == 'in_progress'" class="flavour-text">Em Andamento</p>
        <p v-if="stat == 'done'" class="flavour-text">Feita</p>
        <button @click="updateTaskHandler"><i class="fa fa-solid fa-pen-to-square"></i></button>
        <button @click="deleteTaskHandler"><i class="fa-solid fa-trash"></i></button>
      </h3>
    </div>
  </div>
</template>
<style scoped>
.task {
  background-color: white;
  color: var(--primary-color);
  padding: 4px 7px;
  border-radius: 15px;
  border: 3px solid var(--primary-color);
  justify-content: space-between;
  display: flex;
  margin: 10px;
}

h3 {
  font-size: 14px;
}

.item {
  width: 50%;
}

.flavour-text {
  font-size: 12px;
  margin: 5px;
  background-color: var(--third-color);
  padding: 5px 10px;
  border-radius: 10px;
  width: fit-content;
  display: inline-block;
}

.dir {
  text-align: right;
}

.esq {
  text-align: left;
  margin-top: 5px;
}

button {
  border: none;
  background: transparent;
  margin: 0 7px;
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
