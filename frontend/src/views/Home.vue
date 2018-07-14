<template>
  <div class="home">
    <HelloWorld msg="Super Cool"/>
  </div>
</template>

<script>
// @ is an alias to /src
/* eslint-disable import/no-unresolved */
import HelloWorld from '@/components/HelloWorld.vue';
/* eslint-enable import/no-unresolved */

export default {
  name: 'Home',
  components: {
    HelloWorld,
  },
};
</script>
