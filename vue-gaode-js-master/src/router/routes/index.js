export const constantRoutes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/Home'),
    meta: {
      title: '地图找房'
    }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/Login'),
    meta: {
      title: '地图找房登录'
    }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/Register'),
    meta: {
      title: '地图找房注册'
    }
  },
  {
    path: '/favorites',
    name: 'favorite',
    component: () => import('@/views/Favorites'),
    meta: {
      title: '地图找房收藏夹'
    }
  }
];
