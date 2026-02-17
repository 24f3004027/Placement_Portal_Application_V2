import { createRouter, createWebHistory } from "vue-router"

import Welcome from "../views/Welcome.vue"
import Login from "../views/Login.vue"
import Register from "../views/Register.vue"
import AdminDashboard from "../views/AdminDashboard.vue"
import CompanyDashboard from "../views/CompanyDashboard.vue"
import StudentDashboard from "../views/StudentDashboard.vue"

const routes = [
  { path: "/", component: Welcome},
  { path: "/login", component: Login },
  { path: "/register", component: Register },,
  { path: "/admin-dashboard", component: AdminDashboard },
  { path: "/company-dashboard", component: CompanyDashboard },
  { path: "/student-dashboard", component: StudentDashboard }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router