<template>
<a-layout style="padding: 0 24px 24px">
    <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>Workspace</a-breadcrumb-item>
        <a-breadcrumb-item>Projects</a-breadcrumb-item>
        <a-breadcrumb-item>{{ project_name }}</a-breadcrumb-item>
        <a-breadcrumb-item>Model</a-breadcrumb-item>
    </a-breadcrumb>
    <a-layout-content
        :style="{ background: '#fff', padding: '24px', margin: 0, minHeight: '280px' }"
    >
        Content
    </a-layout-content>
</a-layout>
</template>

<script>
export default {
    name: "Model",
    data() {
        return {
            project_name: "",
        }
    },
    beforeCreate() {
        console.log(this.$route.params.project_id)
        this.$axios({
            method: 'post',
            url: '/project/get-name/',
            data: {
                "id": Number(this.$route.params.project_id)
            }
        }).then((response) => {
            console.log(response.data);
            this.project_name = response.data.name;
        })
    }
}
</script>
