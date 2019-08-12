import Vue from "vue";
import App from "./App";
import router from "./router/index";
import { store } from './store/index'

import PaperDashboard from "./plugins/paperDashboard";
import "vue-notifyjs/themes/default.css";

router.beforeEach((to, from, next) => {
  var requiresAuth = to.matched.some( record => record.meta.requiresAuth );
  var token = store.getters.authToken
  if (requiresAuth && !token) {
    next('/login')
  }
  else if(to.path == '/login' && token){
    next('/')
  }
  else{
    next()
  }
})

Vue.use(PaperDashboard);

/* eslint-disable no-new */
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
