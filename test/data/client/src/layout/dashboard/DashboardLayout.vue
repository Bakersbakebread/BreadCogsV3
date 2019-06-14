<template>
  <div class="wrapper">
    <side-bar>
      <template slot="links">
        {{numberOfGuilds}}
        <sidebar-link to="/dashboard" name="Dashboard" icon="ti-panel"/>
        <!-- <sidebar-link to="/stats" name="User Profile" icon="ti-user"/> -->
        <sidebar-link to="/table-list" name="Threads" icon="ti-view-list-alt"/>
        <!-- <sidebar-link to="/typography" name="Typography" icon="ti-text"/> -->
        <!-- <sidebar-link to="/icons" name="Icons" icon="ti-pencil-alt2"/> -->
        <!-- <sidebar-link to="/maps" name="Map" icon="ti-map"/> -->
        <sidebar-link to="/notifications" name="Notifications" icon="ti-bell"/>
      </template>
    </side-bar>
    <div class="main-panel">
      <top-navbar></top-navbar>

      <dashboard-content @click.native="toggleSidebar">

      </dashboard-content>
    </div>
  </div>
</template>
<style lang="scss">

</style>
<script>
import TopNavbar from "./TopNavbar.vue";
import ContentFooter from "./ContentFooter.vue";
import DashboardContent from "./Content.vue";
import MobileMenu from "./MobileMenu";
export default {
  components: {
    TopNavbar,
    ContentFooter,
    DashboardContent,
    MobileMenu
  },
  methods: {
    toggleSidebar() {
      if (this.$sidebar.showSidebar) {
        this.$sidebar.displaySidebar(false);
      }
    }
  },
    computed:{
    numberOfGuilds: function(){
      return this.$store.getters.allGuildSettings.length;
    }
  }
};
</script>
