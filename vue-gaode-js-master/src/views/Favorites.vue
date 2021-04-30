<template>
    <div>
        <meta name="referrer" content="no-referrer" />
        <br/><br/>
        <div> 已失效房源将不予显示 </div>
        <div v-if='no_star'> 收藏夹为空 </div>
        <div v-else class='slist'>
            <a-list item-layout="vertical" :data-source="star_list">
                <a-list-item slot="renderItem" slot-scope="item">
                  <a-list-item-meta :description="item.description"
                  >
                <a slot="title" :href="item.link">{{ item.title }}</a>
                </a-list-item-meta>
                <img width="200" :src="item.photo" />
                <a-button slot='extra' class='unstar-button' @click="unstar(item.raw_link)">取消收藏</a-button>
                </a-list-item>
            </a-list>
        </div>
    </div>
</template>

<script>
export default {
    data(){
        return{
            star_list: [],
        }
    },
    methods: {
        fetchStars(){
            this.$axios({
                url: 'http://182.92.223.235:8888/getStars',
                method: 'post',
                data: {
                    username: this.$global.username,
                    password: this.$global.password
                }
            }).then(res => {
                console.log(res.data);
                if (res.data['code'] == 200)
                {
                    this.$set(this, 'star_list', res.data.stars);
                }
                else{
                    this.$message.error('登录状态失效');
                }
            })
        },
        unstar(link){
            this.$axios({
                url: 'http://182.92.223.235:8888/removeStar',
                method: 'post',
                data: {
                    username: this.$global.username,
                    password: this.$global.password,
                    link: link
                }
            }).then(res => {
                console.log(res.data);
                if (res.data['code'] == 200)
                {
                    this.$message.success('移除成功');
                    var tmp = []
                    for (var i = 0; i < this.star_list.length; i++)
                    {
                        if (this.star_list[i]['raw_link'] == link)
                        {
                            continue;
                        }
                        tmp.push(this.star_list[i]);
                    }
                    this.$set(this, 'star_list', tmp);
                }
                else{
                    this.$message.warning('登录失效或其他错误');
                }
            })
        },
    },
    created(){
        this.fetchStars();
    },
    computed: {
        no_star(){
            return this.star_list.length == 0;
        }
    }
}
</script>

<style lang='less' scoped>
.slist {
    margin-left: 50px;
    margin-right: 50px;
}

.unstar-button {
    margin-top: 80px;
    margin-right: 50px;
}
</style>