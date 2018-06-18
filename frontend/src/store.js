import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    flights: [],
    loading: false,
  },

  // Check this out https://www.reddit.com/r/vuejs/comments/7dqlfc/vuex_best_practice_do_you_keep_sorted_data_in_the/
  getters: {
    filterNull(state) {
      return state.flights.filter(flight => !!flight.min_price);
    },
    sortFlights(state, getters) {
      return getters.filterNull.sort((a, b) => a.min_price - b.min_price);
    },
    sortFlightsNum(state, getters) {
      return getters.sortFlights.length;
    },
  },

  mutations: {
    FETCH_FLIGHTS(state, flights) {
      state.flights = flights;
    },

    toggleLoading(state) {
      state.loading = !state.loading;
    },
    offLoading(state) {
      state.loading = false;
    },
    onLoading(state) {
      state.loading = true;
    },
  },

  actions: {
    fetchFlights({ commit }, payload) {
      commit('onLoading');
      Vue.axios.get(`http://localhost:8000/query_flight/searchs/${payload}/`)
        .then((response) => {
          commit('FETCH_FLIGHTS', response.data.flight_set);
          commit('offLoading');
        })
        .catch((err) => {
          console.log(err);
          commit('offLoading');
        });
    },
  },
});
