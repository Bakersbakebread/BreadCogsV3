<template>
  <div id="app">
    <div class="card" v-for="(x, index) in test.status" :key="index">
      <strong><marquee>{{ x.author }}</marquee></strong> <br> {{ x.content }}
      </div>
    <!-- <router-view/> -->
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "App",
  data() {
    return {
      test: "testste"
    };
  },
  mounted(){
    axios
    .get('http://localhost:42356/')
    .then(response => (this.test = response.data))
    .catch(error => console.log(error))
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
.card{
  max-width: 400px;
  margin: 10px auto;
  padding: 10px;
  border: solid 1px green;

}
</style>
