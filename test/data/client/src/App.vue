<template>
  <div id="app">
    <form class="" method="post" @submit.prevent="sendThis">
 <input type="text" name="" value="" v-model="message">
 <button type="submit" name="button">Submit</button>
 </form>
 {{ message }}
    <!-- <router-view/> -->
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      message: ""
    };
  },
  methods: {
    sendThis() {
      axios
        .post("http://localhost:42356/", this.message)
        .then(response => (this.test = response.data))
        .catch(error => console.log(error));
    }
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.card {
  max-width: 400px;
  margin: 10px auto;
  padding: 10px;
  border: solid 1px green;
}
</style>
