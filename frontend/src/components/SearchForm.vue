<template lang="html">
  <div>
    <h1>Search Form</h1>
    <v-autocomplete
      v-model="origin"
      :items="airports"
      hint="departure Airport"
      label="Select"
      multiple
      box
    >

    </v-autocomplete>

  </div>

</template>

<script>
export default {
  data() {
    return {
      airports: ['ATL', 'GSP', 'CLT', 'AUS', 'DAL'],
      origin: null,

    };
  },
};
</script>

<style lang="css">
</style>
