<template>
  <div class="login-hero">
    <!-- Floating particles -->
    <div class="particles">
      <div class="particle" style="--delay: 0s; --left: 10%;"></div>
      <div class="particle" style="--delay: 1.5s; --left: 25%;"></div>
      <div class="particle" style="--delay: 3s; --left: 40%;"></div>
      <div class="particle" style="--delay: 0.8s; --left: 60%;"></div>
      <div class="particle" style="--delay: 2.5s; --left: 75%;"></div>
      <div class="particle" style="--delay: 4s; --left: 90%;"></div>
    </div>

    <div class="overlay"></div>

    <div class="container">
      <div class="card" :class="{ 'animate-in': mounted }">
        <div class="card-header">
          <h2 class="title">
            Welcome Back
            <span class="highlight">👋</span>
          </h2>
          <p class="subtitle">Sign in to continue</p>
        </div>

        <form @submit.prevent="loginUser">
          <!-- Email -->
          <div class="input-group">
            <input
              v-model="email"
              type="email"
              placeholder=" "
              required
              class="input"
              autocomplete="email"
            />
            <label>Email</label>
            <span class="input-line"></span>
          </div>

          <!-- Password -->
          <div class="input-group">
            <input
              v-model="password"
              type="password"
              placeholder=" "
              required
              class="input"
              autocomplete="current-password"
            />
            <label>Password</label>
            <span class="input-line"></span>
          </div>

          <button class="btn-login" :disabled="loading">
            <span v-if="!loading" class="btn-text">Sign In</span>
            <div v-else class="loading-spinner"></div>
            <div class="btn-glow"></div>
          </button>
        </form>

        <div class="footer">
          <router-link to="/register" class="link">
            Don't have an account? <span>Create one</span>
          </router-link>
          
          <br><br>
          <router-link to="/" class="back-link">
            ← Back to Home
          </router-link>

          <transition name="message">
            <p v-if="message" class="message" :class="{ success: isSuccess, error: !isSuccess }">
              {{ message }}
            </p>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  data() {
    return {
      email: "",
      password: "",
      message: "",
      isSuccess: false,
      loading: false,
      mounted: false
    }
  },
  methods: {
    async loginUser() {
      try {
        const res = await axios.post("http://127.0.0.1:5000/login", {
          email: this.email,
          password: this.password
        })

        localStorage.setItem("token", res.data.access_token)
        localStorage.setItem("role", res.data.role)
        localStorage.setItem("name", res.data.name)

        // Immediate redirect (no message)
        if (res.data.role === "admin") {
          this.$router.push("/admin-dashboard")
        } else if (res.data.role === "student") {
          this.$router.push("/student-dashboard")
        } else {
          this.$router.push("/company-dashboard")
        }

      } 
      catch (err) {
        this.message = err.response?.data?.msg || "Login Failed"
      }
    }
  },
  mounted() {
    this.mounted = true
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

.back-link {
  display: inline-block;
  margin-bottom: 20px;
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  font-size: 14px;
  transition: 0.3s ease;
}

.back-link:hover {
  color: white;
  transform: translateX(-3px);
}

.login-hero {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 100%);
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

/* Particles & Overlays remain the same for atmosphere */
.particles { position: absolute; inset: 0; pointer-events: none; }
.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  top: 100vh;
  left: var(--left, 10%);
  animation: float 7s linear infinite;
  animation-delay: var(--delay, 0s);
}

@keyframes float {
  0% { transform: translateY(100vh) scale(0); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateY(-120px) scale(1); opacity: 0; }
}

.container {
  z-index: 2;
  width: 100%;
  padding: 20px;
  display: flex;
  justify-content: center;
}

/* GLASS CARD - Main container keeps the glass look */
.card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(25px) saturate(150%);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 28px;
  padding: 52px 40px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
  transform: translateY(40px);
  opacity: 0;
  transition: all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.card.animate-in {
  transform: translateY(0);
  opacity: 1;
}

.card-header { text-align: center; margin-bottom: 36px; }

.title {
  font-size: 32px;
  font-weight: 800;
  color: #ffffff;
  text-shadow: 0 2px 10px rgba(0,0,0,0.2);
  margin: 0 0 8px 0;
}

.subtitle {
  color: #ffffff;
  font-size: 16px;
  font-weight: 500;
  opacity: 0.95; /* Higher opacity for readability */
}

/* INPUT FIELDS - Made Opaque for focus and readability */
.input-group {
  position: relative;
  margin-bottom: 24px;
}

.input {
  width: 100%;
  padding: 18px 20px;
  /* High opacity background for readability */
  background: rgba(255, 255, 255, 0.95); 
  border: 2px solid transparent;
  border-radius: 16px;
  color: #1e293b; /* Dark text on light background */
  font-size: 16px;
  font-weight: 600;
  outline: none;
  transition: all 0.3s ease;
}

.input:focus {
  background: #ffffff;
  border-color: #6366f1;
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
  transform: translateY(-2px);
}

/* Floating Label Logic */
.input-group label {
  position: absolute;
  left: 20px;
  top: 18px;
  color: #64748b; /* Slate gray for better contrast */
  font-size: 16px;
  transition: all 0.3s ease;
  pointer-events: none;
}

.input:focus + label,
.input:not(:placeholder-shown) + label {
  top: -12px;
  left: 12px;
  font-size: 12px;
  font-weight: 700;
  color: #ffffff;
  background: #6366f1; /* Solid background for the floating tag */
  padding: 2px 10px;
  border-radius: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* LOGIN BUTTON */
.btn-login {
  width: 100%;
  height: 56px;
  background: #ffffff;
  color: #6366f1;
  border: none;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.btn-login:hover:not(:disabled) {
  background: #6366f1;
  color: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
}

/* FOOTER & LINKS */
.footer { text-align: center; margin-top: 24px; }

.link {
  color: #ffffff;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}

.link span {
  text-decoration: underline;
  font-weight: 700;
}

/* STATUS MESSAGES */
.message {
  margin-top: 20px;
  padding: 12px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  text-align: center;
}

.message.success { background: #dcfce7; color: #166534; }
.message.error { background: #fee2e2; color: #991b1b; }

@media (max-width: 480px) {
  .card { padding: 30px 20px; margin: 10px; }
}
</style>