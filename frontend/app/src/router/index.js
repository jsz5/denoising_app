import Vue from 'vue'
import VueRouter from 'vue-router'
import Images from '@/components/images'

Vue.use(VueRouter)
export default new VueRouter({
  routes: [
    {
      path: '/',
      name: 'Images',
      component: Images
    }
  ]
})