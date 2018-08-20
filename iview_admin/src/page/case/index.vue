<template lang="pug">
	<Table :columns="columns1" :data="data1"></Table>
</template>
<style lang="less">
@import '../../libs/mixin';
.page-case {
    
}
</style> 
<script>
export default {
    data() {
        return {
        	 columns1: [
                    {
                        title: 'Name',
                        key: 'name'
                    },
                    {
                        title: 'Age',
                        key: 'age'
                    },
                    {
                        title: 'Address',
                        key: 'address'
                    },
                    {
                        title: '模块',
                        key: 'date'
                    },
                    {
                        title: '版本号',
                        key: 'address'
                    },
                    {
                        title: '需求名称',
                        key: 'address'
                    },
                    {
                        title: '用例标题',
                        key: 'address'
                    },
                     {
                        title: '前置条件',
                        key: 'address'
                    },
                    {
                        title: '操作步骤',
                        key: 'address'
                    },
                    {
                        title: '期望结果',
                        key: 'address'
                    },
                    {
                        title: '负责人',
                        key: 'address'
                    },
                    {
                        title: '用例类型',
                        key: 'address'
                    },
                    {
                        title: '创建时间',
                        key: 'address'
                    },
                ],
                data1: [
                    {
                        name: 'John Brown',
                        age: 18,
                        address: 'New York No. 1 Lake Park',
                        date: '2016-10-03'
                    },
                    {
                        name: 'Jim Green',
                        age: 24,
                        address: 'London No. 1 Lake Park',
                        date: '2016-10-01'
                    },
                    {
                        name: 'Joe Black',
                        age: 30,
                        address: 'Sydney No. 1 Lake Park',
                        date: '2016-10-02'
                    },
                    {
                        name: 'Jon Snow',
                        age: 26,
                        address: 'Ottawa No. 2 Lake Park',
                        date: '2016-10-04'
                    }
                ]
            
        }
    },
    created() {
        
    }
};
</script>
</template>