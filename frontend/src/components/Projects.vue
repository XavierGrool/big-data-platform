<template>
<a-layout>
    <a-layout-sider width="200" style="background: #fff">
    <a-menu
        mode="inline"
        :default-selected-keys="['1']"
        :style="{ height: '100%', borderRight: 0 }"
    >
        <a-menu-item key="1" @click="clickProjects">
            <a-icon type="project" />项目空间
        </a-menu-item>
        <a-menu-item key="2" @click="clickUsers">
            <a-icon type="user" />用户管理
        </a-menu-item>
    </a-menu>
    </a-layout-sider>
    <a-layout style="padding: 0 24px 24px">
    <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>Home</a-breadcrumb-item>
        <a-breadcrumb-item>List</a-breadcrumb-item>
        <a-breadcrumb-item>App</a-breadcrumb-item>
    </a-breadcrumb>
    <a-layout-content
        :style="{ background: '#fff', padding: '24px', margin: 0, minHeight: '280px' }"
    >
        Content
    </a-layout-content>
    </a-layout>
</a-layout>
</template>

<script>
export default {
    name: "Projects",
    methods: {
        // 点击项目空间（其实没什么用
        clickProjects(e) {
            console.log(e);
        },

        // 点击用户管理
        clickUsers(e) {
            console.log(e);
            this.$router.push("/dashboard/workspace/users")
        },
    }
}
</script>
