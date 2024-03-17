// import HomeView from "../views/home/HomeView.vue"
import HomeView from '../views/home/HomeView.vue'
import { createRouter, createWebHistory } from 'vue-router'


const routes = [
    { path: '/', component: HomeView }
    // , { path: '/transpile', component: HomeView }
    // ,{ path: '/quiz/:id', component: QuizView, props: true }
]

const router = createRouter({
    // 4. 内部提供了 history 模式的实现。为了简单起见，我们在这里使用 hash 模式。
    history: createWebHistory(import.meta.env.BASE_URL),
    routes, // `routes: routes` 的缩写
})

export default router