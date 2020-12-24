import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false

// vue-router
import router from './router'

// axios
import axios from 'axios'
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
Vue.prototype.$axios = axios

// vue cookies
import VueCookies from 'vue-cookies'
Vue.use(VueCookies)
Vue.$cookies.config('30d')

// ant-design vue
import Antd from 'ant-design-vue';
import message from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
Vue.prototype.$message = message;
Vue.use(Antd)

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
