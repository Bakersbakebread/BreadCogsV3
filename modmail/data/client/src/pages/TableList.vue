<template>
  <div class="row">
    <div class="col mb-2">
      <drop-down
        tag="div"
        :title="filteredThreads"
        class="btn float-sm-right mr-2 mr-sm-5"
        :class="filteredThreadsBtn"
      >
        <a
          @click="filteredThreads = 'all', filteredThreadsBtn = 'btn-primary'"
          class="dropdown-item"
        >All</a>
        <a
          @click="filteredThreads = 'new', filteredThreadsBtn = 'btn-success'"
          class="dropdown-item"
        >New</a>
        <a
          @click="filteredThreads = 'active', filteredThreadsBtn = 'btn-warning'"
          class="dropdown-item"
        >Active</a>
        <a
          @click="filteredThreads = 'closed', filteredThreadsBtn = 'btn-danger'"
          class="dropdown-item"
        >Closed</a>
      </drop-down>

      <drop-down 
      tag="div" 
      :title="assignedThreads" class="btn btn-light-blue float-sm-right mr-2">
        <a
          @click="assignedThreads = 'all'"
          class="dropdown-item"
        >All Threads</a>
        <a
          @click="assignedThreads = 'me'"
          class="dropdown-item"
        >Assigned to me</a>
      </drop-down>
    </div>
    <div v-if="filteredThreads == 'all'" class="col-12">
      <div v-for="(test, guild) in allThreads" :key="guild">
        <card :title="getGuildName(guild).guild.name" :subTitle="getGuildName(guild).guild.id">
          <div slot="raw-content" class="none-found h6" v-if="getTableData(allThreads[guild].threads).length == 0">
            No threads
          </div>
          <div v-else slot="raw-content" class="table-responsive">
            <paper-table
              :data="getTableData(allThreads[guild].threads)"
              :columns="tableColumns"
            ></paper-table>
          </div>
        </card>
      </div>
    </div>
    <div v-if="filteredThreads == 'closed'" class="col-12">
      <div v-for="(test, guild) in onlyClosedThreads" :key="guild">
        <card :title="getGuildName(guild).guild.name" :subTitle="getGuildName(guild).guild.id">
          <div slot="raw-content" class="none-found h6" v-if="getTableData(onlyClosedThreads[guild].threads).length == 0">
            No closed threads
          </div>
          <div v-else slot="raw-content" class="table-responsive">
            <paper-table
              :data="getTableData(onlyClosedThreads[guild].threads)"
              :columns="tableColumns"
            ></paper-table>
          </div>
        </card>
      </div>
    </div>
    <div v-if="filteredThreads == 'new'" class="col-12">
      <div v-for="(test, guild) in onlyNewThreads" :key="guild">
        <card :title="getGuildName(guild).guild.name" :subTitle="getGuildName(guild).guild.id">
          <div slot="raw-content" class="none-found h6" v-if="getTableData(onlyNewThreads[guild].threads).length == 0">
            No new threads
          </div>
          <div v-else slot="raw-content" class="table-responsive">
            <paper-table
              :data="getTableData(onlyNewThreads[guild].threads)"
              :columns="tableColumns"
            ></paper-table>
          </div>
        </card>
      </div>
    </div>
        <div v-if="filteredThreads == 'active'" class="col-12">
      <div v-for="(test, guild) in onlyActiveThreads" :key="guild">
        <card :title="getGuildName(guild).guild.name" :subTitle="getGuildName(guild).guild.id">
          <div slot="raw-content" class="none-found h6" v-if="getTableData(onlyActiveThreads[guild].threads).length == 0">
            No active threads
          </div>
          <div v-else slot="raw-content" class="table-responsive">
            <paper-table
              :data="getTableData(onlyActiveThreads[guild].threads)"
              :columns="tableColumns"
            ></paper-table>
          </div>
        </card>
      </div>
    </div>


  </div>
</template>
<script>
import { PaperTable } from "@/components";

export default {
  components: {
    PaperTable
  },
  data() {
    return {
      tableColumns: ["User", "Message", "Created", "Status"],
      filteredThreads: "new",
      filteredThreadsBtn: "btn-success",
      assignedThreads: "all"
    };
  },
  methods: {
    getTableData(data) {
      var x = [];
      for (const key in data) {
        x.push({
          user: {
            name:
              data[key].thread.author.name +
                "#" +
                data[key].thread.author.discriminator || "Undefined",
            id: data[key].thread.author.id
          },
          message: data[key].thread.content || "Undefined",
          created: data[key].thread.created_at || "Undefined",
          status: data[key].status || "Undefined"
        });
      }
      return x;
      // return x
    },
    getGuildName(guild) {
      // return 'test'
      return this.$store.getters.getGuildById(guild);
    }
  },
  mounted() {
    this.$store.dispatch("loadAllModMailThreads");
    this.$store.dispatch("loadAllGuildSettings");
  },
  computed: {
    allThreads() {
      return this.$store.getters.allThreads;
    },
    onlyClosedThreads() {
      return this.$store.getters.onlyClosedThreads;
    },
    onlyNewThreads() {
      return this.$store.getters.onlyNewThreads;
    },
    onlyActiveThreads() {
      return this.$store.getters.onlyActiveThreads;
    },

  }
};
</script>
<style>
.none-found{
  padding:20px;
  text-align: center;
}
</style>
