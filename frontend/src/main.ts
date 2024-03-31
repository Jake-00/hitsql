// import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ArcoVue from '@arco-design/web-vue';
import ArcoVueIcon from '@arco-design/web-vue/es/icon';
import '@arco-design/web-vue/dist/arco.css';
import { basicSetup } from 'codemirror'
import VueCodemirror from 'vue-codemirror'
import 'highlight.js/styles/stackoverflow-light.css'
import hljs from 'highlight.js/lib/core';
import sql from 'highlight.js/lib/languages/sql';
import hljsVuePlugin from "@highlightjs/vue-plugin";

hljs.registerLanguage('sql', sql);
const app = createApp(App)

app.use(router)
app.use(ArcoVue)
app.use(ArcoVueIcon)
app.use(hljsVuePlugin)
app.use(VueCodemirror, {
    // optional default global options
    autofocus: true,
    disabled: false,
    indentWithTab: true,
    tabSize: 2,
    placeholder: 'Code goes here...',
    extensions: [basicSetup]
    // ...
})
app.mount('#app')

