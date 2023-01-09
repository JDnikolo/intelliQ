import { createRouter, createWebHistory } from 'vue-router'
import ResponderHome from '../views/ResponderHome.vue'
import ViewerHome from "../views/ViewerHome.vue"
import ResponderAnswer from "../views/ResponderAnswer.vue"
import ResponderQuestionnaires from "../views/ResponderQuestionnaires.vue"
import ViewerLogin from "../views/ViewerLogin.vue"
import ViewerEndpoints from "../views/ViewerEndpoints.vue"
import ViewerGetsession from "../views/ViewerGetsession.vue"
import ViewerGetquestion from "../views/ViewerGetquestion.vue"
import ViewerGetall from "../views/ViewerGetall.vue"
import AdminHome from "../views/AdminHome.vue"
import AdminLogin from "../views/AdminLogin.vue"
import AdminEndpoints from "../views/AdminEndpoints.vue"
import AdminResetq from "../views/AdminResetq.vue"

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
          name: 'vLogin',
          component: ViewerLogin
        },
        {
          path: 'endpoints',
          name: 'Viewer Endpoints',
          component: ViewerEndpoints,
		  children: [
			  {
				path: 'getsessionanswers/:qnrID',
				name: 'Session Answers',
				props: true,
				component: ViewerGetsession
			  },
			  {
				path: 'getquestionanswers/:qnrID',
				name: 'Question Answers',
				props: true,
				component: ViewerGetquestion
			  },
			  {
				path: 'getallanswers/:qnrID',
				name: 'All Answers',
				props: true,
				component: ViewerGetall
			  },
					]
		  
        }
      ],

    },
	{
      path: '/admin',
      name: 'Admin Home',
      component: AdminHome,
      children: [
        {
          path: '',
          name: 'Login',
          component: AdminLogin
        },
        {
          path: 'endpoints',
          name: 'Admin Endpoints',
          component: AdminEndpoints,
		  children: [
			  {
				path: 'resetq/:qnrID',
				name: 'AdminResetq',
				props: true,
				component: AdminResetq
			  },
					]
		  
        }
      ],

    },
  ]
})

export default router
