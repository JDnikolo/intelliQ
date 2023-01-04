import { createRouter, createWebHistory } from 'vue-router'
import ResponderHome from '../views/ResponderHome.vue'
import ViewerHome from "../views/ViewerHome.vue"
import ResponderAnswer from "../views/ResponderAnswer.vue"
import ResponderQuestionnaires from "../views/ResponderQuestionnaires.vue"
import ViewerLogin from "../views/ViewerLogin.vue"
import ViewerEndpoints from "../views/ViewerEndpoints.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Intelliq Home',
      component: ResponderHome,
      children: [
        {
          path: '',
          name: 'Available Questionnaires',
          component: ResponderQuestionnaires
        },
        {
          path: 'answer/:qID',
          name: 'Answer Questionnaire',
          props: true,
          component: ResponderAnswer
        },
      ],
    },
    {
      path: '/viewer',
      name: 'Viewer Home',
      component: ViewerHome,
      children: [
        {
          path: '',
          name: 'Login',
          component: ViewerLogin
        },
        {
          path: 'endpoints',
          name: 'Viewer Endpoints',
          component: ViewerEndpoints
        }
      ],

    },
  ]
})

export default router
