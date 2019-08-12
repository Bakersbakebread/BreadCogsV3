<template>
  <div :class="{'nav-open': $sidebar.showSidebar}">
    <notifications></notifications>
    <router-view></router-view>
  </div>

</template>

<script>
import NotificationTemplate from '@/pages/Notifications/NotificationTemplate';
export default {
  components:{
    NotificationTemplate
  },
    mounted() {
      this.notifyVue('top', 'right');
      this.$store.dispatch('getUserDetails')
    },
    methods:{
    notifyVue(verticalAlign, horizontalAlign) {
      const color = Math.floor(Math.random() * 4 + 1);
      this.$notify({
        component: NotificationTemplate,
        icon: "ti-support",
        horizontalAlign: horizontalAlign,
        verticalAlign: verticalAlign,
        type: "warning"
      });
    }
  }
};
</script>

<style lang="scss">
.loader{
  opacity: 0.7;
}
.vue-notifyjs.notifications {
  .alert {
    z-index: 10000;
  }
  .list-move {
    transition: transform 0.3s, opacity 0.4s;
  }
  .list-item {
    display: inline-block;
    margin-right: 10px;
  }
  .list-enter-active {
    transition: transform 0.2s ease-in, opacity 0.4s ease-in;
  }
  .list-leave-active {
    transition: transform 1s ease-out, opacity 0.4s ease-out;
  }

  .list-enter {
    opacity: 0;
    transform: scale(1.1);
  }
  .list-leave-to {
    opacity: 0;
    transform: scale(1.2, 0.7);
  }
}
</style>
