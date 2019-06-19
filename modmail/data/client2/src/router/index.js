import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/pages/HelloWorld'
import GuildSettings from '@/pages/GuildSettings'

Vue.use(Router)

export default new Router({
  // linkActiveClass: "active",
  linkExactActiveClass: "active",
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/guild-settings',
      name : 'GuildSettings',
      component : GuildSettings
    }
  ]
})
