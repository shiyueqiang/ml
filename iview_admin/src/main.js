import Vue from 'vue'
import axios from 'axios'
import iView from 'iview'
import VueRouter from 'vue-router'
import App from './app.vue'
import routes from './libs/route.js'
import components from './components'
import './libs/common.js'

Object.keys(components).forEach(key => {
    Vue.component(key, components[key])
})

Vue.filter('fullNumber', config.fullNumber)

Vue.use(VueRouter)
Vue.use(iView)
const router = new VueRouter({ routes })

document.setTitle = function(title) {
    document.title = title
}

Object.defineProperty(Vue.prototype, 'axios', { value: axios });
Object.defineProperty(Vue.prototype, '$format', {
    value(key) {
        if (key) {
            return JSON.parse(decodeURIComponent(this.$route.params[key]))
        } else {
            return {}
        }
    }
});

// 添加响应拦截器 
axios.interceptors.response.use(function(response) {
    if (response.data.code === '301') {
        location.href = '#/login'
    } else {
        if (response.data.code !== 200) {
            Toast.show(response.data.message)
        }
    }
    return response.data
}, function(err) {
    Promise.reject(err)
})
axios.defaults.transformRequest = [function(data) {
    var ret = []
    for (var it in data) {
        ret.push(encodeURIComponent(it) + '=' + encodeURIComponent(data[it]))
    }
    return ret.join('&')
}]
axios.defaults.responseType = 'json'
axios.defaults.withCredentials = true
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'


// 放在axios下面
window.Promise = Promise

window.Cookie = {
    read(name) {
        let value = document.cookie.match('(?:^|;)\\s*' + name + '=([^;]*)');
        return (value) ? decodeURIComponent(value[1]) : null;
    },
    write(value) {
        let str = value.name + '=' + encodeURIComponent(value.value);
        if (value.domain) {
            str += '; domain=' + value.domain;
        }
        if (value.path) {
            str += '; path=' + value.path;
        }
        if (value.day) {
            let time = new Date();
            time.setTime(time.getTime() + value.day * 24 * 60 * 60 * 1000);
            str += '; expires=' + time.toGMTString();
        }
        document.cookie = str;
    },
    dispose(name) {
        let str = this.read(name);
        this.write({
            name: name,
            value: str,
            day: -1
        });
    }
}


new Vue({
    el: '#main',
    router,
    render: h => h(App)
});

router.beforeEach((to, from, next) => {
    iView.LoadingBar.start();
    config.load = true
    next();
});

router.afterEach(route => {
    config.meta.parent = route.meta.parent
    config.meta.path = route.path
    if (config.meta.parent === '后台首页') {
        config.meta.breadcrumbName = config.meta.parent
        config.meta.breadcrumbIcon = 'logo-windows'
        config.meta.name = ''
    }
    let arr = ['金蛋理财-电销客服管理系统']
    if (route.meta.parent) {
        arr.unshift(route.meta.parent)
    }
    document.setTitle(arr.join(' - '))
    iView.LoadingBar.finish()
});
