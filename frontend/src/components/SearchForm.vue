<template lang="html">
  <div>
    <h1>Search Form</h1>
    <AirportSelector label="Origin Airports"/>
    <AirportSelector label="Destination Airports"/>
    <MultiDate/>
  </div>

</template>

<script>
import MultiDate from '@/components/MultiDate.vue'
import AirportSelector from '@/components/AirportSelector.vue'

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
