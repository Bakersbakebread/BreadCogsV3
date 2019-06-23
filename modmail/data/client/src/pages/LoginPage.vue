<template>
<div class="container">
  test
  <a
  href="http://localhost:42356/api/discord/login"
  class="btn btn-block">Login</a>
  </div>
</template>

<script>
export default {
name: 'Login',
mounted() {
this.$store.dispatch('authUser')
}
}
</script>

<style scoped>
</style>
