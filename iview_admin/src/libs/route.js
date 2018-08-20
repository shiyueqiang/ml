export default [{
    path: '/login',
    component: resolve => require(['../page/login/index.vue'], resolve)
}, {
    path: '/',
    component: resolve => require(['../page/index/index.vue'], resolve),
    children: [{
        path: '/',
        meta: {
            parent: '后台首页'
        },
        component: resolve => require(['../page/index/home.vue'], resolve)
    },{
        path: '/case',
        meta: {
            parent: '实例首页'
        },
        component: resolve => require(['../page/case/index.vue'], resolve)
    },{
        path: '/case/detail',
        meta: {
            parent: '实例'
        },
        component: resolve => require(['../page/case/detail.vue'], resolve)
    }]
}];