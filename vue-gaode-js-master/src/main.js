import Vue from 'vue'
import App from './App.vue'
import router from '@/router';
import axios from 'axios'

Vue.config.productionTip = false
Vue.prototype.$axios = axios 

router.beforeEach((to,from,next) =>{
  if(to.meta.title){
    document.title = to.meta.title
  }
  next();
})

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
