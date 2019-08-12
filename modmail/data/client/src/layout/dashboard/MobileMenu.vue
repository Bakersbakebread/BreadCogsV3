<template>
  <ul class="nav navbar-nav nav-mobile-menu">
    <slot></slot>
  </ul>
</template>
<script>
export default {};
</script>
<style scoped>
.nav-mobile-menu{
  position:fixed;
  bottom:50px;
  left:50px;
}
</style>
