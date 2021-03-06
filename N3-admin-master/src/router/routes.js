import Login from '../views/login'
import CommonLayout from '../layout'

import NormalForm from '../views/form'
import NormalTable from '../views/table'
import Home from '../views/home'

const routes = [
  {
    path: '/home',
    component: Home,
    name: 'home'
  },
  // Login View
  {
    path: '/login',
    component: Login,
    name: 'login'
  },
  {
    path: '*',
    redirect: '/home'
  }
]

export default routes
