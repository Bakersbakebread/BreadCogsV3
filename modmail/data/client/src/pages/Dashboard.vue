<template>
  <div>
    <h3>ModMail threads</h3>
    <div class="row">
      <div class="col-sm-4">
        <stats-card>
          <div class="icon-big text-center icon-success" slot="header">
            <i class="fa fa-envelope-o" aria-hidden="true"></i>
          </div>
          <div class="numbers" slot="content">
            <p>New</p>3
          </div>
        </stats-card>
      </div>
            <div class="col-sm-4">
        <stats-card>
          <div class="icon-big text-center icon-warning" slot="header">
            <i class="fa fa-envelope-o" aria-hidden="true"></i>
          </div>
          <div class="numbers" slot="content">
            <p>Active</p>1
          </div>
        </stats-card>
      </div>
      <div class="col-sm-4">
        <stats-card>
          <div class="icon-big text-center icon-danger" slot="header">
            <i class="fa fa-envelope-o" aria-hidden="true"></i>
          </div>
          <div class="numbers" slot="content">
            <p>Closed</p>30
          </div>
        </stats-card>
      </div>
      </div>
      <div class="row">
      <div class="col">
        <stats-card>
          <div class="icon-big text-center icon-dark" slot="header">
            <i class="fa fa-users" aria-hidden="true"></i>
          </div>
          <div class="numbers" slot="content">
            <p>Visible Member Count</p>
            {{ allMembersShort.length }}
          </div>
        </stats-card>
      </div>
    </div>
    <h3>Guild Settings</h3>
    <div class="row">
      <div class="col-sm-6" v-for="stats in guildSettings" :key="stats.title">
        <card class="card-user mt-5">
          <!-- <div slot="image">
        <img src="@/assets/img/background.jpg" alt="...">
          </div>-->
          <div>
            <div class="author">
              <img class="avatar border-white" :src="stats.guild.icon" alt="...">
              <h4 class="title">
                {{stats.guild.name}}
                <br>

                <a :href="`http://discordapp.com/channels/${stats.guild.id}/`">
                  <span class="guild-link">
                    {{stats.guild.id}}
                    <i class="fa fa-external-link" aria-hidden="true"></i>
                  </span>
                </a>
                <br>
                <small>{{stats.guild.member_count}} members</small>
              </h4>
              <div class="row">
                <div
                  :class="{'col-sm-6 col-12' : stats.alerts_active, 'col-12' : !stats.alerts_active }"
                >
                  <p class="mt-3">Modmail alerts</p>
                  <i
                    v-if="stats.alerts_active"
                    class="alerts fa fa-check text-success"
                    aria-hidden="true"
                  ></i>
                  <i v-else class="alerts fa fa-times text-danger" aria-hidden="true"></i>
                </div>
                <div v-if="stats.alerts_active" class="col-sm-6 col-12">
                  <p class="mt-3">Modmail alerts channel</p>
                  <p class="alerts-channel">
                    {{stats.alerts_channel.name}}<br>
                   <small> {{stats.alerts_channel.id}}</small>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </card>
        <!-- <stats-card>
          <div class="icon-big text-center" :class="`icon-${stats.type}`" slot="header">
            <i :class="stats.icon"></i> 
            <img
              :src="stats.guild.icon"
              class="img-fluid"
            > 
          </div>
          <div class="numbers" slot="content">
            <p>{{ stats.guild.name }}</p>
            <hr>
          </div>
          <div class="numbers" slot="content">
            <p>Alerts enabled</p>
            {{ stats.alerts_active | capitalize }}
          </div>
          <div class="numbers" slot="content">
            <p>Alert Channel</p>
            {{stats.alerts_channel.name}}<br>
            <a :href="`https://discordapp.com/channels/${stats.guild.id}/${stats.alerts_channel.id}`">{{stats.alerts_channel.id}}<br></a>
          </div>
        </stats-card>-->
      </div>
    </div>
  </div>
</template>
<script>
import { StatsCard, ChartCard } from "@/components/index";
import Chartist from "chartist";

export default {
  components: {
    StatsCard,
    ChartCard
  },
  mounted() {
    //console.log(this.$store)
    this.$store.dispatch("loadAllGuildSettings");
    this.$store.dispatch("loadAllMembersShort"); 
    this.$store.dispatch("setLoading", true); 
  },
  computed: {
    guildSettings: function() {
      return this.$store.getters.allGuildSettings;
    },
    allMembersShort: function() {
      return this.$store.getters.allMembersShort;
    }
  },
  filters: {
    capitalize: function(value) {
      if (!value) return "";
      value = value.toString();
      return value.charAt(0).toUpperCase() + value.slice(1);
    }
  }
};
</script>
<style scoped>
.guild-link {
  font-size: 1rem;
}
.alerts {
  font-size: 2rem !important;
}
.alerts-channel {
  font-weight: 200;
  margin: 0;
  padding: 0;
}
</style>
