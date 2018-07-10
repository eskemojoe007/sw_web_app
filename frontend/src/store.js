import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);


const flights = {
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
    filterFlightsNum(state, getters) {
      return getters.filterNull.length;
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
};

const airports = {
  state: {
    airports: [],
    loading: false,
  },

  getters: {
    filterSW(state) {
      return state.airports.filter(airport => !!airport.sw_airport)
    },
    getLenAirports(state, getters) {
      return getters.filterSW.length;
    },
    getParsableAirports(state, getters) {
      return getters.filterSW.map(airport =>
        ({ abrev: airport.abrev, name: `${airport.title} - ${airport.abrev}` }));
    },
  },
  mutations: {
    FETCH_AIRPORTS(state, airports) {
      state.airports = airports;
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
    fetchAirports({ commit }, payload) {
      commit('onLoading');
      Vue.axios.get(`http://localhost:8000/query_flight/airports/`)
        .then((response) => {
          commit('FETCH_AIRPORTS', response.data);
          commit('offLoading');
        })
        .catch((err) => {
          console.log(err);
          commit('offLoading');
        });
    },
  },
};

export default new Vuex.Store({
  modules: {
    flights,
    airports,
  },
});
