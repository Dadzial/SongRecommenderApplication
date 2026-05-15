import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router/Index.ts'
import './style.css'

createApp(App).use(router).mount('#app')