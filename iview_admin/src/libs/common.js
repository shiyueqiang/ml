import axios from 'axios'
import 'iview/src/styles/index.less'
import './common.less'

let getParams = () => {
    let url = location.search || location.href;
    let g = {};
    if (url.indexOf('?') !== -1) {
        let str = url.split('?')[1]
        let arr = str.indexOf('&') !== -1 ? str.split('&') : [str];
        for (let i = 0; i < arr.length; i++) {
            let tmp = arr[i].split('=');
            g[tmp[0]] = decodeURI(tmp[1]);
        }
    }
    return g;
}

Date.prototype.format = function(format) {
    let o = {
        'M+': this.getMonth() + 1,
        'd+': this.getDate(),
        'h+': this.getHours(),
        'm+': this.getMinutes(),
        's+': this.getSeconds(),
        'q+': Math.floor((this.getMonth() + 3) / 3),
        'S': this.getMilliseconds()
    }
    if (/(y+)/.test(format)) {
        format = format.replace(RegExp.$1, (this.getFullYear() + '').substr(4 - RegExp.$1.length));
    }
    for (let k in o) {
        if (new RegExp('(' + k + ')').test(format)) {
            format = format.replace(RegExp.$1, RegExp.$1.length === 1 ? o[k] : ('00' + o[k]).substr(('' + o[k]).length));
        }
    }
    return format;
}
axios.defaults.transformRequest = [function(data) {
    let ret = []
    for (let it in data) {
        ret.push(encodeURIComponent(it) + '=' + encodeURIComponent(data[it]))
    }
    return ret.join('&')
}]

axios.defaults.responseType = 'json'
axios.defaults.baseURL = '/index/'

Number.prototype.cutFixed = function(n) {
    let t = this.toString().split('.')
    let s = '000000000000000'
    if (n) {
        if (/\./.test(this)) {
            return [t[0], (t[1] + s).substr(0, n)].join('.')
        } else {
            return [this, s.substr(0, n)].join('.')
        }
    } else {
        return this
    }
}

String.prototype.cutFixed = function(n) {
    let _this = parseInt(this)
    return _this ? _this.cutFixed(n) : (0).cutFixed(n)
}

window.config = {
    meta: {
        parent: '',
        path: '',
        name: '',
        breadcrumbName: '',
        breadcrumbIcon: ''
    },
    user_info: {
        admin_name: '',
        department_name: '',
        post_name: ''
    },
    timer: null,
    params: getParams(),
    load: false
}

window.axios = axios