import Vue from 'vue';
import Vuex from 'vuex';
import images from './modules/images'

Vue.use(Vuex);
export default new Vuex.Store({
  modules: {
    images
  },
});
