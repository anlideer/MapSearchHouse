<template>
  <div class='app-inner'>
    <div class="input-wrap">
      <div class="input-box">
        <input
          id="input"
          class="input-text"
          placeholder="输入公司地址"
          v-model="address"
        />
        <div class="input-result__list" v-if="showSelect && resultList.length">
          <div
            class="input-result__item"
            v-for="item in resultList"
            :key="item.name"
            @click="selectedHandle(item.name)">
            {{item.name}}
          </div>
        </div>
      </div>
      <!--<button class="input-btn" @click="handleOk">搜索</button>-->
    </div>
    <div id="container"></div>
  </div>
</template>

<script>
import AMapLoader from '@amap/amap-jsapi-loader';

export default {
  name: 'Map',
  data() {
    return {
      map: null,
      marker: null,
      geocoder: null,
      autoComplete: null,
      address: '',
      lnglat: null,
      showSelect: false,
      resultList: [],
    };
  },
  computed: {

  },
  created() {},
  mounted () {
    AMapLoader.load({
        "key": "2b2fa2dca30400a380445eb87ce96229",   // 申请好的Web端开发者Key，首次调用 load 时必填
        "version": "2.0",   // 指定要加载的 JSAPI 的版本，缺省时默认为 1.4.15
        "plugins": [
          'AMap.ToolBar',
          'AMap.Geocoder',
          'AMap.PlaceSearch',
          'AMap.Scale',
          'AMap.Geocoder',
          'AMap.AutoComplete',
          'AMap.Marker'
        ],  // 需要使用的的插件列表，如比例尺'AMap.Scale'等
    }).then((AMap)=>{
        var city="北京"
        this.map = new AMap.Map('container', {'zoom': 9});
        const toolbar = new AMap.ToolBar();
        const scale = new AMap.Scale();
        this.map.addControl(toolbar);
        this.map.addControl(scale);
        this.geocoder = new AMap.Geocoder({});
        this.marker = new AMap.Marker();
        const autoOptions = {
          //city 限定城市，默认全国
          city: city,
          input: 'input',
        }
        this.autoComplete = new AMap.AutoComplete(autoOptions);
        this.placeSearch = new AMap.PlaceSearch({
          city: city,
          map: this.map
        });
        this.autoComplete.on('select', this.select)
    }).catch(e => {
        console.log(e)
    })

  },
  methods: {
    select(e){
      console.log(e)
        this.placeSearch.setCity(e.poi.adcode);
        this.placeSearch.search(e.poi.name);  //关键字查询查询
    },
  },
};
</script>

<style lang='less' scoped>
.app-inner {
  text-align: center;
}

#container {
  margin: 30px auto;
  width: 750px;
  height: 300px;;
}

.input {
  &-wrap {
    margin: 20px 0;
  }

  &-box {
    position: relative;
    display: inline-block;
  }

  &-text {
    width: 300px;
    height: 30px;
  }

  &-btn {
    padding: 0 10px;
    height: 36px;
  }

  &-result {

    &__list {
      padding-bottom: 10px;
      position: absolute;
      top: 30px;
      left: 0;
      z-index: 99;
      width: 100%;
      background-color: #fff;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    &__item {
      padding: 0 10px;
      width: 100%;
      line-height: 30px;
      text-align: left;
      border-bottom: 1px solid #eee;

      &:last-child {
        border-bottom: 0;
      }
    }
  }
}

.map-img {
  margin: 0 0 30px;
}
</style>
