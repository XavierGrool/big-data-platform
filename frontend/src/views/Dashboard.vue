<template>
  <a-layout id="components-layout-demo-top-side-2">
    <a-layout-header class="header">
      <div class="logo" />
      <a-menu
        theme="dark"
        mode="horizontal"
        :default-selected-keys="['2']"
        :style="{ lineHeight: '64px' }"
      >
        <a-menu-item key="1">
          nav 1
        </a-menu-item>
        <a-menu-item key="2">
          nav 2
        </a-menu-item>
        <a-menu-item key="3">
          nav 3
        </a-menu-item>
        <a-popover v-model="visible" trigger="click">
          <a-card slot="content" :bordered="false">
            <a-card-meta title="Username" description="Permission">
              <a-icon slot="avatar" type="smile" style="font-size: 42px;"/>
            </a-card-meta>
            <template slot="actions">
              <span @click="changePasswd"><a-icon key="edit" type="edit"/>修改密码</span>
              <span @click="logout"><a-icon key="logout" type="logout"/>登出</span>
            </template>
          </a-card>
          <a-button class="avatar" type="primary" shape="circle" icon="user" />
        </a-popover>
      </a-menu>
    </a-layout-header>
    <a-layout>
      <a-layout-sider width="200" style="background: #fff">
        <a-menu
          mode="inline"
          :default-selected-keys="['1']"
          :default-open-keys="['sub1']"
          :style="{ height: '100%', borderRight: 0 }"
        >
          <a-sub-menu key="sub1">
            <span slot="title"><a-icon type="user" />subnav 1</span>
            <a-menu-item key="1">
              option1
            </a-menu-item>
            <a-menu-item key="2">
              option2
            </a-menu-item>
            <a-menu-item key="3">
              option3
            </a-menu-item>
            <a-menu-item key="4">
              option4
            </a-menu-item>
          </a-sub-menu>
          <a-sub-menu key="sub2">
            <span slot="title"><a-icon type="laptop" />subnav 2</span>
            <a-menu-item key="5">
              option5
            </a-menu-item>
            <a-menu-item key="6">
              option6
            </a-menu-item>
            <a-menu-item key="7">
              option7
            </a-menu-item>
            <a-menu-item key="8">
              option8
            </a-menu-item>
          </a-sub-menu>
          <a-sub-menu key="sub3">
            <span slot="title"><a-icon type="notification" />subnav 3</span>
            <a-menu-item key="9">
              option9
            </a-menu-item>
            <a-menu-item key="10">
              option10
            </a-menu-item>
            <a-menu-item key="11">
              option11
            </a-menu-item>
            <a-menu-item key="12">
              option12
            </a-menu-item>
          </a-sub-menu>
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
  </a-layout>
</template>

<script>
export default {
  name: "Dashboard",
  data() {
    return {
      visible: false,
      collapsed: false,
    };
  },
  methods: {
    hide() {
      console.log(111);
      this.visible = false;
    },
    logout() {
      this.$cookies.remove("username")
      this.$router.push("/")
      this.$message.success('登出成功！');
    },
    changePasswd() {
      console.log("修改密码（未实现）");
      console.log("当前用户: " + this.$cookies.get("username"));
    }
  },
};
</script>

<style>
#components-layout-demo-top-side-2 .logo {
  width: 120px;
  height: 31px;
  background: rgba(255, 255, 255, 0.2);
  margin: 16px 28px 16px 0;
  float: left;
}

.avatar {
  margin-top: 16px;
  float: right;
}
</style>
