<template lang="html">
  <v-container>
    <h1>Enter Search</h1>
    <v-form ref="form" v-model="valid" lazy-validation>
      <SearchCard v-for="id in cardList" :key="id" :id="id"/>
      <!-- <SearchCard/> -->
      <v-btn
        :disabled="!valid"
        @click="submit"
        color="primary"
      >
        submit
      </v-btn>
      <v-btn @click="clear">clear all</v-btn>
    </v-form>
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
    submit() {
      // this.valid = this.$refs.form.validate();
      console.log(this.$refs.form.validate());
    },
    clear() {
      this.$refs.form.reset();
      // TODO: Delete the cards we no longer need.
    },
  },
};
</script>

<style lang="css">
</style>
