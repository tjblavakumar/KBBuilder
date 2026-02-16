import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CreateKBView from '../views/CreateKBView.vue'
import ChatView from '../views/ChatView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/create',
      name: 'create',
      component: CreateKBView
    },
    {
      path: '/chat/:id',
      name: 'chat',
      component: ChatView
    }
  ]
})

export default router
