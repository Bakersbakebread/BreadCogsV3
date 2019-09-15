import DashboardLayout from "@/layout/dashboard/DashboardLayout.vue";
// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";

// Admin pages
import Dashboard from "@/pages/Dashboard.vue";
import UserProfile from "@/pages/UserProfile.vue";
import Notifications from "@/pages/Notifications.vue";
import Icons from "@/pages/Icons.vue";
import Maps from "@/pages/Maps.vue";
import Typography from "@/pages/Typography.vue";
import TableList from "@/pages/TableList.vue";
import BotSystemSettings from "@/pages/BotSystemSettings.vue";
import MembersPage from "@/pages/MembersPage.vue";
import LoginPage from "@/pages/LoginPage.vue";

const routes = [
  { path: "/login", component: LoginPage, name: "login" },
  {
    path: "/",
    component: DashboardLayout,
    redirect: "/dashboard",
    meta:{
      requiresAuth: true
    },
    children: [
      {
        path: "dashboard",
        name: "dashboard",
        component: Dashboard
      },
      {
        path: "bot-settings",
        name: "Redbot Settings",
        component: BotSystemSettings
      },
      {
        path: "members",
        name: "Visible Members",
        component: MembersPage
      },
      {
        path: "members/:search",
        name: "Visible Members Search",
        component: MembersPage
      },
      {
        path: "stats",
        name: "stats",
        component: UserProfile
      },
      {
        path: "notifications",
        name: "notifications",
        component: Notifications
      },
      {
        path: "icons",
        name: "icons",
        component: Icons
      },
      {
        path: "maps",
        name: "maps",
        component: Maps
      },
      {
        path: "typography",
        name: "typography",
        component: Typography
      },
      {
        path: "table-list",
        name: "table-list",
        component: TableList
      }
    ]
  },
  { path: "*", component: NotFound }
];

/**
 * Asynchronously load view (Webpack Lazy loading compatible)
 * The specified component must be inside the Views folder
 * @param  {string} name  the filename (basename) of the view to load.
function view(name) {
   var res= require('../components/Dashboard/Views/' + name + '.vue');
   return res;
};**/

export default routes;