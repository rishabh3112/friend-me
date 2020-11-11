<template>
  <div v-if="room === undefined" class="home-page">
    <div class="user-details row">
      <h3 class="col s12 center-align heading">Friend Me</h3>
      <p class="col s12 center-align grey-text text-darken-2">
        Chat with people you can connect with
      </p>
      <div class="input-field col s6">
        <input v-model="name" id="name" type="text" class="validate" />
        <label for="name">Name</label>
      </div>
      <div class="input-field col s6">
        <input v-model="age" id="age" type="number" class="validate" />
        <label for="age">Age</label>
      </div>
      <div class="input-field col s12">
        <span class="grey-text">Movie</span>
        <select v-model="movie" class="browser-default">
          <option>action and adventure</option>
          <option>comedy and drama</option>
          <option>horror</option>
          <option>mystery and thriller</option>
        </select>
      </div>
      <label class="col s6">
        <input v-model="sports" type="checkbox" />
        <span>Sports</span>
      </label>
      <label class="col s6">
        <input v-model="travel" type="checkbox" />
        <span>Travel</span>
      </label>
      <div class="col s12 btn" @click="submit()">Submit</div>
    </div>
  </div>
  <div class="chat-window" v-else-if="this.socket !== undefined">
    <div class="message">
      <ul id="example-1">
        <li v-for="item in messages" :key="item.message">
          {{item.user}}:{{ item.message }}
        </li>
      </ul>
    </div>
    <div class="chat white row valign-wrapper">
      <div class="input-field col s10">
        <input v-model="message" id="age" class="validate" />
      </div>
      <div class="col s2 btn" @click="send()">send</div>
    </div>
  </div>
  <div class="chat-window" v-else>

  </div>
</template>

<script>
export default {
  name: "App",
  data: () => {
    return {
      name: "",
      age: 20,
      movie: "",
      sports: false,
      travel: false,
      room: undefined,
      socket: undefined,
      message: "",
      messages: []
    };
  },
  methods: {
    async submit() {
      const response = await fetch('http://127.0.0.1:5000/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({
          name: this.name,
          age: parseInt(this.age),
          movie: this.movie,
          sports: this.sports,
          travel: this.travel
        })
      });
      const result = await response.json();
      this.room = result.room;
      this.socket = io('http://127.0.0.1:5000/');
      this.socket.on('connect', () => {
        this.socket.emit('join', {name: this.name, room: this.room});
        console.log("APPLE");
      })
      this.socket.on('message', data => {
        if (!data.user) {
          this.messages.push({user: "admin", message: data});
          return;
        }
        this.messages.push(data)
      })
    },
    async send() {
      this.socket.send(
        {
          message: {
            user: this.name,
            message: this.message
          },
          room: this.room
        }
      );
      this.message = "";
    }
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Pacifico&family=Permanent+Marker&display=swap");
.home-page {
  display: flex;
  height: 100%;
  align-items: center;
  align-content: center;
  justify-content: center;
  background: url("./assets/spikes.png");
}

.user-details {
  width: 50%;
  max-width: 500px;
  background: #fff;
  padding: 20px;
  box-shadow: 0px 0px 10px #eee;
}

.chat {
  height: 80px;
  width: 100%;
  box-shadow: 0px 0px 10px #eee;
  padding-left: 10px;
  padding-right: 10px;
}

.message {
  height: calc(100% - 80px);
}

.heading {
  font-family: "Permanent Marker", cursive;
}

.chat-window {
  overflow: hidden;
  background: url("./assets/spikes.png");
  height: 100%;
}

label.col {
  margin-top: 10px;
  margin-bottom: 20px;
}
</style>
