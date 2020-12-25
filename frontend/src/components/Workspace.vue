<template>
<a-layout>
    <a-layout-sider width="200" style="background: #fff">
    <a-menu
        mode="inline"
        :default-selected-keys="['1']"
        :style="{ height: '100%', borderRight: 0 }"
    >
        <a-menu-item key="1">
        <a-icon type="user" />项目管理
        </a-menu-item>
        <a-menu-item key="2">
        <a-icon type="user" />option1
        </a-menu-item>
        <a-menu-item key="3">
        <a-icon type="user" />option1
        </a-menu-item>
        <a-menu-item key="4">
        <a-icon type="user" />option1
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
    name: "Worksapce"
}
</script>
