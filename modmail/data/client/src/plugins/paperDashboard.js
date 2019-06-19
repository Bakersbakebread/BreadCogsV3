import Notify from "vue-notifyjs";
import SideBar from "@/components/SidebarPlugin";
import GlobalComponents from "./globalComponents";
import GlobalDirectives from "./globalDirectives";
import "es6-promise/auto";
// Import component
import Loading from "vue-loading-overlay";
// Import stylesheet
import "vue-loading-overlay/dist/vue-loading.css";
// Init plugin

//css assets
import "bootstrap/dist/css/bootstrap.css";
import "@/assets/sass/paper-dashboard.scss";
import "@/assets/css/themify-icons.css";

export default {
  install(Vue) {
    Vue.use(Loading);
    Vue.use(require("vue-moment"));
    Vue.use(GlobalComponents);
    Vue.use(GlobalDirectives);
    Vue.use(SideBar);
    Vue.use(Notify);
  }
};
