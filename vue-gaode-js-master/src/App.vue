<template>
  <div id="app">
    <AppHeader></AppHeader>
    <router-view></router-view>
  </div>
  
</template>

<script>
import AppHeader from './views/Header'

export default {
  name: 'App',
  components: {
    AppHeader
  }
}
</script>

<style lang="less" scoped>

</style>

