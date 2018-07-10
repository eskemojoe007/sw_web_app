<template lang="html">
  <div>
    <h1>How does this work?</h1>
    <!-- TODO This doesn't quite work like we'd like -->
    <input type="number" name="search ID" value=""
           v-model="searchID"
           @change="fetchFlights(searchID)"
           placeholder="search ID">
    <p v-if="loading">Loading data...</p>
    <v-data-table
      :headers="headers"
      :items="sortFlights"
      hide-actions
      class="elevation-1"
    >
      <template slot="items" slot-scope="props">
        <td class="text-xs-right">{{ props.item.origin_airport }}</td>
        <td class="text-xs-right">{{ props.item.destination_airport }}</td>
        <td class="text-xs-right">{{ props.item.min_price }}</td>
        <td class="text-xs-right">{{ props.item.travel_time }}</td>
      </template>
    </v-data-table>
    <!-- <ul v-if="sortFlightsNum > 0 && !loading">
      <li v-for="flight in sortFlights" :key="flight.id"> {{ flight.min_price }} </li>
    </ul> -->
  </div>
</template>

<script>
import { mapGetters, mapActions, mapState } from 'vuex';

export default {
  data() {
    return {
      searchID: null,
      headers: [
        {
          text: 'Origin',
          value: 'origin_airport',
        },
        { text: 'Destination', value: 'destination_airport' },
        { text: 'Price', value: 'min_price' },
        { text: 'Time', value: 'travel_time' },
      ],
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
