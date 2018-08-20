<template lang="pug">
Row.page-home
    Col(span="24")
        div.logo  &#xe651;
        dl.desc
            dd 金蛋理财-电销客服管理系统
        p 欢迎您，{{user_info.admin_name}} {{user_info.admin_mobile}}
</template>
<style lang="less">
.page-home {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    color: #2d8cf0;
    dt {
        font-size: 18px
    }
    dd {
        font-size: 14px;
    }
    p {
        padding-top: 60px;
        color: #666
    }
    .logo {
        font-size: 40px;
        padding-bottom: 10px;
        font-family: iconfont
    }
}
</style>
<script>
export default {
    data() {
        return {
            config,
            user_info: config.user_info
        }
    }
}
</script>