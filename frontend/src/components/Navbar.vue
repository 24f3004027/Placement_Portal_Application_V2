<template>
  <nav class="app-navbar">
    <div class="nav-brand">
      <router-link to="/" class="brand-link">
        <span class="brand-icon">🎓</span>
        <span class="brand-text">Placement Portal <small class="version-tag">v2</small></span>
      </router-link>
    </div>

    <div class="nav-actions" v-if="token">
      <span class="user-badge" :class="roleBadgeClass">
        {{ roleName }}
      </span>
      <span class="user-name" v-if="userName">
        👤 {{ userName }}
      </span>
      <button @click="handleLogout" class="btn-logout">
        🚪 Logout
      </button>
    </div>

    <div class="nav-actions" v-else>
      <router-link to="/login" class="nav-btn btn-secondary">Login</router-link>
      <router-link to="/register" class="nav-btn btn-primary">Register</router-link>
    </div>
  </nav>
</template>

<script>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { authService } from "../services/authService";

export default {
  name: "Navbar",
  setup() {
    const router = useRouter();

    const token = computed(() => localStorage.getItem("access_token"));
    const role = computed(() => localStorage.getItem("role"));
    const userName = computed(() => localStorage.getItem("user_name"));

    const roleName = computed(() => {
      const r = role.value;
      if (r === "admin") return "Administrator";
      if (r === "company") return "Recruiter";
      if (r === "student") return "Student";
      return "User";
    });

    const roleBadgeClass = computed(() => {
      const r = role.value;
      if (r === "admin") return "badge-admin";
      if (r === "company") return "badge-company";
      if (r === "student") return "badge-student";
      return "";
    });

    const handleLogout = () => {
      authService.logout();
      router.push("/login");
    };

    return {
      token,
      userName,
      roleName,
      roleBadgeClass,
      handleLogout
    };
  }
};
</script>

<style scoped>
.app-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: rgba(18, 24, 38, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  font-weight: 700;
  font-size: 1.25rem;
  color: #ffffff;
}

.brand-icon {
  font-size: 1.5rem;
}

.version-tag {
  font-size: 0.75rem;
  background: #3b82f6;
  color: white;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  margin-left: 0.25rem;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-name {
  font-size: 0.9rem;
  color: #e2e8f0;
  font-weight: 500;
}

.user-badge {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.6rem;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-admin {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.4);
}

.badge-company {
  background: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
  border: 1px solid rgba(245, 158, 11, 0.4);
}

.badge-student {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
  border: 1px solid rgba(59, 130, 246, 0.4);
}

.btn-logout {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
  padding: 0.4rem 0.9rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.85rem;
  transition: all 0.2s ease;
}

.btn-logout:hover {
  background: #ef4444;
  color: white;
}

.nav-btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: #e2e8f0;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
}
</style>
