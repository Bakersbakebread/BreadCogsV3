<template>
<div>
<div class="body"></div>
<div class="outer">
  <div class="middle">
    <div class="inner card card-body bg-nude">
                <img class="logo-img mx-auto" src="@/assets/img/logo.png" alt="">

    <h4>Please login to continue.</h4>
      <router-link to="/api/discord/login" class="btn btn-success">Login</router-link>
    </div>
  </div>
</div>
</div>
</template>

<script>
export default {
  name: "Login",
  mounted() {
    this.$store.dispatch("authUser");
  }
};
</script>

<style>
.logo-img{
  height: 100px;
  width:100px;
}
.body {
  background-image: url("https://camo.githubusercontent.com/12adf4288357d03a1a0379e343dbbf0d842c71ef/68747470733a2f2f696d6775722e636f6d2f705931575546582e706e67");
  background-position: center center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: cover;
  background-color: #464646;
      filter: blur(2px);
  -webkit-filter: blur(2px);
  height: 100vh;

}
.outer {
  text-align: center;
  display: table;
  position: absolute;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100%;
  
}
.middle {
  display: table-cell;
  vertical-align: middle;
  
}

.inner {
  margin-left: auto;
  /* padding:20px; */
  margin-right: auto;
  width: 400px;
  z-index: 1;
  /*whatever width you want*/
  
}
</style>
