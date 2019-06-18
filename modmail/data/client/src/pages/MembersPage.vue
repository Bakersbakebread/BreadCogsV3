<template>
  <div>
    <loading :active.sync="isFiltering" :can-cancel="false" :is-full-page="false"/>
    <label for="searchBar">Search members</label>
    <input id="searchBar" class="form-control" v-model="searchQuery">

    <div class="d-flex justify-content-end mb-2 pt-2">
      <div
        class="float-left pt-2 mr-4"
        v-if="isSearching"
      >{{filteredResources.length}} found members</div>
      <div class="float-left pt-2 mr-4" v-else>{{allMembersShort.length}} total members</div>
      <div class="btn btn-primary btn-wd mr-2" @click="nextPage">Next page</div>
      <div class="btn btn-primary btn-wd" @click="prevPage">Previous page</div>
    </div>

      <template v-if="isSearching">
        <div class="row">
        <div v-for="(x, index) in filteredResources" :key="index" class="col-12 col-sm-6">
          <member-card :x="x"/>
        </div>
        <card
        class="mx-auto w-100 text-center" 
        v-if="filteredResources.length == 0">
        <img src="@/assets/img/emoji_sad.png"/>
        <h3>No members found</h3>
        </card>
        </div>
      </template>
      
      <template v-else>
      <div class="row" v-for="(page, index) in paginatedData" :key="index">
        <div v-for="x in page" :key="x.member.id" class="col-12 col-sm-6">
          <member-card :x="x"/>
        </div>
      </div>
      </template>
  </div>
</template>

<script>
import _ from "lodash";
import MemberCard from "@/components/Cards/MemberCard";
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";

export default {
  name: "MembersPage",
  components: {
    MemberCard,
    Loading
  },
  data() {
    return {
      loading: false,
      pageNumber: 0,
      pageSize: 20,
      isFiltering: false,
      searchQuery: "",
      filteredResources: null
    };
  },
  mounted() {
    this.$store.dispatch("loadAllMembersShort");
    this.updateQuery();
  },
  methods: {
    beforeEnter: function (el) {
      el.style.opacity = 0
      el.style.height = 0
    },
    enter: function (el, done) {
      var delay = el.dataset.index * 150
      setTimeout(function () {
        Velocity(
          el,
          { opacity: 1, height: '1.6em' },
          { complete: done }
        )
      }, delay)
    },
    leave: function (el, done) {
      var delay = el.dataset.index * 150
      setTimeout(function () {
        Velocity(
          el,
          { opacity: 0, height: 0 },
          { complete: done }
        )
      }, delay)
    },
    nextPage() {
      this.pageNumber++;
    },
    updateQuery() {
      if (this.$route.params.search) {
        this.searchQuery = this.$route.params.search;
      }
    },
    prevPage() {
      this.pageNumber--;
    },
    getRGBValues(str) {
      var vals = str
        .substring(str.indexOf("(") + 1, str.length - 1)
        .split(", ");
      return `${vals[0]}, ${vals[1]}, ${vals[2]}`;
    },
    updateSearch() {
      this.isFiltering = true;
      this.filteredResources = this.allMembersShort.filter(
        x =>
          x.member.name
            .toUpperCase()
            .startsWith(this.searchQuery.toUpperCase()) ||
          x.member.id.toString().startsWith(this.searchQuery)
      );
      this.isFiltering = false;
    }
  },
  watch: {
    searchQuery() {
      this.updateSearch();
    }
  },
  computed: {
    isSearching() {
      if (this.searchQuery.length >= 1) {
        return true;
      } else {
        return false;
      }
    },
    allMembersShort: function() {
      return this.$store.getters.allMembersShort;
    },
    pageCount() {
      let l = this.allMembersShort.length,
        s = this.pageSize;
      return Math.ceil(l / s);
    },
    paginatedData() {
      const start = this.pageNumber * this.pageSize,
        end = start + this.pageSize;
      return _.chunk(this.allMembersShort.slice(start, end), 2);
    }
  }
};
</script>

<style>
.role-color {
  display: inline-block;
  width: 10px;
  height: 10px;
  margin-right: 5px;
  border: solid 1px black;
}
</style>
