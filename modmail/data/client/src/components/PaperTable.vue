<template>
<div>
  <div class="text-center">
    <span class="btn btn-neutral btn-block p-2" @click="active = !active">
      <span v-if="!active"><i class="fa fa-caret-down" aria-hidden="true"></i>Expand</span>
      <span v-if="active"><i class="fa fa-caret-up" aria-hidden="true"></i>Close</span>
    </span>
</div>
  <table class="table active-tag" :class="tableClass">
    <thead  v-if="active">
      <slot name="columns">
        <th v-for="column in columns" :key="column">{{column}}</th>
      </slot>
    </thead>
    <tbody  v-if="active">
      <tr v-for="(item, index) in data" :key="index">
        <slot :row="item">
          <td><router-link :to="'/members/' + item.user.id">{{item.user.name}}</router-link></td>
          <td>{{item.message}}</td>
          <td>{{item.created || moment("from")}}</td>
          <td>
            <span
              :class="{
            'bg-success p-2 rounded text-light' : item.status == 'new', 
            'bg-warning p-2 rounded text-light': item.status == 'active',
            'bg-danger p-2 rounded text-light': item.status == 'closed'
            }"
            >{{item.status}}</span>
          </td>
        </slot>
      </tr>
    </tbody>
  </table>
  </div>
</template>
<script>
export default {
  name: "paper-table",
  props: {
    active:false,
    columns: Array,
    data: Array,
    type: {
      type: String, // striped | hover
      default: "striped"
    },
    title: {
      type: String,
      default: ""
    },
    subTitle: {
      type: String,
      default: ""
    }
  },
  computed: {
    tableClass() {
      return `table-${this.type}`;
    }
  },
  methods: {
    hasValue(item, column) {
      return item[column.toLowerCase()] !== "undefined";
    },
    itemValue(item, column) {
      var x = item[column.toLowerCase()];
      return x;
    }
  }
};
</script>
<style>
.new {
  background-color: green;
}
.active-tag{
  transition: ease-in 5s;
}
</style>
