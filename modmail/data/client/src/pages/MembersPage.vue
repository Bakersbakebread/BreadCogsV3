<template>
  <div>
    found {{allMembersShort.length}}
    <div v-if="loading">Loading...</div>
    <input v-model="searchQuery">
    <div class="btn btn-primary" @click="nextPage">Next</div>
    <div class="btn btn-primary" @click="prevPage">Previous</div>

    <div v-if="isSearching" class="row">
      <div v-for="(x, index) in filteredResources" :key="index" class="col-12 col-sm-6">
            <member-card :x="x"/>
      </div>
    </div>

    <div v-else class="row" v-for="(page, index) in paginatedData" :key="index">
          <div v-for="x in page" :key="x.member.id" class="col-12 col-sm-6">
      <member-card :x="x"/>
      </div>
    </div>
  </div>
</template>

<script>
import _ from "lodash";
import MemberCard from '@/components/Cards/MemberCard'

export default {
  name: "MembersPage",
  components:{
    MemberCard
  },
  data() {
    return {
      loading: true,
      pageNumber: 0,
      pageSize: 20,
      searchQuery: '',
      filteredResources: null
    };
  },
  mounted() {
    this.$store.dispatch("loadAllMembersShort");
    this.updateQuery()
  },
  methods: {
    nextPage() {
      this.pageNumber++;
    },
    updateQuery(){
      if (this.$route.params.search) {
        this.searchQuery = this.$route.params.search
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
    }
  },
  watch: {
    searchQuery() {
      this.filteredResources = this.allMembersShort.filter(
        x =>
          x.member.name
            .toUpperCase()
            .startsWith(this.searchQuery.toUpperCase()) ||
          x.member.id.toString().startsWith(this.searchQuery)
      );
    },
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
.role-color{
  display: inline-block;
  width: 10px;
  height: 10px;
  margin-right: 5px;
  border: solid 1px black;
}
</style>
