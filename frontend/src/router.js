import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";
import RegSignIn from "./views/RegSignIn.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/home",
      name: "home",
      component: Home
    },
    {
      path: "/",
      name: "signin",
      component: RegSignIn
    }
  ]
});
