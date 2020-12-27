<template>
<a-layout>
    <a-layout-content
        :style="{ margin: '24px 16px', padding: '24px', minHeight: '280px' }"
    >
        <mavon-editor
            :value="help_md"
            :subfield="false"
            :defaultOpen="'preview'"
            :toolbarsFlag="false"
            :editable="false"
            :scrollStyle="true"
            :ishljs="true"
        />
    </a-layout-content>
</a-layout>
</template>

<script>
export default {
    name: "Help",
    data(){
        return {
            help_md: ''
        }
    },
    beforeCreate() {
        this.$axios({
            method: 'get',
            url: '/help/',
        }).then((response) => {
            console.log(response.data)
            this.help_md = response.data.content;
        })
    },
}
</script>

<style scoped></style>
