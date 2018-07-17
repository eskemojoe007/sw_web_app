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
    FETCH_FLIGHTS(state, newFlights) {
      state.flights = newFlights;
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
      return state.airports.filter(airport => !!airport.sw_airport);
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
    FETCH_AIRPORTS(state, newAirports) {
      state.airports = newAirports;
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
    fetchAirports({ commit }) {
      commit('onLoading');
      Vue.axios.get('http://localhost:8000/query_flight/airports/')
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

const formDetails = {
  namespaced: true,
  state: {
    cards: [
      {
        id: 1,
        origins: [],
        destinations: [],
        dates: [],
      },
    ],
    // height: null,
  },
  getters: {
    numCards(state) {
      return state.cards.length;
    },
    maxCardId(state) {
      return Math.max(...state.cards.map(card => card.id));
    },
    hideOneCard(state, getters) {
      return getters.numCards === 1;
    },
    cardById: (state) => (id) => {
      return state.cards.find(card => card.id === id)
    },
    // cardById(state, id) {
    //   return state.cards.find(card => card.id === id);
    // },
  },
  mutations: {
    addEmptyCard(state, card) {
      state.cards.push(card);
    },
    setInputVal(state, payload) {
      const card = state.cards.find(obj => obj.id === payload.id);

    },
  },
  actions: {
    addEmptyCard({ commit, getters }) {
      const id = getters.maxCardId + 1;
      const emptyCard = {
        id,
        origins: [],
        destinations: [],
        dates: [],
      };
      commit('addEmptyCard', emptyCard);
    },
    // setValue({ commit, getters }, payload) {
    //   let card = getters.cardById(payload.id);
    //   card[payload.description] = payload.value;
    //   commit
    // },
  },
};

export default new Vuex.Store({
  modules: {
    flights,
    airports,
    formDetails,
  },
});
