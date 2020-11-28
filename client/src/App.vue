<template>
  <transition name="fade">
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
            <option value="0">action and adventure</option>
            <option value="1">comedy and drama</option>
            <option value="2">horror</option>
            <option value="3">mystery and thriller</option>
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
      <div class="chat-header row valign-wrapper">
        <div class="col s11 valign-wrapper">
          <img class="icon" src='./assets/favicon.ico' />
          <span> Room {{room}} </span>
        </div>
        <div class="col s1">
          <div class="btn-floating red" @click="exit()">
            <i class="material-icons">clear</i>
          </div>
        </div>
      </div>
      <div class="message">
        <transition-group name="list" tag="p">
        <div v-for="item in messages" :key="item.message" class="row">
          <div
            v-if="item.id === this.id"
            class="me bubble right-align col s5 m5 l5"
          >
            <b>{{ item.user }}</b>
            <br />
            {{ item.message }}
            <br />
            <small v-if="item.profane">Original message contained explicit words. <b>{{item.user}}</b> will be removed if used explicit words in {{profaneAllowed}} more messages</small>
          </div>
          <div v-else-if="item.id === undefined" class="center-align">
            <b class="admin-msg">{{ item.message }}</b>
          </div>
          <div v-else class="them bubble left-align col s5 m5 l5">
            <b>{{ item.user }}</b>
            <br />
            {{ item.message }}
          </div>
        </div>
        </transition-group>
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
  </transition>
</template>

<script>
import Filter from 'bad-words'
const filter = new Filter();
export default {
  name: "App",
  data: () => {
    return {
      name: "",
      profaneAllowed: 3,
      age: undefined,
      movie: undefined,
      sports: false,
      travel: false,
      room: undefined,
      socket: undefined,
      id: undefined,
      message: "",
      messages: [],
    };
  },
  methods: {
    async submit() {
      const response = await fetch("http://0.0.0.0:5000/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json;charset=utf-8",
        },
        body: JSON.stringify({
          name: this.name,
          age: parseInt(this.age),
          movie: parseInt(this.movie),
          sports: this.sports,
          travel: this.travel,
        }),
      });

      const result = await response.json();
      this.room = result.room;
      this.id = result.id;
      this.socket = io("http://0.0.0.0:5000/");
      this.socket.on("connect", () => {
        this.socket.emit("join", { name: this.name, room: this.room });
      });
      this.socket.on("message", (data) => {
        if (!data.user) {
          this.messages.push({ user: "admin", message: filter.clean(data) });
          return;
        }
        data.profane = false;
        if (filter.isProfane(data.message)) {
          if (this.profaneAllowed == 0) {
            this.exit();
            return;
          }
          data.message = filter.clean(data.message);
          data.profane = true;
          this.profaneAllowed--;
        }
        this.messages.push(data);
      });
    },

    async send() {
      if (this.message === "") {
        return;
      }

      this.socket.send({
        message: {
          user: this.name,
          id: this.id,
          message: this.message,
        },
        room: this.room,
      });

      this.message = "";
    },

    async exit() {
      this.socket.emit("leave", { name: this.name, room: this.room });
      this.socket.close();
      this.profaneAllowed = 3;
      this.room = undefined;
      this.socket = undefined;
      this.name = "";
      this.age = undefined;
      this.sports = false;
      this.travel = false;
      this.movie = undefined;
      this.messages = []
    },

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
}

.icon {
  width: 40px;
  border-radius: 20px;
  margin:0px 10px;
}
.admin-msg {
  background: #fff;
  padding: 3px 10px;
  border-radius: 5px;
  box-shadow: 0px 0px 10px #555;
}

.user-details {
  width: 50%;
  max-width: 500px;
  min-width: 300px;
  background: #fff;
  padding: 20px;
  box-shadow: 0px 0px 10px #555;
}

.chat {
  height: 50px;
  width: 100%;
  box-shadow: 0px 0px 10px #555;
  padding: 0px;
  padding-left: 10px;
  padding-right: 10px;
}

.chat-header {
  height: 50px;
  width: 100%;
  box-shadow: 0px 0px 10px #555;
  background: #fff;
  margin-bottom: 0px;
  font-family: "Permanent Marker", cursive;
  font-size: 25px;
  padding: 0px 10px;
}

.message {
  height: calc(100% - 100px);
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
  height: 100%;
}

.bubble {
  background: #99f;
  padding: 10px;
  max-width: 400px;
  word-wrap: break-word;
  border-radius: 5px;
  position: relative;
  box-shadow: 0px 0px 10px #555;
}

.me {
  width: 100%;
  background: #cfc;
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
  border-left: 10px solid #cfc;
  border-right: 10px solid transparent;
  border-top: 10px solid #cfc;
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

.fade-enter-active, .fade-leave-active {
  transition: all .5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
  transform: scale(0);
}

.list-enter-active,
.list-leave-active {
  transition: all 0.25s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
</style>
