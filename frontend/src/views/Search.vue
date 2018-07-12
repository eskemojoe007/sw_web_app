<template lang="html">
  <div class="search">
    <SearchForm/>
  </div>
</template>

<script>
/* eslint-disable import/no-unresolved */
import SearchForm from '@/components/SearchForm.vue';
/* eslint-enable import/no-unresolved */

export default {
  name: 'Home',
  components: {
    SearchForm,
  },
};
</script>

<style lang="css">
</style>
