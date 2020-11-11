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
      <div v-for="item in messages" :key="item.message" class="row">
        <div v-if="item.user === name" class="me bubble right-align col s5 m5 l5">
          <b>{{item.user}}</b>
          <br/>
          {{item.message}}
        </div>
        <div v-else-if="item.user === 'admin'" class="center-align">
          <b>{{item.message}}</b>
        </div>
        <div v-else class="them bubble left-align col s5 m5 l5">
          <b>{{item.user}}</b>
          <br/>
          {{item.message}}
        </div>
        
      </div>
    </div>
    <div class="chat white row valign-wrapper">
      <div class="input-field col s11">
        <input v-model="message" id="age" class="validate" />
      </div>
      <div class="col s1">
        <div class="btn-floating" @click="send()">
          <i class="material-icons">send</i>
        </div>
      </div>
    </div>
  </div>
  <div class="chat-window" v-else>
    <div class="progress">
        <div class="indeterminate"></div>
    </div>
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
      const response = await fetch('http://192.168.0.107:5000/', {
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
      this.socket = io('http://192.168.0.107:5000/');
      this.socket.on('connect', () => {
        this.socket.emit('join', {name: this.name, room: this.room});
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
      if (this.message === "") {
        return;
      }
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
  min-width: 300px;
  background: #fff;
  padding: 20px;
  box-shadow: 0px 0px 10px #eee;
}

.chat {
  height: 80px;
  width: 100%;
  box-shadow: 0px 0px 10px #eee;
  padding-left: 40px;
  padding-right: 40px;
}

.message {
  height: calc(100% - 80px);
  padding: 20px;
  overflow: auto;
  width: 100%;
  margin: 0 auto;
}

.heading {
  font-family: "Permanent Marker", cursive;
}

b {
  font-family: "Permanent Marker", cursive;
}

.chat-window {
  overflow: hidden;
  background: url("./assets/spikes.png");
  height: 100%;
}

.bubble {
  background: #99f;
  padding: 10px;
  box-shadow: 0px 0px 10px #eee;
  max-width: 400px;
  word-wrap: break-word;
  border-radius: 5px;
  position: relative;
}

.me {
  width: 100%;
  background: #9f9;
  float: right;
}

label.col {
  margin-top: 10px;
  margin-bottom: 20px;
}

.me:before {
  content: "";
  width: 0px;
  height: 0px;
  position: absolute;
  border-left: 10px solid #9f9;
  border-right: 10px solid transparent;
  border-top: 10px solid #9f9;
  border-bottom: 10px solid transparent;
  right: -19px;
  top: 6px;
}

.them:before {
  content: "";
  width: 0px;
  height: 0px;
  position: absolute;
  border-left: 10px solid transparent;
  border-right: 10px solid #99f;
  border-top: 10px solid #99f;
  border-bottom: 10px solid transparent;
  left: -19px;
  top: 6px;
}

</style>
