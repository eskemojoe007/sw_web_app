<template lang="html">
  <div>
    <h1>How does this work?</h1>
    <input type="number" name="search ID" value=""
           v-model="searchID"
           @change="fetchFlights(searchID)"
           placeholder="search ID">
    <p v-if="loading">Loading data...</p>
    <ul v-if="sortFlightsNum > 0 && !loading">
      <li v-for="flight in sortFlights" :key="flight.id"> {{ flight.min_price }} </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapState } from 'vuex';

export default {
  data() {
    return {
      searchID: null,
    };
  },
  //
  // mounted() {
  //   this.fetchFlights(this.searchID);
  // },

  computed: {
    ...mapGetters([
      'sortFlights',
      'sortFlightsNum',
    ]),
    ...mapState([
      'loading',
    ]),
  },
  methods: {
    ...mapActions([
      'fetchFlights',
    ]),
  },
};
</script>

<style lang="css">
</style>
