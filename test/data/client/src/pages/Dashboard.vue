<template>
  <div>
    <h3>Guild Settings</h3>
    <div class="row">
      <div class="col-md-6 col-xl-3" v-for="stats in guildSettings" :key="stats.title">
        <stats-card>
          <div class="icon-big text-center" :class="`icon-${stats.type}`" slot="header">
            <!-- <i :class="stats.icon"></i> -->
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
          <!-- <div class="stats" slot="footer">
            <i :class="stats.footerIcon"></i>
             {{stats.footerText}}
          </div>-->
        </stats-card>
      </div>
    </div>

    <!--Charts-->
    <!-- <div class="row">

      <div class="col-12">
        <chart-card title="Users behavior"
                    sub-title="24 Hours performance"
                    :chart-data="usersChart.data"
                    :chart-options="usersChart.options">
          <span slot="footer">
            <i class="ti-reload"></i> Updated 3 minutes ago
          </span>
          <div slot="legend">
            <i class="fa fa-circle text-info"></i> Open
            <i class="fa fa-circle text-danger"></i> Click
            <i class="fa fa-circle text-warning"></i> Click Second Time
          </div>
        </chart-card>
      </div>

      <div class="col-md-6 col-12">
        <chart-card title="Email Statistics"
                    sub-title="Last campaign performance"
                    :chart-data="preferencesChart.data"
                    chart-type="Pie">
          <span slot="footer">
            <i class="ti-timer"></i> Campaign set 2 days ago</span>
          <div slot="legend">
            <i class="fa fa-circle text-info"></i> Open
            <i class="fa fa-circle text-danger"></i> Bounce
            <i class="fa fa-circle text-warning"></i> Unsubscribe
          </div>
        </chart-card>
      </div>

      <div class="col-md-6 col-12">
        <chart-card title="2015 Sales"
                    sub-title="All products including Taxes"
                    :chart-data="activityChart.data"
                    :chart-options="activityChart.options">
          <span slot="footer">
            <i class="ti-check"></i> Data information certified
          </span>
          <div slot="legend">
            <i class="fa fa-circle text-info"></i> Tesla Model S
            <i class="fa fa-circle text-warning"></i> BMW 5 Series
          </div>
        </chart-card>
      </div>

    </div>-->
  </div>
</template>
<script>
import { StatsCard, ChartCard } from "@/components/index";
import Chartist from 'chartist';


export default {
  components: {
    StatsCard,
    ChartCard,
  },
  mounted() {
    //console.log(this.$store)
    this.$store.dispatch('loadAllGuildSettings'); // dispatch loading


  },
  computed:{
    guildSettings: function(){
      return this.$store.getters.allGuildSettings
    }
  },
filters: {
  capitalize: function (value) {
    if (!value) return ''
    value = value.toString()
    return value.charAt(0).toUpperCase() + value.slice(1)
  }
}
  };
</script>
<style>
</style>
