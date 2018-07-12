<template lang="html">
  <v-menu
    ref="menu"
    :close-on-content-click="false"
    v-model="menu"
    :nudge-right="40"
    :return-value.sync="date"
    lazy
    transition="scale-transition"
    offset-y
    full-width
    min-width="290px"
  >
    <v-combobox
      slot="activator"
      v-model="datesAll"
      label="Departure Dates"
      prepend-icon="event"
      multiple
      readonly
      clearable
    >
      <template
        slot='selection'
        slot-scope='data'>
        <v-chip
          close
          @input="save(data.item)"
          small
        >
          {{ getString(data.item) }}
        </v-chip>
      </template>
    </v-combobox>
    <v-date-picker
      v-model="date"
      no-title
      @input="save(date)"
      :events="datesAll"
      event-color="blue lighten-1"
    >
      <v-spacer/>
      <v-btn
        flat color="primary"
        @click="menu = false"
      >
        OK
      </v-btn>
    </v-date-picker>

  </v-menu>
</template>

<script>
export default {
  data() {
    return {
      date: null,
      menu: false,
      datesAll: [],
    };
  },
  methods: {
    save(date) {
      const index = this.datesAll.findIndex(x => x === date);

      if (index === -1) {
        this.datesAll.push(date);
      } else {
        this.datesAll.splice(index, 1);
      }
    },
    getString(dtString) {
      const weekday = new Array(7);
      weekday[1] = 'Mon';
      weekday[2] = 'Tue';
      weekday[3] = 'Wed';
      weekday[4] = 'Thu';
      weekday[5] = 'Fri';
      weekday[6] = 'Sat';
      weekday[0] = 'Sun';

      const dt = new Date(dtString);
      const dayWeek = dt.getUTCDay();

      return `${weekday[dayWeek]}, ${dt.getUTCMonth()}/${dt.getUTCDate()}`;
    },
  },
};
</script>

<style lang="css">
</style>
