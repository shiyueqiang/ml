<template lang="pug">
div.page-index
    MenuList(v-model='close', :list="menu_list")
    .framework(:class="{frameworkClose: close}")
        Head(:userInfo="user_info")
        router-view
</template>
<style lang="less">
@import '../../libs/mixin';
.page-index {
    min-width: 1200px;
    width: 100%;
    min-height: 100vh;
    position: relative;
    &:after {
        content: ' ';
        display: block;
        clear: both;
        height: 1px;
    }
    .framework {
        position: relative;
        margin-left: 64px;
        margin-left: 16.666666%;
        min-height: 95vh;
    }
    .frameworkClose {
        margin-left: 64px;
    }
}
</style>
<script>
export default {
    data() {
        return {
            user_info: config.user_info,
            close: localStorage.menuStatus === 'true' || false,
            menu_list: []
        }
    },
    created() {
        this.user_info = {
            admin_name: '郝学亮',
            department_name: '客服经理',
            post_name: '啊啊啊啊'
        }

        // axios.post('index/get_user_info')
        //     .then(result => {
        //         if (result.code == 0) {
        //             this.user_info = result.data.user_info
        //             config.user_info.admin_name = this.user_info.admin_name
        //             config.user_info.department_name = this.user_info.department_name
        //             config.user_info.post_name = this.user_info.post_name
        //             this.menu_list = result.data.user_info.menu_list
        //             this.menu_list.unshift({
        //                 name: '后台首页',
        //                 type: 'home',
        //                 link: location.href.split('#')[0],
        //             })
        //         }
        //     })
    },
    watch: {
        close() {
            localStorage.menuStatus = this.close
        }
    }
};
</script>
</template>