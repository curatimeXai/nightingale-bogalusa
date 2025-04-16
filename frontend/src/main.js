import { createApp } from 'vue'
import App from './App.vue'
import router from './router'; // Correct import of router

const app = createApp(App);

// If you're using any plugins like FloatingVue, you can use them here:
// app.use(FloatingVue);

app.use(router);  // This sets up routing
app.mount('#app');
