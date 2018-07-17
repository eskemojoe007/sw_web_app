<template lang="html">
  <v-autocomplete
    v-model="selectedAirports"
    :items="getParsableAirports"
    item-text="name"
    item-value="abrev"
    :label="labelString"
    multiple
    clearable
    box
    prepend-inner-icon="place"
    :height="height"
    required
    :rules="selectedAirportsRules"
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
      // selectedAirports: [],
      height: null,
      selectedAirportsRules: [
        v => (!!v && v.length > 0) || `${this.label} Must be Specified`,
        v => (v && v.length <= 10) || `Max 10 ${this.label} airports`,
      ],
    };
  },
  props: {
    label: {
      type: String,
      default: 'Origin',
    },
    id: {
      type: Number,
      default: 1,
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
    labelString() {
      return `${this.label} Airports`;
    },
    selectedAirports: {
      get() {
        let vals;
        if (this.label.toUpperCase() === 'ORIGIN') {
          // vals = this.$store.getters.cardById(this.id).origins;
          vals = this.$store.state.formDetails.cards[this.id].origins;
        } else if (this.label.toUpperCase() === 'DESTINATION') {
          // vals = this.$store.getters.cardById(this.id).destinations;
          vals = this.$store.state.formDetails.cards[this.id].destinations;
        } else {
          vals = [];
          console.log('label must be ORIGIN or DESTINATION');
        }
        return vals;
      },
      set(value) {
        this.setCardValues({ id: this.id, value})
        // this.$store.commit('setCardValues', { id: this.id, value })
      },
    },
  },
  methods: {
    ...mapActions([
      'fetchAirports',
    ]),
    ...mapActions('formDetails', [
      'setCardValues',
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
