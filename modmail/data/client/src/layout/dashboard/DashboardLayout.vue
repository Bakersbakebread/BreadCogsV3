<template>
  <div class="wrapper">
    <loading
      :active.sync="loading"
      :can-cancel="false"
      :is-full-page="true"
    >
    <img src="@/assets/img/cog.png" class="loader avatar" slot="default">
    </loading>
    <side-bar>
      <template slot="links">
        {{numberOfGuilds}}
        <sidebar-link to="/dashboard" name="Dashboard" icon="ti-panel"/>
        <sidebar-link to="/table-list" name="Threads" icon="ti-view-list-alt"/>
        <sidebar-link to="/members" name="Members" icon="ti-user"/>
        <!-- <sidebar-link to="/typography" name="Typography" icon="ti-text"/> -->
        <sidebar-link to="/bot-settings" name="Redbot Settings" icon="ti-server"/>
        <!-- <sidebar-link to="/maps" name="Map" icon="ti-map"/> -->
        <sidebar-link to="/notifications" name="Notifications" icon="ti-bell"/>
      </template>
    </side-bar>
    <div class="main-panel">
      <top-navbar></top-navbar>

      <dashboard-content @click.native="toggleSidebar"></dashboard-content>
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
    // Import component
    import Loading from 'vue-loading-overlay';
    // Import stylesheet
    import 'vue-loading-overlay/dist/vue-loading.css';

export default {
  components: {
    TopNavbar,
    ContentFooter,
    DashboardContent,
    MobileMenu,
    Loading
  },
  methods: {
    toggleSidebar() {
      if (this.$sidebar.showSidebar) {
        this.$sidebar.displaySidebar(false);
      }
    }
  },
  computed: {
    numberOfGuilds: function() {
      return this.$store.getters.allGuildSettings.length;
    },
    loading() {
      return this.$store.getters.loading;
    }
  }
};
</script>

<style>
.loader {
    position: absolute;
    top: 50%;
    border-radius: 100px;
    left: 50%;
    width: 120px;
    height: 120px;
    margin:-60px 0 0 -60px;
    -webkit-animation:spin 4s linear infinite;
    -moz-animation:spin 4s linear infinite;
    animation:spin 4s linear infinite;
}
@-moz-keyframes spin { 100% { -moz-transform: rotate(360deg); } }
@-webkit-keyframes spin { 100% { -webkit-transform: rotate(360deg); } }
@keyframes spin { 100% { -webkit-transform: rotate(360deg); transform:rotate(360deg); } }
</style>

