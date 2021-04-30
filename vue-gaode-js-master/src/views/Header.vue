<template>
  <div class="app-header clearfix">
    <div class="logo-field">
      <router-link to='/'><img src="../assets/logo.png" class="logo"/> <span>地图找房</span></router-link>
    </div>
      <div class='corner' v-if="hasLogin"><router-link to='/favorites'><a-button>收藏夹</a-button></router-link></div>
      <div v-else class='corner'><router-link to='/login'><a-button>登录</a-button></router-link></div>
  </div>
</template>

<script>
import {bus} from '@/utils/bus.js';

  export default {
    data(){
      return{
        hasLogin: false
      }
    },
    methods: {
      updateCorner(){
        console.log('update corner');
        if (this.$global.username != null)
        {
          this.$set(this, 'hasLogin', true);
        }
        else
        {
          this.$set(this, 'hasLogin', false);
        }
      }
    },
    created(){
      bus.$on('login', this.updateCorner);
    }

  }
</script>

<style lang="less">
  .app-header {
    height: 60px;
    line-height: 60px;
    background: #fff;
    color: #c0ccda;
    display: flex;
    position: fixed;
    width:100%;
    z-index:3;
    box-shadow: 0px 0px 5px #f9f9f9;
    .fixed {
      position: absolute;
      top: 0px;
      bottom: 0px;
      width: 100%;
    }
    .logo-field {
      flex: 1;
      font-size: 26px;
    }
    .logo {
      width: 40px;
      float: left;
      margin: 10px 10px 10px 18px;
    }
    .corner {
      font-size: 20px;
      margin-right: 100px;
      color: #000000;
      cursor: pointer;
    }

  }
</style>