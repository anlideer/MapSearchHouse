export const constantRoutes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/Home'),
    meta: {
      title: '地图找房'
    }
  }
];
