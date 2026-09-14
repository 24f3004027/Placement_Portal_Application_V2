<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h2>Create Account</h2>
        <p>Register as a Student or Recruiter to get started</p>
      </div>

      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label>Full Name / Company Name</label>
          <input
            type="text"
            placeholder="John Doe"
            v-model="name"
            required
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label>Email Address</label>
          <input
            type="email"
            placeholder="name@example.com"
            v-model="email"
            required
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input
            type="password"
            placeholder="••••••••"
            v-model="password"
            required
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label>Account Role</label>
          <select v-model="role" required class="form-control">
            <option disabled value="">Select Role</option>
            <option value="student">Student</option>
            <option value="company">Corporate Recruiter (Company)</option>
          </select>
        </div>

        <button type="submit" class="btn-submit" :disabled="loading">
          <span v-if="!loading">Create Account</span>
          <span v-else>Registering...</span>
        </button>
      </form>

      <div v-if="error" class="alert-error">
        ⚠️ {{ error }}
      </div>

      <div class="auth-footer">
        <p>Already have an account? <router-link to="/login">Sign In</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import { authService } from "../services/authService";

export default {
  name: "Register",
  data() {
    return {
      name: "",
      email: "",
      password: "",
      role: "",
      error: "",
      loading: false
    };
  },
  methods: {
    async handleRegister() {
      this.error = "";
      this.loading = true;
      try {
        await authService.register(this.name, this.email, this.password, this.role);
        this.$router.push("/login");
      } catch (err) {
        this.error = err.response?.data?.msg || "Registration failed. Please try again.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
}

.auth-card {
  background: rgba(18, 24, 38, 0.75);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2.5rem;
  border-radius: 12px;
  width: 100%;
  max-width: 440px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.auth-header h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.75rem;
  color: #ffffff;
}

.auth-header p {
  margin: 0 0 1.5rem 0;
  color: #94a3b8;
  font-size: 0.9rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  text-align: left;
}

.form-group label {
  font-size: 0.85rem;
  color: #cbd5e1;
  font-weight: 600;
}

.form-control {
  padding: 0.75rem 1rem;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(10, 14, 23, 0.6);
  color: #ffffff;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}

.form-control:focus {
  border-color: #3b82f6;
}

.btn-submit {
  padding: 0.8rem;
  border-radius: 6px;
  border: none;
  background: #10b981;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 0.5rem;
}

.btn-submit:hover:not(:disabled) {
  background: #059669;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.alert-error {
  margin-top: 1rem;
  padding: 0.75rem;
  border-radius: 6px;
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #f87171;
  font-size: 0.85rem;
  text-align: center;
}

.auth-footer {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.9rem;
  color: #94a3b8;
}

.auth-footer a {
  color: #60a5fa;
  font-weight: 600;
  text-decoration: none;
}

.auth-footer a:hover {
  text-decoration: underline;
}
</style>