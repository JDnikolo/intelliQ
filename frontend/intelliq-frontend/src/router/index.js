import { createRouter, createWebHistory } from 'vue-router'
import ResponderHome from '../views/ResponderHome.vue'
import ViewerHome from "../views/ViewerHome.vue"
import ResponderAnswer from "../views/ResponderAnswer.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: ResponderHome
    },
    {
      path: '/answer/:qID',
      name: 'Answer Questionnaire',
      props: true,
      component: ResponderAnswer
    },
    {
      path: '/viewer',
      name: 'Viewer Home',
      component: ViewerHome
    },
  ]
})

export default router
