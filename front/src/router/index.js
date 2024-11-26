import MainPageView from '@/views/MainPageView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import ProfileView from '@/views/ProfileView.vue'
import ProductListView from '@/views/ProductListView.vue'
import ExchangeRateView from '@/views/ExchangeRateView.vue'
import MapView from '@/views/MapView.vue'
import SurveyView from '@/views/SurveyView.vue'
import RecommendView from '@/views/RecommendView.vue'

import { createRouter, createWebHistory } from 'vue-router'
import ProductDetailView from '@/views/ProductDetailView.vue'
import UpdateUserInfo from '@/views/UpdateUserInfo.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'mainpage',
      component: MainPageView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
    },
    {
      path: '/login',
      name: 'login',
      component: LogInView,
    },
    {
      path: '/upate',
      name: 'update',
      component: UpdateUserInfo
    },
    {
      path: '/profile/:userId',
      name: 'profile',
      component: ProfileView,
      props: true,
    },
    {
      path: '/productlist',
      name: 'productlist',
      component: ProductListView,
    },
    {
      path: '/exchangerate',
      name: 'exchangerate',
      component: ExchangeRateView,
    },
    {
      path: '/map',
      name: 'map',
      component: MapView,
    },
    {
      path: '/survey',
      name: 'survey',
      component: SurveyView,
    },
    {
      path: '/recommend/:userSurveyId',
      name: 'recommend',
      component: RecommendView,
    },
    {
      path: '/productdetail/:productId',
      name: 'productdetail',
      component: ProductDetailView,
    },
  ],
})

export default router
