import Vue from 'vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'
import nwsMain from '@/components/nws-main'
import nwsNotFound from '@/components/nws-not-found/nws-not-found'

Vue.use(VueRouter) // Integrate the Vue-Router plugin
Vue.use(VueResource)

export default new VueRouter({
  mode: 'history',
  base: process.env.ROUTER_BASE,
  routes: [
    {
      path: '/',
      name: 'nws-main',
      component: nwsMain,
      // Inject  props based on route.query values (our query parameters!)
      props: (route) => ({
        url: route.query.url,
        engine: route.query.engine
      })
    },
    {
      path: '/index.html',
      name: 'nws-index',
      component: nwsMain,
      // Inject  props based on route.query values (our query parameters!)
      props: (route) => ({
        url: route.query.url,
        engine: route.query.engine
      })
    },
    {
      path: '*',
      name: '404',
      component: nwsNotFound
    }
  ]
})
