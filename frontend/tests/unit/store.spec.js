// import { shallowMount, createLocalVue, mount } from '@vue/test-utils';
// import { mount } from '@vue/test-utils';
// eslint-disable-next-line import/no-unresolved
// import HelloWorld from '@/components/HelloWorld.vue';
// import Vuetify from 'vuetify';
import { flights } from '@/store';

describe('Flight Store', () => {
  it('Tests default airports', () => {
    expect(flights.state.flights).toEqual([]);
    expect(flights.state.loading).toBe(false);
  });
  it('Tests loading mutations', () => {
    const state = { loading: false };
    flights.mutations.onLoading(state);
    expect(state.loading).toBe(true);
    flights.mutations.offLoading(state);
    expect(state.loading).toBe(false);
    flights.mutations.toggleLoading(state);
    expect(state.loading).toBe(true);
    flights.mutations.toggleLoading(state);
    expect(state.loading).toBe(false);

  });
});
