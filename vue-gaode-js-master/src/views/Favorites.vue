<template>
    <div>
        <div v-if='no_star'> 收藏夹为空 </div>
        <div v-else>
            
        </div>
    </div>
</template>

<script>
export default {
    data(){
        return{
            star_list = [],
        }
    },
    methods: {

    },
    computed: {
        no_star(){
            return this.star_list.length == 0;
        }
    }
}
</script>

<style lang='less' scoped>

</style>