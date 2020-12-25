import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Workspace from '../components/Workspace.vue'
import Help from '../components/Help.vue'
// import Test from '../views/Test.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Login
  },
  {
    path: '/dashboard',
    component: Dashboard,
    children: [
      {
        path: 'workspace',
        component: Workspace
      },
      {
        path: 'help',
        component: Help
      }
    ]
  },
]

const router = new VueRouter({
  routes
})

export default router
