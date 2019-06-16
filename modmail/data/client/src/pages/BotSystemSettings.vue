<template>
  <div>
    <div class="row">
      <div class="col">
        <card title="CPU Usage">
          <circle-progress :percent="settings.cpu"/>
        </card>
      </div>
      <div class="col">
        <card title="RAM Usage" class="col">
          <circle-progress :percent="settings.ram"/>
        </card>
      </div>
    </div>
    <div class="row">
      <div class="col-6">
        <stats-card>
          <div class="icon-big text-center icon-info" slot="header">
            <i class="ti-view-list-alt"></i>
          </div>
          <div class="numbers" slot="content">
            <p>Guilds</p>
            {{settings.guilds}}
          </div>
          <div class="stats" slot="footer">
            <i class="ti-reload"></i> Updated Now
          </div>
        </stats-card>
      </div>
      <div class="col-6">
        <stats-card>
          <div class="icon-big text-center icon-success" slot="header">
            <i class="ti-timer"></i>
          </div>
          <div class="numbers" slot="content">
            <p>Uptime</p>
            {{settings.uptime}}
          </div>
          <div class="stats" slot="footer">
            <i class="ti-reload"></i> Updated Now
          </div>
        </stats-card>
      </div>
    </div>
    <div class="row">
      <div class="col-6">
        <stats-card>
          <div class="icon-big text-center icon-danger" slot="header">
            <i class="ti-pin-alt"></i>
          </div>
          <div class="numbers" slot="content">
            <p>Red Version</p>
            {{settings.red_version}}
          </div>
          <div class="stats" slot="footer">
            <i class="ti-reload"></i> Updated Now
          </div>
        </stats-card>
      </div>
      <div class="col-6">
        <stats-card>
          <div class="icon-big text-center icon-warning" slot="header">
            <i class="ti-pin-alt"></i>
          </div>
          <div class="numbers" slot="content">
            <p>Discord.py Version</p>
            {{settings.dpy_version}}
          </div>
          <div class="stats" slot="footer">
            <i class="ti-reload"></i> Updated Now
          </div>
        </stats-card>
      </div>
    </div>
  </div>
</template>
<script>
import { StatsCard } from "@/components/index";
import CircleProgress from "@/components/CircleProgress";
export default {
  name: "BotSystemSettings",
  components: {
    CircleProgress,
    StatsCard
  },
  mounted() {
    //console.log(this.$store)
    this.$store.dispatch("loadBotSysSettings");
  },
  computed: {
    settings: function() {
      return this.$store.getters.botSysSettings;
    }
  }
};
</script>