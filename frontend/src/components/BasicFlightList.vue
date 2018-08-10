<template lang="html">
  <v-container>
    <h1>Enter an old search ID (try 4)</h1>
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
        <td>{{ props.item.origin_airport }}</td>
        <td>{{ props.item.destination_airport }}</td>
        <td>{{ `\$${props.item.min_price}` }}</td>
        <td>{{ secondsToHm(props.item.travel_time) }}</td>
        <td>{{ props.item.depart_time }}</td>
        <td>{{ props.item.arrive_time }}</td>
      </template>
    </v-data-table>
    <!-- <ul v-if="sortFlightsNum > 0 && !loading">
      <li v-for="flight in sortFlights" :key="flight.id"> {{ flight.min_price }} </li>
    </ul> -->
  </v-container>
</template>

<script>
import { mapGetters, mapActions, mapState } from 'vuex';

export default {
  name: 'BasicFlightList',
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
        { text: 'Travel Time', value: 'travel_time' },
        { text: 'Departure Time', value: 'depart_time' },
        { text: 'Arrival Time', value: 'arrive_time' },
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
      'filterFlightsNum',
    ]),
    ...mapState([
      'loading',
    ]),
  },
  methods: {
    ...mapActions([
      'fetchFlights',
    ]),
    secondsToHm(seconds) {
      const d = Number(seconds);
      const h = Math.floor(d / 3600);
      const m = Math.floor((d % 3600) / 60);
      // const s = Math.floor(d % 3600 % 60);

      const hDisplay = h > 0 ? `${h}h` : '';
      const mDisplay = m > 0 ? ` ${m}m` : '';
      // let sDisplay = s > 0 ? s + (s == 1 ? " second" : " seconds") : "";
      return hDisplay + mDisplay;
    },
  },
};
</script>

<style lang="css">
</style>
