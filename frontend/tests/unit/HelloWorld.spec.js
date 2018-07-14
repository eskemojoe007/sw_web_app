import { shallowMount, createLocalVue, mount } from '@vue/test-utils';
// import { mount } from '@vue/test-utils';
// eslint-disable-next-line import/no-unresolved
import HelloWorld from '@/components/HelloWorld.vue';
import Vuetify from 'vuetify';

describe('HelloWorld.vue', () => {
  let localVue;
  let wrapper;
  beforeAll(() => {
    localVue = createLocalVue();
    localVue.use(Vuetify, {});
    wrapper = mount(HelloWorld, { localVue });
  });

  it('renders props.msg when passed', () => {
    const msg = 'new message';
    wrapper.setProps({ msg });
    expect(wrapper.html()).toBe(msg);
    expect(wrapper.props().msg).toBe(msg);
  });


  it('render props.author when passed', () => {
    const msg = 'new message';

    wrapper.setProps({ author: msg });
    expect(wrapper.html()).toMatch(msg);
    expect(wrapper.props().author).toBe(msg);
  });
});

// describe('description', () => {
//   it('render props.authoer when passed', () => {
//     const msg = 'new message';
//     const wrapper = shallowMount(HelloWorld, {
//       propsData: {
//         author: msg,
//       },
//     });
//     expect(wrapper.text()).toMatch(msg);
//   });
// });
