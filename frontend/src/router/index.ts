import { createRouter, createWebHistory } from 'vue-router';
const MainPage = () => import('@/views/MainPage.vue'); 
const Login = () => import('@/views/Login.vue');       
const Signup = () => import('@/views/Signup.vue'); 
const Upload = () => import('@/views/Upload.vue'); 

const routes = [
  {
    path: '/',
    name: 'MainPage',
    component: MainPage,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup,
  },
  {
    path: '/upload',
    name: 'Upload',
    component: Upload,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
