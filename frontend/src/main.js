import '@babel/polyfill'
import Vue from 'vue';
import './plugins/axios'
import './plugins/vuetify'
// import axios from 'axios';
// import VueAxios from 'vue-axios';
import App from './App.vue';
import store from './store';
import router from './router'

// Vue.use(VueAxios, axios);

Vue.config.productionTip = false;

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app');
