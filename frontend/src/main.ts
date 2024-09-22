import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia';
import './assets/index.css'
import router from './router'; // Import the router
const pinia = createPinia();

createApp(App).use(router).use(pinia).mount('#app');
