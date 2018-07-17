<template lang="html">
  <div>
    <v-card>
      <v-layout row wrap>
        <v-flex xs12 sm4><AirportSelector label="Origin" :id="id"/></v-flex>
        <v-flex xs12 sm4><AirportSelector label="Destination" :id="id"/></v-flex>
        <v-flex xs12 sm4><MultiDate/></v-flex>
      </v-layout>
      <v-speed-dial
        v-model="fab"
        top
        right
        absolute
        transition="slide-y-reverse-transition"
        direction="left"
        open-on-hover
      >

        <v-btn
          slot="activator"
          v-model="fab"
          color="primary"
          dark
          fab
        >
          <v-icon large>chevron_left</v-icon>
          <v-icon>close</v-icon>
        </v-btn>
        <v-tooltip bottom>
          <v-btn
            slot='activator'
            fab
            outline
            small
            color="primary"
            @click.native="addEmptyCard"
          >
            <v-icon>add</v-icon>
          </v-btn>
          <span>Add new search below</span>
        </v-tooltip>
        <v-tooltip bottom>
          <v-btn
            slot='activator'
            fab
            outline
            small
            color="primary"
          >
            <v-icon>swap_horiz</v-icon>
          </v-btn>
          <span>Add and reverse Locations</span>
        </v-tooltip>
        <v-btn
          fab
          outline
          small
          color="red"
          v-if="!hideOneCard"
        >
          <v-icon>delete</v-icon>
        </v-btn>
      </v-speed-dial>
    </v-card>
    <v-snackbar
      v-model="alert"
      color="warning"
      :timeout="timeout"
    >
      <v-icon color="white">priority_high</v-icon>
      Multiple Searches is currently not supported.
      <v-btn
        dark
        flat
        @click.native="alert = false"
      >
        Close
      </v-btn>
    </v-snackbar>
  </div>

</template>

<script>
/* eslint-disable import/no-unresolved */
import MultiDate from '@/components/MultiDate.vue';
import AirportSelector from '@/components/AirportSelector.vue';
import { mapGetters, mapActions } from 'vuex';
/* eslint-enable import/no-unresolved */

export default {
  name: 'SearchCard',
  components: {
    MultiDate,
    AirportSelector,
  },
  data() {
    return {
      alert: false,
      timeout: 3000,
      fab: false,
    };
  },
  props: {
    id: {
      default: 0,
      type: Number,
    },
  },
  computed: {
    ...mapGetters('formDetails', [
      'hideOneCard',
    ]),
  },
  methods: {
    ...mapActions('formDetails', ['addEmptyCard']),
  },
};
</script>

<style lang="css">
</style>
