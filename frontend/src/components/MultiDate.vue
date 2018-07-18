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
      prepend-inner-icon="event"
      multiple
      readonly
      clearable
      box
      ref='dateText'
      required
      :rules="datesAllRules"
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
      :min="minDate"
      :max="maxDate"
    >
      <v-spacer/>
      <v-btn
        color="primary"
        @click="menu = false"
      >
        OK
      </v-btn>
    </v-date-picker>

  </v-menu>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      date: null,
      menu: false,
      // datesAll: [],
      datesAllRules: [
        v => (!!v && v.length > 0) || 'Must be Specified',
        v => (v && v.length <= 10) || 'Max 10 dates',
      ],
      // minDate: new Date(),
    };
  },
  props: {
    id: {
      default: 1,
      type: Number,
    },
  },
  computed: {
    minDate() {
      const today = new Date();
      return this.formatDate(today);
    },
    maxDate() {
      const today = new Date();
      today.setFullYear(today.getFullYear() + 1);
      return this.formatDate(today);
    },
    datesAll: {
      get() {
        return this.$store.state.formDetails.cards[this.id].dates;
      },
      set(value) {
        this.setCardValues({
          id: this.id,
          input: 'dates',
          value,
        });
      },
    },
  },
  methods: {
    ...mapActions('formDetails', [
      'pushCardValues',
      'spliceCardValues',
      'setCardValues',
    ]),
    save(date) {
      const dates = this.datesAll;
      const index = dates.findIndex(x => x === date);
      if (index === -1) {
        this.pushCardValues({ id: this.id, input: 'dates', value: date });
      } else {
        // this.datesAll.splice(index, 1);
        console.log('Delete that MOFO');
        this.spliceCardValues({ id: this.id, input: 'dates', index });
      }
      // this.$refs.dateText.focus();
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
    formatDate(date) {
      let month = `${date.getMonth() + 1}`;
      let day = `${date.getDate()}`;
      const year = date.getFullYear();

      if (month.length < 2) month = `0${month}`;
      if (day.length < 2) day = `0${day}`;

      return [year, month, day].join('-');
    },
  },
};
</script>

<style lang="css">
</style>
