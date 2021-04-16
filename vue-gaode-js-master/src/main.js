import Vue from 'vue'
import App from './App.vue'
import router from '@/router';
import axios from 'axios'
import Button from 'ant-design-vue/lib/button';
import Form from  'ant-design-vue/lib/form';
import Input from 'ant-design-vue/lib/input';
import Icon from 'ant-design-vue/lib/icon';
import 'ant-design-vue/dist/antd.css';

Vue.component(Button.name, Button);
Vue.component(Form.name, Form);
Vue.component(Form.Item.name, Form.Item);
Vue.component(Input.name, Input);
Vue.component(Icon.name, Icon);


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
