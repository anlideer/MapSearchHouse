// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'es6-shim'

import Vue from 'vue'
import N3 from 'N3-components'
import 'N3-components/dist/index.min.css'
import axios from './utils/axios'
import extend from './extend'
import VueAMap from 'vue-amap';

Vue.use(axios)
Vue.use(extend)
Vue.use(N3)
Vue.use(VueAMap);
VueAMap.initAMapApiLoader({
  key: '2b2fa2dca30400a380445eb87ce96229',
  plugin: ['AMap.Autocomplete', 'AMap.PlaceSearch', 'AMap.Scale', 'AMap.OverView', 'AMap.ToolBar', 'AMap.MapType', 'AMap.PolyEditor', 'AMap.CircleEditor'],
  // 默认高德 sdk 版本为 1.4.4
  v: '2.0'
});

import App from './App'
import router from './router'
import store from './store'
import './assets/styles/base.css'

/* eslint-disable */
new Vue({
  el: '#app',
  template: '<App />',
  components: { App },
  router,
  store
})
/* eslint-enable */
