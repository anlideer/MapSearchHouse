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
      </div>
      <!--<button class="input-btn" @click="handleOk">搜索</button>-->
    </div>
    <div id="container"></div>
  </div>
</template>

<script>
import AMapLoader from '@amap/amap-jsapi-loader';
import Vue from 'vue/dist/vue.esm.js';

export default {
  name: 'Map',
  data() {
    return {
      map: null,
      marker: null,
      geocoder: null,
      autoComplete: null,
      address: '',
      infoWindow: null,
      arrivalRange: null,
      polygons: [],
      companyPosition: [],
      travelTime: 30,
      travelMethod: 0,
      allHouses: [],
      cluster: null,
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
          'AMap.PlaceSearch',
          'AMap.Scale',
          'AMap.Geocoder',
          'AMap.AutoComplete',
          'AMap.Marker',
          'AMap.InfoWindow',
          'AMap.Event',
          'AMap.Icon',
          'AMap.Polygon',
          'AMap.ArrivalRange',
          'AMap.MarkerCluster',

        ],  // 需要使用的的插件列表，如比例尺'AMap.Scale'等
    }).then((AMap)=>{
        var city="北京"
        this.map = new AMap.Map('container', {'zoom': 9});
        const toolbar = new AMap.ToolBar();
        const scale = new AMap.Scale();
        this.map.addControl(toolbar);
        this.map.addControl(scale);
        this.geocoder = new AMap.Geocoder({});
        this.marker = new AMap.Marker({});
        this.infoWindow = new AMap.InfoWindow({});
        this.arrivalRange = new AMap.ArrivalRange();
        this.AMap = AMap;
        const autoOptions = {
          //city 限定城市，默认全国
          city: city,
          input: 'input',
        }
        this.autoComplete = new AMap.AutoComplete(autoOptions);
        this.placeSearch = new AMap.PlaceSearch({
          city: city,
          //map: this.map // 因为要自定义窗口，所以自己来标记点以及写
        });
        this.autoComplete.on('select', this.select);

        this.showAllHouses();
    }).catch(e => {
        console.log(e);
    })

  },
  methods: {
    select(e){
        //console.log(e)
        this.placeSearch.setCity(e.poi.adcode);
        this.placeSearch.search(e.poi.name, this.search_callback);  //关键字查询查询
        this.map.clearMap();
    },

    showAllHouses(){
        // 从静态文件拿到所有房源
        console.log('fetching houses...');
        this.$axios.get('/json/houses.json').then(res => 
        {
          if (res.status == 200)
          {
            this.allHouses = res.data.split('||');
            console.log(this.allHouses);
            for (var i = 0; i < this.allHouses.length; i++){
              this.allHouses[i] = JSON.parse(this.allHouses[i]);
              this.allHouses[i]['lnglat'] = [this.allHouses[i]['longitude'], this.allHouses[i]['latitude']];
            }
            console.log('house json loaded');
          }
          else{
            console.log('failed to load house json.')
            console.log(res);
          }
        }).catch(function (error) { // 请求失败处理
          console.log('error');
          console.log(error);
        });
    },
    
    // 海量点标记
    addHouseCluster()
    {
      if (this.cluster != null){
        this.cluster.setMap(this.map);
      }
      if (this.allHouses == []){
        console.log('no house');
        return;
      }
      var sts = [{
                url: "//a.amap.com/jsapi_demos/static/images/blue.png",
                size: new this.AMap.Size(32, 32),
                offset: new this.AMap.Pixel(-16, -16)
            }, {
                url: "//a.amap.com/jsapi_demos/static/images/green.png",
                size: new this.AMap.Size(32, 32),
                offset: new this.AMap.Pixel(-16, -16)
            }, {
                url: "//a.amap.com/jsapi_demos/static/images/orange.png",
                size: new this.AMap.Size(36, 36),
                offset: new this.AMap.Pixel(-18, -18)
            }, {
                url: "//a.amap.com/jsapi_demos/static/images/red.png",
                size: new this.AMap.Size(48, 48),
                offset: new this.AMap.Pixel(-24, -24)
            }, {
                url: "//a.amap.com/jsapi_demos/static/images/darkRed.png",
                size: new this.AMap.Size(48, 48),
                offset: new this.AMap.Pixel(-24, -24)
            }];
      var gridSize = 60;
      this.cluster = new this.AMap.MarkerCluster(this.map, this.allHouses, {
          styles: sts,
          gridSize: gridSize,
          clusterByZoomChange: true,
      });

      this.cluster.on('click', this.showHouseDetail);

    },

    // 点击房源标记点后
    showHouseDetail(e)
    {
      //console.log(e);
      var chosenData = e.clusterData;
      if (chosenData.length > 1)
      {
        this.map.setZoomAndCenter(this.map.getZoom() + 1, e.lnglat, true);
      }
      else{
        // 显示信息窗体
        var singleData = chosenData[0];
        this.$axios({
            url: 'http://182.92.223.235:8888/getHouseList',
            method: 'post',
            data: {
              'locationName': singleData.location,
            }
        }).then(res=>{
          console.log(res.data);
          if (res.data['code'] != "200")
          {
            console.log('error' + res.data['message']);
          }
          else{
            var houseHtml = ''
            var houseList = res.data.data;
            for (var i = 0; i < houseList.length; i++){
              var h = houseList[i];
              var tmpStr = '<div>';
              tmpStr += '<a href=https://dt.lianjia.com/zufang/'+ h['link'].toString() + ' target="_blank">' + h['title'] + '</a>';
              tmpStr += '<br/><img src="' + h['photo'].toString()  +'" height="100"/>'
              tmpStr += '<div>价格：' + h['price'].toString() + '元/月</div>'
              tmpStr += '<div>' + h['rooms'] + ' 面积: ' + h['area'] + '</div>'
              tmpStr += '</div><br/>';
              houseHtml += tmpStr;
            }
            //let that = this;
            let InfoContent = Vue.extend({
              template: '<div> <div id="scrolltest" style="overflow:auto; height:300px; width: 300px;"> <div>' 
              + singleData.location  + '-' + singleData.houseNum + '房源</div><br/>'
              + houseHtml
              + '</div></div>',
              data() {
                return {

                };
              },
              methods: {
                // chooseThis(){
                //   console.log('choose this!');
                //   // 外面写个函数再把选定的这个东西的信息传给它
                //   that.chooseCompanyLocation(p);
                // },
              },
            });
            let component = new InfoContent().$mount();

            this.infoWindow = new this.AMap.InfoWindow({
              anchor: 'bottom-center',
              content: component.$el
            })
            this.infoWindow.open(this.map, singleData.lnglat); 

          }
          
          }).catch(function (error) { // 请求失败处理
            console.log('error');
            console.log(error);
          });
      }
    },

    // 搜索的回调
    search_callback(status, result)
    {
      if (status == "complete")
      {
        console.log(result);
        this.addPoints(result.poiList.pois);
      }
      else
      {
        console.log(result);
      }
    },

    // 添加可能的公司地点供选择
    addPoints(points)
    {
      this.map.clearMap();
      for (var i = 0; i < points.length; i++)
      {
        this.addOnePoint(points[i]);
      }
      this.map.setFitView();
    },

    // 上面那个功能的添加单点的功能
    addOnePoint(p)
    {
      var location = p.location;
      var pointMarker = new this.AMap.Marker({
        map: this.map,
        position: [location.lng, location.lat],
        anchor: 'bottom-center'
      });
      pointMarker.setExtData(p)

      pointMarker.on('click', this.showPointDetail);
    },

    showPointDetail(e)
    {
      //console.log(e.target.getExtData());
      var p = e.target.getExtData();
      let that = this;
      let InfoContent = Vue.extend({
        template: "<div><div>" + p.name +"</div><br/><div>" + p.address + "</div><br/><div>" + p.type +"</div><br/><button @click='chooseThis'>选定</button></div>",
        data() {
          return {
            content: p,
          };
        },
        methods: {
          chooseThis(){
            //console.log('choose this!');
            // 外面写个函数再把选定的这个东西的信息传给它
            that.chooseCompanyLocation(p);
          },
        },
      });
      let component = new InfoContent().$mount();

      this.infoWindow = new this.AMap.InfoWindow({
        anchor: 'bottom-center',
        content: component.$el
      })
      var location = p.location;
      this.infoWindow.open(this.map, [location.lng, location.lat]);
    },

    drawPolygons(status, result){
      //console.log(result);
      this.polygons = [];
      if(result.bounds){
        for(var i=0;i<result.bounds.length;i++){
           var polygon = new this.AMap.Polygon({
                fillColor:"#3366FF",
                fillOpacity:"0.4",
                strokeColor:"#00FF00",
                strokeOpacity:"0.5",
                strokeWeight:1
            });
            polygon.setPath(result.bounds[i]);
            this.polygons.push(polygon);
        }
        this.map.add(this.polygons);

        this.addHouseCluster();

        // var that = this;
        // // 从后端拿到所有在区域内的房源
        // this.$axios({
        //   url: 'http://182.92.223.235:8888/searchHouses',
        //   method: 'post',
        //   data: {
        //     bounds: result.bounds
        //   }
        // }).then(res => 
        // {
        //   if (res.data.code == 200){
        //     var houses = res.data.data;
        //     console.log(houses);
        //     that.showHousesSearch(houses); 
        //   }
        //   else{
        //     console.log(res.data);
        //   }
        // }).catch(function (error) { // 请求失败处理
        //   console.log('error');
        //   console.log(error);
        // });

      }

    },
    // // 显示检索得到的房源
    // showHousesSearch(houses)
    // {
    //   var points = [];
    //   for(var i = 0; i < houses.length; i++){
    //     var house = houses[i];
    //     var point = new this.AMap.Marker({
    //       map: this.map,
    //       position: [house.lnglat[0], house.lnglat[1]],
    //       title: house.location + '-' + house.number + '个房源',
    //       anchor: 'bottom-center',
    //     })
    //     // TODO: content defined

    //     points.push(point);
    //   }
    //   this.map.add(points);
    // },

    chooseCompanyLocation(p)
    {
      console.log(p);
      this.companyPosition = [p.location.lng, p.location.lat];
      if (this.infoWindow != null){
        this.infoWindow.close();
        this.infoWindow = null;
      }
      // 先把点给清除只剩选定的工作地点
      this.map.clearMap();    
      new this.AMap.Marker({
        map: this.map,
        position: [p.location.lng, p.location.lat],
        icon: '//vdata.amap.com/icons/b18/1/2.png',
        offset: new this.AMap.Pixel(-10, -10),
        anchor: 'center',
        //anchor: 'bottom-center',
      })

      // 公交到达圈，绘制多边形，然后筛选一下在范围内的房源
      this.arrivalRange.search(this.companyPosition, this.travelTime, this.drawPolygons,
        {
          policy: this.travelMethod
        }
      )

    },


  },
  
  watch: {
    address: function(){
      this.map.clearMap();
      if (this.cluster != null){
        this.cluster.setMap(null);
      }
    }
  }
};
</script>

<style lang='less' scoped>
.app-inner {
  text-align: center;
}

#container {
  margin: 30px auto;
  width: 1500px;
  height: 500px;;
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