<template lang="html">
  <div>
    <h1>Search Form</h1>
    <v-autocomplete
      v-model="origin"
      :items="airports"
      label="Select Departure Airports"
      multiple
      clearable
      chips
      solo
    >
      <template slot="selection" slot-scope="data">
        <v-chip
          close
          :selected="data.seclected"
          @input="data.parent.selectItem(data.item)"
        >
          {{data.item}}
        </v-chip>
      </template>

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
