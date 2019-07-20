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
          <td>
            <tooltip>
              <span slot="text">{{item.created | moment("from")}}</span>
              <span slot="tooltip">{{item.created}}</span>
              </tooltip>
          </td>
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
<style lang="scss">
.new {
  background-color: green;
}
.active-tag{
  transition: ease-in 5s;
}
.tooltip {
  display: block !important;
  z-index: 10000;

  .tooltip-inner {
    background: black;
    color: white;
    border-radius: 16px;
    padding: 5px 10px 4px;
  }

  .tooltip-arrow {
    width: 0;
    height: 0;
    border-style: solid;
    position: absolute;
    margin: 5px;
    border-color: black;
    z-index: 1;
  }

  &[x-placement^="top"] {
    margin-bottom: 5px;

    .tooltip-arrow {
      border-width: 5px 5px 0 5px;
      border-left-color: transparent !important;
      border-right-color: transparent !important;
      border-bottom-color: transparent !important;
      bottom: -5px;
      left: calc(50% - 5px);
      margin-top: 0;
      margin-bottom: 0;
    }
  }

  &[x-placement^="bottom"] {
    margin-top: 5px;

    .tooltip-arrow {
      border-width: 0 5px 5px 5px;
      border-left-color: transparent !important;
      border-right-color: transparent !important;
      border-top-color: transparent !important;
      top: -5px;
      left: calc(50% - 5px);
      margin-top: 0;
      margin-bottom: 0;
    }
  }

  &[x-placement^="right"] {
    margin-left: 5px;

    .tooltip-arrow {
      border-width: 5px 5px 5px 0;
      border-left-color: transparent !important;
      border-top-color: transparent !important;
      border-bottom-color: transparent !important;
      left: -5px;
      top: calc(50% - 5px);
      margin-left: 0;
      margin-right: 0;
    }
  }

  &[x-placement^="left"] {
    margin-right: 5px;

    .tooltip-arrow {
      border-width: 5px 0 5px 5px;
      border-top-color: transparent !important;
      border-right-color: transparent !important;
      border-bottom-color: transparent !important;
      right: -5px;
      top: calc(50% - 5px);
      margin-left: 0;
      margin-right: 0;
    }
  }

  &[aria-hidden='true'] {
    visibility: hidden;
    opacity: 0;
    transition: opacity .15s, visibility .15s;
  }

  &[aria-hidden='false'] {
    visibility: visible;
    opacity: 1;
    transition: opacity .15s;
  }
}
</style>
