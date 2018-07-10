import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';
import About from './views/About.vue';
import BasicFlightList from './components/BasicFlightList.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/about',
      name: 'about',
      component: About,
    },
    {
      path: '/results',
      name: 'results',
      component: BasicFlightList,
    },
    {
      path: '/search',
      name: 'search',
      // component: NotDone,
    },
    {
      path: '/bug',
      name: 'bug',
      // component: NotDone,
    },
  ],
});
