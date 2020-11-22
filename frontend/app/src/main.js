import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import '@mdi/font/css/materialdesignicons.css'
import '@babel/polyfill'
import * as cv2 from 'opencv.js'

Vue.config.productionTip = false
Vue.prototype.$cv2 = cv2

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
