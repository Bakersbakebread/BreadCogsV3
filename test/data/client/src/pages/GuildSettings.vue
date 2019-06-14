<template>
<div>
  <div
    class="card mt-2"
    v-for="(x, index) in allGuildSettings"
    :class="isTrue(x.alerts_active)"
    :key="index"
  >
    <div class="row no-gutters">
      <div class="col-auto">
        <img :src="x.guild.icon" style="width:100px;" alt>
      </div>
      <div class="col">
        <div class="card-block px-2">
          <h4 class="card-title mt-3">{{x.guild.name}}</h4>
          <div class="row">
          <div class="col text-center">
             <h6>ModMail alerts active</h6>
             <!-- <span>{{x.alerts_active}} ✔️</span> -->
             <span>✔️</span>
          </div>
          <div class="col text-center">
         <strong>ModMail channel</strong>
         <br>
             <!-- <span>{{x.alerts_active}} ✔️</span> -->
             <span>{{x.alerts_channel.name}}</span><br>
             <span>{{x.alerts_channel.id}}</span>
          </div>
          <div class="col text-center">
             <h6>ModMail alerts active</h6>
             <!-- <span>{{x.alerts_active}} ✔️</span> -->
             <span>✔️</span>
          </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "GuildSettings",
  data() {
    return {
      allGuildSettings: ""
    };
  },
  mounted() {
    axios
      .post("http://localhost:42356/")
      .then(response => (this.allGuildSettings = JSON.parse(response.data)))
      .catch(error => console.log(error));
  },
  methods: {
    isTrue(alerts_active) {
      if (alerts_active == true) {
        return "true-class";
      }
    }
  }
};
</script>

<style>
.true-class {
  /* border-left: solid 3px green; */
}
</style>

