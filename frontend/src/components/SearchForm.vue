<template lang="html">
  <div>
    <h1>Search Form</h1>
    <AirportSelector label="Origin Airports"/>
    <AirportSelector label="Destination Airports"/>
    <MultiDate/>
  </div>

</template>

<script>
/* eslint-disable import/no-unresolved */
import MultiDate from '@/components/MultiDate.vue';
import AirportSelector from '@/components/AirportSelector.vue';
/* eslint-enable import/no-unresolved */

export default {
  components: {
    MultiDate,
    AirportSelector,
  },
  data() {
    return {
      origin: null,
    };
  },
};
</script>

<style lang="css">
</style>
