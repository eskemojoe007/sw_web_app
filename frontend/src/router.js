import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';
import About from './views/About.vue';
import Search from './views/Search.vue';
import BasicFlightList from './components/BasicFlightList.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/search',
      // name: 'home',
      // component: Search,
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
      component: Search,
    },
    {
      path: '/bug',
      name: 'bug',
      // component: NotDone,
    },
  ],
});
