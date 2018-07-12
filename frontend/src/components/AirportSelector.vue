<template lang="html">
  <v-autocomplete
    v-model="selectedAirports"
    :items="getParsableAirports"
    item-text="name"
    item-value="abrev"
    :label="label"
    multiple
    clearable
  >
    <template slot="selection" slot-scope="data">
      <!--TODO selectItem isn't ideal.  -->
      <v-chip
        close
        @input="data.parent.selectItem(data.item)"
        class="chip--select-multi"
        small
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
</template>

<script>
import { mapGetters, mapActions, mapState } from 'vuex';

export default {
  data() {
    return {
      selectedAirports: [],
    };
  },
  props: {
    label: {
      type: String,
      default: 'Select Airports',
    },
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
