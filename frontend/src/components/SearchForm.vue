<template lang="html">
  <div>
    <h1>Search Form</h1>
    <v-autocomplete
      v-model="origin"
      :items="airports"
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
          :selected="data.seclected"
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
export default {
  data() {
    return {
      airports: [
        { abrev: 'ATL', name: 'Atlanta - ATL' },
        { abrev: 'GSP', name: 'Greenville - GSP' },
        { abrev: 'CLT', name: 'Charlotte - CLT' },
        { abrev: 'AUS', name: 'Austin - AUS' },
        { abrev: 'DAL', name: 'Dallas - DAL' },
      ],
      origin: null,

    };
  },
};
</script>

<style lang="css">
</style>
