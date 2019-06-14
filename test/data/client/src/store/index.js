import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";

Vue.use(Vuex)

const URL = "http://localhost:42356"

export const store = new Vuex.Store({
  state: {
    allGuildSettings: '',
    loading: true
  },
  actions: {
    loadAllGuildSettings({
      commit
    }) {
      axios
      .post(`${URL}/guilds/settings`)
      .then((response) => {
        // console.log(response.data, this)
        commit('setAllGuildSettings', JSON.parse(response.data))
        commit('changeLoadingState', false)
      })
    }
  },
  mutations:{
    setAllGuildSettings(state, allGuildSettings){
      state.allGuildSettings = allGuildSettings
    },
    changeLoadingState(state, loading) {
      state.loading = loading
    }
  },
  getters:{
    allGuildSettings: state => state.allGuildSettings
  }
})
