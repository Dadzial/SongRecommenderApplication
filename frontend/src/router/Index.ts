import { createRouter, createWebHistory } from "vue-router"
import SearchView from "../views/SearchView.vue"
import ResultsView from "../views/ResultsView.vue"

const routes = [
    { path: "/", component: SearchView },
    { path: "/results", component: ResultsView }
]

export const router = createRouter({
    history: createWebHistory(),
    routes
})