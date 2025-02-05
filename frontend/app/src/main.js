import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import '@mdi/font/css/materialdesignicons.css'
import '@babel/polyfill'
import * as cv2 from 'opencv.js'
import store from './store'
import * as utils from './utils/helper'
import router from './router'
import '@/assets/css/main.css';
import '@/assets/css/variables.css';
Vue.config.productionTip = false
Vue.prototype.$cv2 = cv2
Vue.prototype.$utils = utils


new Vue({
  vuetify,
  store,
  router,
  render: h => h(App)
}).$mount('#app')
