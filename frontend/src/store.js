import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    flights: [],
  },
  mutations: {
    FETCH_FLIGHTS(state, flights) {
      state.flights = flights
    },
  },
  actions: {
    fetchFlights({ commit }, payload) {
      axios.get(`http://localhost:8000/query_flight/searchs/${payload}/`)
        .then((response) => {
          commit('FETCH_FLIGHTS', response.data['flight_set']);
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
});
