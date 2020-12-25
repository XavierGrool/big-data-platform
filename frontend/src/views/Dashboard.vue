<template>
  <a-layout>
    <a-layout-header class="header">
      <p class="logo">大数据分析工具平台</p>
      <a-menu
        theme="dark"
        mode="horizontal"
        :default-selected-keys="['workspace']"
        :style="{ lineHeight: '64px' }"
      >
        <a-menu-item key="workspace" @click="clickWorkspace">
          工作台
        </a-menu-item>
        <a-menu-item key="help" @click="clickHelp">
          使用帮助
        </a-menu-item>
        <a-popover
          v-model="popover_visible"
          trigger="click"
          placement="bottomRight"
          @visibleChange="clickAvatar"
        >
          <a-card slot="content" :bordered="false">
            <a-card-meta :title="username" :description="user_role">
              <a-icon slot="avatar" type="smile" style="font-size: 42px;"/>
            </a-card-meta>
            <template slot="actions">
              <span @click="changePasswd"><a-icon key="edit" type="edit"/>修改密码</span>
              <span @click="logout"><a-icon key="logout" type="logout"/>登出</span>
            </template>
            <a-modal
              title="修改密码"
              :visible="modal_visible"
              :footer="null"
              @cancel="closeModal"
            >
              <a-form :form="form" :label-col="{ span: 5 }" :wrapper-col="{ span: 12 }" @submit="submitPasswd">
                <a-form-item label="原密码">
                  <a-input
                    v-decorator="['old_passwd', { rules: [{ required: true, message: '原密码不得为空!' }] }]"
                    type="password"
                  />
                </a-form-item>
                <a-form-item label="新密码">
                  <a-input
                    v-decorator="['new_passwd', { rules: [{ required: true, message: '新密码不得为空!' }] }]"
                    type="password"
                  />
                </a-form-item>
                <a-form-item label="确认密码">
                  <a-input
                    v-decorator="['confirm_passwd', { rules: [{ required: true, message: '两次输入不一致!' }] }]"
                    type="password"
                  />
                </a-form-item>
                <a-form-item :wrapper-col="{ span: 12, offset: 5 }">
                  <a-button type="primary" html-type="submit">
                    提交
                  </a-button>
                </a-form-item>
              </a-form>
            </a-modal>
          </a-card>
          <a-button class="avatar" type="primary" shape="circle" icon="user" />
        </a-popover>
      </a-menu>
    </a-layout-header>
    <router-view></router-view>
  </a-layout>
</template>

<script>
export default {
  name: "Dashboard",
  data() {
    return {
      form: this.$form.createForm(this, { name: 'coordinated' }),
      popover_visible: false,
      modal_visible: false,
      username: "null",
      user_role: "普通用户"
    };
  },
  methods: {
    // 点击 "工作台"
    clickWorkspace(e) {
      console.log(e.key);
      this.$router.push("/dashboard/workspace")
    },

    // 点击 "使用帮助"
    clickHelp(e) {
      console.log(e.key);
      this.$router.push("/dashboard/help")
    },
    
    // 点击用户头像
    clickAvatar(popover_visible) {
      if (popover_visible == true) {
        // 从 cookie 拿到 username 然后发给后端查询用户信息
        // 得到用户信息展示 username 及用户身份
        this.$axios({
          method: 'post',
          url: '/user/info/',
          data: {
            "username": this.$cookies.get("username")
          }
        }).then((response) => {
          console.log(response.data);
          // 先判断状态码，如果是 0 直接弹警告，如果是 1 则展示信息
          // username 直接展示
          // role 判断一下
          if (response.data.status == 0) {
            this.$message.error('用户不存在！');
          } else {
            this.username = response.data.username;
            if (response.data.role == 1) {
              this.user_role = "超级管理员";
            } else if (response.data.role == 2) {
              this.user_role = "普通用户";
            }
          }
        })
      }
    },

    // 登出
    logout() {
      this.$cookies.remove("username")
      this.$router.replace("/")
      this.$message.success('登出成功！');
    },

    // 修改密码
    changePasswd() {
      this.popover_visible = false;
      this.modal_visible = true;
    },

    // 关闭修改密码对话框
    closeModal() {
      this.modal_visible = false;
    },

    // 提交修改密码
    submitPasswd(e) {
      e.preventDefault();
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values);
          // 先判断一下两次密码一不一致
          // 如果如果不一致，弹警告
          // 一致的话，调用 /user/change-passwd 接口 (POST)
          // 发送 username, old_passwd, new_passwd
          // 其中 username 通过 cookie 获得
          if (values.new_passwd != values.confirm_passwd) {
            this.$message.error('两次密码输入不一致！');
          } else {
            this.$axios({
              method: 'post',
              url: '/user/change-passwd/',
              data: {
                "username": this.$cookies.get("username"),
                "old_passwd": values.old_passwd,
                "new_passwd": values.new_passwd
              }
            }).then((response) => {
              console.log(response.data)
              // 如果状态码 status 为 0，说明旧密码验证失败，弹警告
              // 如果 status 为 1，说明密码修改成功
              // 提示修改成功，清除现有 cookie 并跳转回登录页要求重新登录
              if (response.data.status == 0) {
                this.$message.error('原密码不正确！');
              } else if (response.data.status == 1) {
                this.$message.success('密码修改成功！');
                this.$cookies.remove("username");
                this.$router.replace("/")
              } else {
                this.$message.error('非法状态！');
              }
            })
          }
        }
      });
    },
  },
};
</script>

<style>
.logo {
  float: left;
  color: #FFFAFA;
  font-size:22px;
  padding-right: 48px;
}

.avatar {
  margin-top: 16px;
  float: right;
}
</style>
