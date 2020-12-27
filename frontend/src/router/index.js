import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Workspace from '../components/Workspace.vue'
import Projects from '../components/Projects.vue'
import Users from '../components/Users.vue'
import Project from '../components/Project.vue'
import Help from '../components/Help.vue'
import Dataset from '../components/Dataset.vue'
import Model from '../components/Model.vue'
import Prediction from '../components/Prediction.vue'
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
        component: Workspace,
        children: [
          {
            path: 'projects',
            component: Projects
          },
          {
            path: 'users',
            component: Users
          },
          {
            path: 'project/:id',
            component: Project,
            children: [
              {
                path: 'dataset',
                component: Dataset
              },
              {
                path: 'model',
                component: Model
              },
              {
                path: 'prediction',
                component: Prediction
              },
            ]
          }
        ]
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
