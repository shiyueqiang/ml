<template lang="pug">
.v-head
    Breadcrumb.breadcrumb
        BreadcrumbItem(v-show="meta.breadcrumbName")
            Icon(:type="meta.breadcrumbIcon")
            |  {{meta.breadcrumbName}}
        BreadcrumbItem(v-show="meta.name")  {{meta.name}}
    Dropdown(placement="bottom-end")
        a.userInfo(href="javascript:;")
            Avatar(size="small" shape="square" icon="md-person" style="margin-right:7px;background-color:#2d8cf0")
            Tag(type="border") {{userInfo.department_name}}
            | {{userInfo.admin_name}}
        DropdownMenu(slot="list")
            DropdownItem.dropdownItem
                Icon(type="ios-send")
                | 消息
            DropdownItem.dropdownItem
                Icon(type="md-settings")
                | 设置
            DropdownItem.dropdownItem(divided @click.native="logout")
                Icon(type="md-power")
                | 退出
</template>
<script>
export default {
    props: {
        userInfo: {
            type: Object,
            default () {
                return {}
            }
        }
    },
    data() {
        return {
            meta: config.meta
        }
    },
    methods: {
        logout() {
            axios.post('/index/signout')
                .then(el => {
                    location.reload()
                })
        }
    }
}
</script>