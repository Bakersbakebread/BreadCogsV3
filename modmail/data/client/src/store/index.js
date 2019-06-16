import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";

Vue.use(Vuex)

const URL = "http://localhost:42356"

export const store = new Vuex.Store({
  state: {
    allGuildSettings: '',
    allMembersShort: '',
    botSysSettings: '',
    allThreads: '',
    loading: false
  },
  actions: {
    setLoading({commit, state}){
      commit('changeLoadingState', state);
    },
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
    },
    loadBotSysSettings({
      commit
    }) {
      axios
      .post(`${URL}/bot/sys-settings`)
      .then((response) => {
        // console.log(response.data, this)
        commit('setBotSysSettings', JSON.parse(response.data))
        commit('changeLoadingState', false)
      })
    },
    loadAllModMailThreads({
      commit
    }) {
      axios
      .post(`${URL}/guilds/all-messages`)
      .then((response) => {
        // console.log(response.data, this)
        commit('setAllThreads', JSON.parse(response.data))
        commit('changeLoadingState', false)
      })
    },
    loadAllMembersShort({
      commit
    }) {
      axios
      .post(`${URL}/members/get-all-short`)
      .then((response) => {
        // console.log(response.data, this)
        commit('setAllMembersShort', JSON.parse(response.data))
        commit('changeLoadingState', false)
      })
    }
  },
  mutations:{
    setAllGuildSettings(state, allGuildSettings){
      state.allGuildSettings = allGuildSettings
    },
    setAllThreads(state, allThreads){
      state.allThreads = allThreads
    },
    setBotSysSettings(state, botSysSettings){
      state.botSysSettings = botSysSettings
    },
    setAllMembersShort(state, allMembersShort){
      state.allMembersShort = allMembersShort
    },
    changeLoadingState(state, loading) {
      state.loading = loading
    }
  },
  getters:{
    loading: state => state.loading,
    allGuildSettings: state => state.allGuildSettings,
    allMembersShort: state => state.allMembersShort,
    botSysSettings: state => state.botSysSettings,
    allThreads: state => state.allThreads,
    
    onlyClosedThreads: (state) => {
      const threads = state.allThreads;
      const newObj ={};
      
      Object.entries(threads).forEach(([key, value]) => {
          newObj[key]  = {...value, threads: value.threads.filter(x => x.status === 'closed')};
      })
      return newObj;
    },
    onlyActiveThreads: (state) => {
      const threads = state.allThreads;
      const newObj ={};
      
      Object.entries(threads).forEach(([key, value]) => {
          newObj[key]  = {...value, threads: value.threads.filter(x => x.status === 'active')};
      })
      return newObj;
    },
    onlyNewThreads: (state) => {
      const threads = state.allThreads;
      const newObj ={};
      
      Object.entries(threads).forEach(([key, value]) => {
          newObj[key]  = {...value, threads: value.threads.filter(x => x.status === 'new')};
      })
      return newObj;
    },

    getGuildById: (state, getters) => (id) => {
      var myArray = state.allGuildSettings;
      for (var i=0; i < myArray.length; i++) {
        if (myArray[i].guild.id === id) {
            return myArray[i];
        }
    }
    }
  }
})
