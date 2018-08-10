<template>
  <v-app>
    <v-navigation-drawer
      class="pa-0"
      persistent
      :mini-variant="miniVariant"
      :clipped="clipped"
      v-model="drawer"
      enable-resize-watcher
      fixed
      app
    >
      <v-layout column fill-height>
        <v-list>
          <v-list-tile
            v-for="(item, i) in items_top"
            :key="i"
            :to="item.to"
            :active-class="highlightColor"
          >
            <v-list-tile-action>
              <v-icon v-html="item.icon"/>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title v-text="item.title"/>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
        <v-spacer/>
        <v-list>
          <v-list-tile
            v-for="(item, i) in items_bottom"
            :key="i"
            :to="item.to"
            :href="item.href"
            :active-class="highlightColor"
            :target="item.target"
          >
            <v-list-tile-action>
              <v-icon v-html="item.icon"/>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title v-text="item.title"/>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile
            :active-class="highlightColor"
            @click.stop="miniVariant = !miniVariant"
          >
            <v-list-tile-action>
              <v-icon v-html="miniVariant ? 'chevron_right' : 'chevron_left'"/>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Mini Sidebar</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-layout>
    </v-navigation-drawer>
    <v-toolbar
      app
      :clipped-left="clipped"
      color='primary'
      dark
    >
      <v-toolbar-side-icon @click.stop="drawer = !drawer"/>
      <!-- <v-btn icon @click.stop="miniVariant = !miniVariant">
        <v-icon v-html="miniVariant ? 'chevron_right' : 'chevron_left'"/>
      </v-btn> -->
      <!-- <v-btn icon @click.stop="clipped = !clipped">
        <v-icon>web</v-icon>
      </v-btn> -->
      <!-- <v-btn icon @click.stop="fixed = !fixed">
        <v-icon>remove</v-icon>
      </v-btn> -->
      <v-toolbar-title v-text="title"/>
      <v-spacer/>
    </v-toolbar>
    <v-content>
      <router-view/>
    </v-content>
    <!-- <v-footer :fixed="fixed" app>
      <span>&copy; 2017</span>
    </v-footer> -->
  </v-app>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue';
// import BasicFlightList from './components/BasicFlightList.vue';
// import SearchForm from './components/SearchForm.vue';
import { mapActions } from 'vuex';

export default {
  name: 'App',
  // components: {
  //   HelloWorld,
  //   BasicFlightList,
  // },
  data() {
    return {
      clipped: true,
      drawer: false,
      highlightColor: 'grey lighten-2',
      // fixed: false,
      items_top: [
        // {
        //   icon: 'home',
        //   title: 'Home',
        //   // to: { name: 'home' },
        //   to: '/',
        // },
        {
          icon: 'flight',
          title: 'Search Flights',
          // to: '/about',
          to: { name: 'search' },
        },
        {
          icon: 'history',
          title: 'Old Searches',
          // to: '/about',
          to: { name: 'results' },
        },
      ],
      items_bottom: [
        {
          icon: 'question_answer',
          title: 'About',
          // to: '/about',
          to: { name: 'about' },
          href: null,
          target: null,
        },
        {
          icon: 'bug_report',
          title: 'Report Bug',
          // to: '/about',
          to: null,
          href: 'https://github.com/eskemojoe007/sw_web_app/issues/new',
          target: '_blank',
        },
      ],
      miniVariant: false,
      title: 'SW Searcher',
    };
  },
  methods: {
    ...mapActions([
      'fetchAirports',
    ]),
  },
  created() {
    this.fetchAirports();
  },
};
</script>
