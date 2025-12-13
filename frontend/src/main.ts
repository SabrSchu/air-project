import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config'
import 'primeicons/primeicons.css'

// PrimeVue components
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import FloatLabel from 'primevue/floatlabel';
import InputText from 'primevue/inputtext';

const app = createApp(App);

app.use(PrimeVue, { unstyled : true });
app.use(router);

// Registration of global PrimeVue components
app.component('IconField', IconField);
app.component('InputIcon', InputIcon);
app.component('FloatLabel', FloatLabel);
app.component('InputText', InputText);

app.mount('#app');
