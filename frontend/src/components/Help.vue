<template>
<a-layout>
    <a-layout-content style="padding: 0 50px">
        <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>Home</a-breadcrumb-item>
        <a-breadcrumb-item>List</a-breadcrumb-item>
        <a-breadcrumb-item>App</a-breadcrumb-item>
        </a-breadcrumb>
        <div :style="{ background: '#fff', padding: '24px', minHeight: '280px' }">
        Content
        </div>
    </a-layout-content>
</a-layout>
</template>

<script>
export default {
    name: "Help"
}
</script>
