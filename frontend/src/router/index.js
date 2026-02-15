import { createRouter, createWebHistory } from "vue-router"

import Welcome from "../views/Welcome.vue"
import Login from "../views/Login.vue"
import Register from "../views/Register.vue"

const routes = [
  { path: "/", component: Welcome},
  { path: "/login", component: Login },
  { path: "/register", component: Register }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router