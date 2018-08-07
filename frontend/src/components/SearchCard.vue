<template lang="html">
  <div>
    <v-card class="mb-2 px-1 pb-1">
      <v-layout row wrap>
        <v-flex xs12 md4><AirportSelector label="Origin" :id="id"/></v-flex>
        <v-flex xs12 md4><AirportSelector label="Destination" :id="id"/></v-flex>
        <v-flex xs12 md4><MultiDate :id="id"/></v-flex>
      </v-layout>
      <v-speed-dial
        class="speed-dial-card"
        v-model="fab"
        transition="slide-x-reverse-transition"
        direction="left"
        right
        absolute
      >
        <v-btn
          slot="activator"
          v-model="fab"
          color="accent"
          dark
          fab
          small
        >
          <v-icon large>chevron_left</v-icon>
          <v-icon>close</v-icon>
        </v-btn>
        <v-tooltip bottom>
          <v-btn
            slot='activator'
            fab
            small
            @click.native="addEmptyCard(id)"
            color='accent'
          >
            <v-icon>add</v-icon>
          </v-btn>
          <span>Add new search below</span>
        </v-tooltip>
        <v-tooltip bottom>
          <v-btn
            slot='activator'
            fab
            small
            @click.native="copyInvertCard(id)"
            color='accent'
          >
            <v-icon>swap_horiz</v-icon>
          </v-btn>
          <span>Add and reverse Locations</span>
        </v-tooltip>
        <v-btn
          fab
          small
          color="red accent-1"
          dark
          v-if="!hideOneCard"
          @click.native="removeCard(id)"
        >
          <v-icon>delete</v-icon>
        </v-btn>
      </v-speed-dial>
    </v-card>
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
    ...mapActions('formDetails', [
      'addEmptyCard',
      'removeCard',
      'copyInvertCard',
    ]),
  },
};
</script>

<style lang="css">
.speed-dial-card {
  bottom: -20px !important;
}
</style>
