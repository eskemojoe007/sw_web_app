<template lang="html">
  <div>
    <h1>How does this work?</h1>
    {{ flights }}
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  mounted() {
    this.fetchFlights(1);
  },

  computed: {
    ...mapState([
      'flights',
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
