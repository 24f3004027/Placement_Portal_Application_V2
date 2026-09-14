<template>
  <div class="welcome-container">
    <div class="hero-card">
      <div class="hero-icon">🎓</div>
      <h1 class="hero-title">Enterprise Placement Portal</h1>
      <p class="hero-subtitle">
        Streamlined campus recruitment, asynchronous data exports, Redis caching, and real-time application management.
      </p>

      <div class="feature-pills">
        <span class="pill">⚡ Vue 3 & Vite</span>
        <span class="pill">🐍 Flask REST API</span>
        <span class="pill">🔑 JWT RBAC</span>
        <span class="pill">🔄 Celery & Redis</span>
        <span class="pill">📄 ReportLab PDF</span>
      </div>

      <div class="hero-actions">
        <router-link to="/login" class="btn btn-primary">
          🔑 Sign In to Portal
        </router-link>
        <router-link to="/register" class="btn btn-secondary">
          ✨ Create New Account
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Welcome"
};
</script>

<style scoped>
.welcome-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
}

.hero-card {
  background: rgba(18, 24, 38, 0.75);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 3.5rem 2.5rem;
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  text-align: center;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
}

.hero-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
}

.hero-title {
  font-size: 2.2rem;
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 0.75rem 0;
  letter-spacing: -0.5px;
}

.hero-subtitle {
  font-size: 1rem;
  color: #94a3b8;
  line-height: 1.6;
  margin: 0 0 1.75rem 0;
}

.feature-pills {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.pill {
  background: rgba(59, 130, 246, 0.15);
  border: 1px solid rgba(59, 130, 246, 0.3);
  color: #60a5fa;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.3rem 0.7rem;
  border-radius: 20px;
}

.hero-actions {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.btn {
  padding: 0.85rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  display: inline-block;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.08);
  color: #e2e8f0;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.15);
}
</style>