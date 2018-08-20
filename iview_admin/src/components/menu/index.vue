<template lang="pug">
.v-side(:class="{'v-sideClose':close}")
    .switch(@click="switchSide")
        Icon(type="md-apps")
    .logo {{close ? "&#xe6cd;" :  "&#xe651;"}}
    .menu
        template(v-for="(item,index) in list")
            a.menuLink(:class="{current:meta.parent==item.name}", :href="item.link" v-if="item.link" @click="switchMenu(item.name)")
                Icon.typeIcon(:type="item.type")
                span.text {{item.name}}
            dl(:class="{current:meta.parent==item.name}" v-else)
                dt(@click="switchMenu(item.name)")
                    Icon.typeIcon(:type="item.type")
                    span.text {{item.name}}
                    i.arrow(:class="{current:meta.parent==item.name}")
                dd(:style="objStyle(item.name)")
                    div(:ref="item.name" v-if="item.children")
                        router-link(:to="_item.link" v-for="_item in item.children", :key="_item.id", :class="subClassName(_item,item.name,item.type)") {{_item.name}}
    .copyRight
        span.icon
            Icon(type="md-hammer")
        span(v-if="!close") 金蛋理财提供技术支持
</template>
<script>
export default {
    props: {
        value: {
            type: Boolean,
            default: false
        },
        // list:{
        //     type: Array,
        //     default(){
        //         return []
        //     }
        // }
    },
    data() {
        return {
            config,
            meta: config.meta,
            close: this.value,
            list: [{
                name: '电销主页',
                type: 'logo-windows',
                children: [{
                    name: '用户信息',
                    link: '/user/info'
                }, {
                    name: '操作记录',
                    link: '/user/info'
                }, {
                    name: '提交工单',
                    link: '/user/info'
                }, {
                    name: '联系记录',
                    link: '/user/info'
                }, {
                    name: '操作记录',
                    link: '/user/info'
                }, {
                    name: '工单记录',
                    link: '/user/info'
                }, ]
            }, {
                name: '实例首页',
                type: 'md-contacts',
                children: [{
                    name: '实例首页',
                    link: '/case/'
                }, {
                    name: '操作记录',
                    link: '/user/info'
                }, {
                    name: '提交工单',
                    link: '/user/info'
                }, {
                    name: '联系记录',
                    link: '/user/info'
                }, {
                    name: '操作记录',
                    link: '/user/info'
                }, {
                    name: '工单记录',
                    link: '/user/info'
                }]
            }, {
                name: '数据统计',
                type: 'ios-grid',
                children: [{
                    name: '分时段电销',
                    link: '/user/info'
                }, {
                    name: '客服工作量',
                    link: '/user/info'
                }, {
                    name: '电销工作量',
                    link: '/user/info'
                }, {
                    name: '电销业绩',
                    link: '/user/info'
                }, {
                    name: '公海用户',
                    link: '/user/info'
                }, {
                    name: '用户分类',
                    link: '/user/info'
                }]
            }, {
                name: '质检界面',
                type: 'md-medkit',
                children: [{
                    name: '质检评分',
                    link: '/user/info'
                }, {
                    name: '评分结果',
                    link: '/user/info'
                }, {
                    name: '质检详情',
                    link: '/user/info'
                }]
            }, {
                name: '电销监控',
                type: 'logo-snapchat',
                children: [{
                    name: '客服状态时长',
                    link: '/user/info'
                }, {
                    name: '电话呼叫明细',
                    link: '/user/info'
                }]
            }, {
                name: '权限设置',
                type: 'ios-flower',
                children: [{
                    name: '用户管理',
                    link: '/user/info'
                }, {
                    name: '结果设置',
                    link: '/user/info'
                }]
            }]
        }
    },
    methods: {
        objStyle(name) {
            if (this.close) return {}
            if (this.$refs[name]) {
                return {
                    height: `${this.meta.parent === name ? this.$refs[name][0].offsetHeight : 0}px`
                }
            } else {
                if (this.meta.parent === name) {
                    return { height: 'auto' }
                }
                return {

                }
            }

        },
        subClassName(_item, name, iconType) {
            if (_item.link === this.meta.path) {
                this.meta.name = _item.name
                this.meta.breadcrumbName = name
                this.meta.breadcrumbIcon = iconType
                return 'current'
            }
            return ''
        },
        switchMenu(name) {
            if (this.close) return
            if (this.meta.parent === name) {
                this.meta.parent = ''
            } else {
                this.meta.parent = name
            }
        },
        switchSide() {
            this.close = !this.close
        }
    },
    watch: {
        value() {
            this.colse = this.value
        },
        close() {

            // 处理由关闭状态到开启状态，子菜单不展示的问题
            let tmp = this.meta.parent
            this.meta.parent = ''
            setTimeout(() => {
                this.meta.parent = tmp
            }, 30)
            this.$emit('input', this.close)
        }
    }
}
</script>