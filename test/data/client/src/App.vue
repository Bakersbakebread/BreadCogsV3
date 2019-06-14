<template>
  <div id="app">
    <navBar/>
    <!-- {{ message }} -->
    <div class="container">
    <router-view class="mt-2"/>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import NavBar from "@/components/layout/NavBar"

export default {
  name: "App",
  data() {
    return {
      message: ""
    };
  },
  components:{
    NavBar
  },
  methods: {
    sendThis() {}
  },
  mounted() {
    axios
      .post("http://localhost:42356/")
      .then(response => (this.message = JSON.parse(response.data)))
      .catch(error => console.log(error));
  },
  computed: {
    byUser() {
      return this.message.reduce((acc, message) => {
        (acc[message.author.name] = acc[message.author.name] || []).push(
          message.content
        );
        return acc;
      }, {});
    }
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin: 0 auto;
}
</style>
