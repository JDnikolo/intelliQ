# intelliq Frontend
The frontend server is implemented using Vue.js, a component-based JavaScript web user interface framework. Routing is handled using [Vue Router](https://router.vuejs.org/), and authentication retention is handled using [Pinia](https://pinia.vuejs.org/) stores. HTTPS is implemented using a [mkcert](https://github.com/FiloSottile/mkcert) locally-trusted development certificate.

### **Routing:**
Routing is done using Vue Router, through a combonation of pages and nested router views. The page hierarchy can be found in `intelliq-frontend/src/router`.
### **Views:**
The Vue templates can be found in `intelliq-frontend/src/views`, and are split into two categories:
#### **Responder templates**  
Used for responding browsing and filling out questionnaires. These include:
* [ResponderHome.Vue](https://github.com/ntua/SoftEng22-12/blob/main/frontend/intelliq-frontend/src/views/ResponderHome.vue): router-view housing template for other Responder templates.
* [ResponderQuestionnaires.vue](https://github.com/ntua/SoftEng22-12/blob/main/frontend/intelliq-frontend/src/views/ResponderQuestionnaires.vue): An overview of available questionnaires to be answered.
* [ResponderAnswer.vue](https://github.com/ntua/SoftEng22-12/blob/main/frontend/intelliq-frontend/src/views/ResponderAnswer.vue): Questionnaire answering template. Implements random sessionID creation, collection of answers and transmission of answers to the API.
#### **Viewer Templates**
Used for browsing questionnaire results and user authentication. These include:
* [ViewerHome.vue](https://github.com/ntua/SoftEng22-12/blob/main/frontend/intelliq-frontend/src/views/ViewerHome.vue): router-view housing template for other Viewer templates.
* [ViewerLogin.vue](https://github.com/ntua/SoftEng22-12/blob/main/frontend/intelliq-frontend/src/views/ViewerLogin.vue): Login page, handles user authentication before granting access to questionnaire results. 
* [ViewerEndpoints.vue](https://github.com/ntua/SoftEng22-12/blob/main/frontend/intelliq-frontend/src/views/ViewerEndpoints.vue): Base component for result browsing. Contains all available questionnaires and a router-view to components for viewing all results or results by session/question. Redirects to ViewerLogin.vue if any request returns an 401-unauthorized response.
* [ViewerGetall.vue](https://github.com/ntua/SoftEng22-12/blob/main/frontend/intelliq-frontend/src/views/ViewerGetall.vue): handles fetching all answers over all sessions for selected questionnaire.
* [ViewerGetquestion.vue](https://github.com/ntua/SoftEng22-12/blob/main/frontend/intelliq-frontend/src/views/ViewerGetquestion.vue): handles fetching all answers for a single question of the selected questionnaire.
* [ViewerGetsession.vue](https://github.com/ntua/SoftEng22-12/blob/main/frontend/intelliq-frontend/src/views/ViewerGetsession.vue): handles fetching all answers of a single session for the selected questionnaire.  

*Note that retrieval of available questionnaires from server is done via a frontend-only endpoint of the API, since it was impossible to fetch this data using only the endpoints described in the API specification document.* 