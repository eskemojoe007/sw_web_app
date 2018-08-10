<template lang="html">
  <v-container>
    <h1>Enter Search</h1>
    <v-form ref="form" v-model="valid" lazy-validation>
      <SearchCard v-for="id in cardList" :key="id" :id="id"/>
      <!-- <SearchCard/> -->
      <v-btn
        :disabled="!valid"
        @click.native="submit"
        color="primary"
      >
        submit
      </v-btn>
      <v-btn @click="clear">clear all</v-btn>
    </v-form>
    <v-snackbar
      v-model="alert"
      color="error"
      :timeout="timeout"
    >
      <v-icon color="white">priority_high</v-icon>
      Search is not currently connected to the backend just yet...Be patient
      <v-btn
        dark
        flat
        @click.native="alert = false"
      >
        Close
      </v-btn>
    </v-snackbar>
  </v-container>
</template>

<script>
/* eslint-disable import/no-unresolved */
import SearchCard from '@/components/SearchCard.vue';
/* eslint-enable import/no-unresolved */
import { mapState, mapGetters, mapActions } from 'vuex';

export default {
  name: 'Search',
  data() {
    return {
      valid: true,
      alert: false,
      timeout: 3000,
    };
  },
  components: {
    SearchCard,
  },
  computed: {
    ...mapState('formDetails', ['cardList']),
    // ...mapGetters('formDetails', ['maxCardId']),
  },
  methods: {
    ...mapActions('formDetails', ['resetState']),
    submit() {
      this.valid = this.$refs.form.validate();
      if (this.valid) {
        this.alert = true;
      }
      // console.log(this.$refs.form.validate());
      // if (this.cardList.length > 1) {
      //   this.alert = true;
      // }
    },
    clear() {
      this.$refs.form.reset();
      this.resetState();
    },
  },
};
</script>

<style lang="css">
</style>
