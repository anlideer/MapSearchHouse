import Vue from 'vue'
import App from './App.vue'
import router from '@/router';
import axios from 'axios';
// import Message from 'vue-message';
// import {Message}from 'element-ui'

import Button from 'ant-design-vue/lib/button';
import Form from  'ant-design-vue/lib/form';
import Input from 'ant-design-vue/lib/input';
import Icon from 'ant-design-vue/lib/icon';
import DropDown from 'ant-design-vue/lib/dropdown';
import Menu from 'ant-design-vue/lib/menu';
import InputNumber from 'ant-design-vue/lib/input-number';
import Message from 'ant-design-vue/lib/message';
import 'ant-design-vue/dist/antd.css';
import md5 from 'js-md5';

import Global from '@/utils/Global';

Vue.component(Button.name, Button);
Vue.component(Form.name, Form);
Vue.component(Form.Item.name, Form.Item);
Vue.component(Input.name, Input);
Vue.component(Icon.name, Icon);
Vue.component(DropDown.name, DropDown);
Vue.component(Menu.name, Menu);
Vue.component(Menu.Item.name, Menu.Item);
Vue.component(InputNumber.name, InputNumber);
// Vue.component(Message.name, Message);

// Vue.prototype.$message = Message
Vue.config.productionTip = false;
Vue.prototype.$axios = axios;
Vue.prototype.$md5 = md5;
Vue.prototype.$message = Message;
Vue.prototype.$global = Global;


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
