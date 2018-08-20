<template lang="pug">
.v-main(:class="{center:width>0 }", :style="objStyle")
    slot
    slot(name="extra")
</template>
<script>
export default {
    props: {
        title: {
            type: String,
            default: ''
        },
        width: {
            type: [Number, String],
            default: 0
        }
    },
    computed: {
        objStyle() {
            return {
                width: `${this.width}px`
            }
        }
    }
};
</script>