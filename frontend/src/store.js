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
      Vue.axios.get(`https://pacific-caverns-22538.herokuapp.com/query_flight/searchs/${payload}/`)
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
      Vue.axios.get('https://pacific-caverns-22538.herokuapp.com/query_flight/airports/')
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


function emptyCard() {
  return {
    origins: [],
    destinations: [],
    dates: [],
  };
}
// const emptyCard = {
//   origins: [],
//   destinations: [],
//   dates: [],
// };

// https://forum.vuejs.org/t/vuex-best-practices-for-complex-objects/10143
const formDetails = {
  namespaced: true,
  state: {
    cards: {
      1: emptyCard(),
    },
    cardList: [1],
    // height: null,
  },
  getters: {
    numCards(state) {
      return state.cardList.length;
    },
    maxCardId(state) {
      return Math.max(...state.cardList);
      // return Math.max(...state.cards.map(card => card.id));
    },
    hideOneCard(state, getters) {
      return getters.numCards === 1;
    },
    // cardById: (state) => (id) => {
    //   return state.cards[id]
    // },
    // cardById(state, id) {
    //   return state.cards.find(card => card.id === id);
    // },
  },
  mutations: {
    addCardList(state, payload) {
      const { oldID } = payload;
      const { newID } = payload;
      const index = state.cardList.findIndex(x => x === oldID);
      state.cardList.splice(index + 1, 0, newID);
    },
    addCardObj(state, payload) {
      state.cards[payload.id] = payload.card;
    },
    removeCardList(state, id) {
      const index = state.cardList.findIndex(x => x === id);
      if (!(index === -1)) {
        state.cardList.splice(index, 1);
      } else {
        console.log('Tried to remove item that didnt exist');
      }
    },
    removeCardObj(state, id) {
      delete state.cards[id];
    },
    commitCardValues(state, payload) {
      state.cards[payload.id][payload.input] = payload.value;
    },
    commitPushValue(state, payload) {
      state.cards[payload.id][payload.input].push(payload.value);
    },
    commitSpliceValue(state, payload) {
      state.cards[payload.id][payload.input].splice(payload.index, 1);
    },
    resetCardObj(state) {
      state.cards = { 1: emptyCard() };
    },
    resetCartList(state) {
      state.cardList = [1];
    },
    // setInputVal(state, payload) {
    //   const card = state.cards.find(obj => obj.id === payload.id);
    // },
  },
  actions: {
    addEmptyCard({ commit, getters }, oldID) {
      const newID = getters.maxCardId + 1;
      commit('addCardList', { newID, oldID });
      commit('addCardObj', {
        id: newID,
        card: emptyCard(),
      });
    },
    removeCard({ commit }, id) {
      commit('removeCardList', id);
      commit('removeCardObj', id);
    },
    setCardValues({ commit }, payload) {
      commit('commitCardValues', payload);
    },
    datesSave({ commit, state }, payload) {
      const { id } = payload;
      const { date } = payload;
      const { dates } = state.cards[id];
      // const dates = state.cards[id].dates;
      const index = dates.findIndex(x => x === date);
      if (index === -1) {
        commit('commitPushValue', { id, input: 'dates', value: date });
      } else {
        // this.datesAll.splice(index, 1);
        commit('commitSpliceValue', { id, input: 'dates', index });
      }
    },
    copyInvertCard({ commit, state, getters }, oldID) {
      const newID = getters.maxCardId + 1;
      commit('addCardList', { newID, oldID });
      commit('addCardObj', {
        id: newID,
        card: {
          origins: state.cards[oldID].destinations,
          destinations: state.cards[oldID].origins,
          dates: [],
        },
      });
    },
    resetState({ commit }) {
      commit('resetCardObj');
      commit('resetCartList');
    },
  },
};

export default new Vuex.Store({
  modules: {
    flights,
    airports,
    formDetails,
  },
});
