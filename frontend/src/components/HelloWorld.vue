<template>
  <v-app id="inspire">
    <v-app-bar class="px-3" color="white" flat density="compact">
      <v-spacer></v-spacer>
      <v-tabs centered color="grey-darken-2">
        <v-tab v-for="link in links" :key="link">
          {{ link }}
        </v-tab>
      </v-tabs>
      <v-spacer></v-spacer>

      <v-avatar color="grey-darken-1" size="32"></v-avatar>
    </v-app-bar>

    <v-main class="bg-grey-lighten-3">
      <v-container>
        <v-row>
          <v-col cols="12" sm="8">
            <v-sheet rounded class="d-flex justify-center">

              <v-sheet :color="color" :height="225" :width="250" class="my-10 pa-10 text-center" @click="saveResult">
                <p>Жми сюда, когда поменяется цвет станет зеленым</p>
                <p v-if="error">Рано!</p>
                <p>Результат: {{ lastResult }} мс.</p>
              </v-sheet>

            </v-sheet>
          </v-col>

          <v-col cols="12" sm="4">
            <v-sheet min-height="80vh" rounded>
              <v-table>
                <thead>
                  <tr>
                    <th class="text-left">
                      Имя
                    </th>
                    <th class="text-left">
                      Скорость реакции
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="leader in leaders" :key="leader.id">
                    <td>{{ leader.name }} #{{ leader.id }}</td>
                    <td>{{ leader.time }} мс</td>
                  </tr>
                </tbody>
              </v-table>
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
      <div class="text-center">
        <v-dialog v-model="showModal" width="500px">

          <v-card>
            <v-card-text>
              Введите ваше имя:
              <v-text-field v-model="name" label="Мое имя" required></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-btn color="primary" block @click="createUser">Сохранить</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </div>
    </v-main>
  </v-app>
</template>

<script>
import axios from 'axios'

export default {
  data: () => ({
    userId: null,
    name: null,
    error: false,
    startTime: new Date(),
    endTime: new Date(),
    delta: 0,
    lastResult: 0,
    clicked: false,
    defaultColor: 'info',
    links: [
      'Главная',
    ],
    leaders: []
  }),
  computed: {
    showModal() {
      return !this.userId
    },
    getDelta() {
      return this.delta
    },
    color() {
      return this.defaultColor
    },
    elapsed() {
      return true
    },
  },
  mounted() {
    this.changeColor()
    setInterval(this.getLeaders, 3000);
  },
  methods: {

    saveResult() {
      if (this.defaultColor === 'info' || this.defaultColor === 'error') {
        this.error = true;
        this.defaultColor = 'error'

      }
      else {
        this.error = false;
        this.defaultColor = 'info'
        this.endTime = new Date();
        this.delta = this.endTime - this.startTime
        this.lastResult = this.delta;
        this.saveTime(this.delta)
        this.changeColor()
      }

    },

    changeColor() {
      if (this.userId) {
        const randomValue = Math.random() * 15000;
        setTimeout(() => {
          this.defaultColor = 'green'
          this.startTime = new Date();
        }, randomValue)
      }

    },
    getLeaders() {
      if (this.userId) {
        axios
          .get('http://45.12.75.118:8000/leaders')
          .then(response => (this.leaders = response.data));
      }
    },
    saveTime(time) {
      const payload = {
        time: time,
        user_id: this.userId
      }
      axios.post('http://45.12.75.118:8000/reactions', payload)
    },
    createUser() {
      axios.post('http://45.12.75.118:8000/login', {
        name: this.name
      }).then(response => {
        this.userId = response.data.id;
        this.changeColor();
      })
    },
  }
}
</script>