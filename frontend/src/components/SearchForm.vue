<template lang="html">
  <div>
    <h1>Search Form</h1>
    <v-autocomplete
      v-model="origin"
      :items="getParsableAirports"
      item-text="name"
      item-value="abrev"
      label="Select Departure Airports"
      chips
      multiple
      clearable
    >
      <template slot="selection" slot-scope="data">
        <v-chip
          close
          @input="data.parent.selectItem(data.item)"
          class="chip--select-multi"
        >
          {{ data.item.abrev }}
        </v-chip>

      </template>
      <template slot="no-data">
        <v-list-tile>
          <v-list-tile-title>
            Search for your needed SW
            <strong>Airport</strong>
          </v-list-tile-title>
        </v-list-tile>
      </template>
    </v-autocomplete>

  </div>

</template>

<script>
import { mapGetters, mapActions, mapState } from 'vuex';

export default {
  data() {
    return {
      origin: null,
    };
  },
  computed: {
    ...mapGetters([
      'getLenAirports',
      'getParsableAirports',
    ]),
    ...mapState([
      'loading',
    ]),
  },
  methods: {
    ...mapActions([
      'fetchAirports',
    ]),
  },
  mounted() {
    if (this.getLenAirports <= 0 && !this.loading) {
      this.fetchAirports();
    }
  },
};
</script>

<style lang="css">
</style>
