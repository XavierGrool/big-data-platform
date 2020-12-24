<template>
  <div class="login">
    <h1 class="title">大数据分析工具平台</h1>
    <a-form
      :form="form"
      class="login-form"
      @submit="handleSubmit"
    >
      <a-form-item>
        <a-input
          v-decorator="[
            'userName',
            { rules: [{ required: true, message: 'Please input your username!' }] },
          ]"
          placeholder="Username"
        >
          <a-icon slot="prefix" type="user" style="color: rgba(0,0,0,.25)" />
        </a-input>
      </a-form-item>
      <a-form-item>
        <a-input
          v-decorator="[
            'password',
            { rules: [{ required: true, message: 'Please input your Password!' }] },
          ]"
          type="password"
          placeholder="Password"
        >
          <a-icon slot="prefix" type="lock" style="color: rgba(0,0,0,.25)" />
        </a-input>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit" class="login-form-button">
          Log in
        </a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
export default {
  name: 'Login',
  beforeCreate() {
    this.form = this.$form.createForm(this, { name: 'normal_login' });
    
    // 如果 cookie 已存在，证明已经登录，则直接进入 dashboard
    if (this.$cookies.get("username") != null) {
      this.$router.push("/dashboard")
    }
  },
  methods: {
    handleSubmit(e) {
      e.preventDefault();
      let _this = this;
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values);
          let username = values.userName;
          this.$axios({
            method: 'post',
            url: '/login/',
            data: {
              "username": values.userName,
              "password": values.password
            }
          }).then(function (response) {
            console.log(response.data)
            if (response.data.status == 0) {
              _this.$message.error('用户名不存在！');
            } else if (response.data.status == 1) {
              _this.$cookies.set("username", username);
              _this.$message.success('登录成功！');
              _this.$router.push("/dashboard")
            } else if (response.data.status == 2) {
              _this.$message.error('密码错误！');
            } else {
              _this.$message.error('非法状态！');
            }
          })
        }
      });
    },
  },
}
</script>

<style scoped>
.login {
  text-align: center;
}
.login .title {
  margin-top: 130px;
  margin-bottom: 50px;
}
.login-form {
  width: 400px;
  padding-top: 40px;
  padding-left: 30px;
  padding-right: 30px;
  padding-bottom: 20px;
  margin-left:auto;
  margin-right:auto;
  border-radius: 5px;
  box-shadow: 2px 4px 10px 4px rgb(211,211,211);
}
.login-form-forgot {
  float: right;
}
.login-form-button {
  width: 60%;
}
</style>
