import { createApp } from 'vue'
import { createPinia, defineStore } from 'pinia'
import { useViewerStore } from './stores/viewerCreds.js'
import App from './App.vue'
import router from './router'

import './assets/main.css'
const pinia = createPinia()
//viewer credential store, used in viewer endpoint access
const app = createApp(App)

app.use(router)
app.use(pinia)
const viewerStore = useViewerStore()
app.mount('#app')
