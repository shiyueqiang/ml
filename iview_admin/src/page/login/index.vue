<style lang="less">
.page-login {
    background: rgb(59, 78, 128) url('http://ued.fengtangkeji.com/CMS/assets/Group.png');
    height: 100vh;
    background-size: cover;
    position: fixed;
    left: 0;
    top: 0;
    right: 0;
    z-index: 100;
    .logo {
        color: #fff;
        text-align: center;
        font-size: 40px;
        margin-bottom: 10px;
        font-family: 'iconfont'
    }
    .loginBox {
        width: 300px;
        position: absolute;
        left: 50%;
        top: 40%;
        transform: translate(-50%, -50%);
    }
}
</style>
<template lang="pug">
.page-login
    .loginBox
        .logo &#xe651;
        Form(:model="formItem")
            FormItem
                Input(size="large" v-model="formItem.admin_mobile" placeholder="用户名")
                    Icon(type="person" slot="prepend")
            FormItem
                Input(size="large" v-model="formItem.admin_pwd" placeholder="密码" type="password")
                    Icon(type="locked" slot="prepend")
            FormItem
                Button(size="large" type="primary" @click="login" long) 登录
</template>
<script>
export default {
    data() {
        return {
            random: Math.random(),
            formItem: {
                admin_mobile: '',
                admin_pwd: '',
                code: 'aaaaa'
            },
            config
        }
    },
    methods: {
        login() {
            axios.post('login/do_login', this.formItem)
                .then(result => {
                    if (result.code === 0) {
                        let redirectUrl = sessionStorage.redirectUrl
                        if (redirectUrl) {
                            sessionStorage.removeItem('redirectUrl')
                        } else {
                            redirectUrl = location.href.split('#')[0]
                        }
                        location.href = redirectUrl
                    }
                })
        }
    }
}
</script>