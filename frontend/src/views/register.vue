<template>
  <div class="login-hero">
    <div class="particles">
      <div class="particle" style="--delay: 0s; --left: 15%;"></div>
      <div class="particle" style="--delay: 2s; --left: 35%;"></div>
      <div class="particle" style="--delay: 1s; --left: 55%;"></div>
      <div class="particle" style="--delay: 3.5s; --left: 85%;"></div>
    </div>

    <div class="container">
      <div class="card" :class="{ 'animate-in': mounted }">
        <div class="card-header">
          <h2 class="title">Create Account</h2>
          <p class="subtitle">Join our community today</p>
        </div>

        <form @submit.prevent="registerUser">
          <div class="input-group">
            <input v-model="name" type="text" placeholder=" " required class="input" />
            <label>Full Name</label>
          </div>

          <div class="input-group">
            <input v-model="email" type="email" placeholder=" " required class="input" />
            <label>Email Address</label>
          </div>

          <div class="input-group">
            <input v-model="password" type="password" placeholder=" " required class="input" />
            <label>Password</label>
          </div>

          <div class="input-group">
            <select v-model="role" required class="input select-input">
              <option value="" disabled selected hidden></option>
              <option value="student">Student</option>
              <option value="company">Company</option>
            </select>
            <label :class="{ 'label-fixed': role }">Select Role</label>
          </div>

          <button type="submit" class="btn-register">
            <span class="btn-text">Register</span>
            <div class="btn-glow"></div>
          </button>
        </form>

        <div class="footer">
          <router-link to="/login" class="link">
            Already have an account? <span>Login</span>
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
      name: "",
      email: "",
      password: "",
      role: "",
      message: "",
      isSuccess: false,
      mounted: false
    }
  },
  methods: {
    async registerUser() {
    try {
      await axios.post("http://127.0.0.1:5000/req", {
        name: this.name,
        email: this.email,
        password: this.password,
        role: this.role
      })

      // Redirect to login
      this.$router.push("/login")

    } 
    catch (err) {
      this.message = err.response?.data?.msg || "Registration Failed"
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

/* Background Particles */
.particles { position: absolute; inset: 0; pointer-events: none; }
.particle {
  position: absolute;
  width: 5px;
  height: 5px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  top: 100vh;
  left: var(--left, 10%);
  animation: float 8s linear infinite;
  animation-delay: var(--delay, 0s);
}

@keyframes float {
  0% { transform: translateY(100vh) scale(0); opacity: 0; }
  50% { opacity: 0.8; }
  100% { transform: translateY(-10vh) scale(1.2); opacity: 0; }
}

.container { z-index: 2; width: 100%; padding: 20px; display: flex; justify-content: center; }

/* Opaque Glass Card */
.card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(25px) saturate(160%);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 28px;
  padding: 40px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
  transform: translateY(30px);
  opacity: 0;
  transition: all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.card.animate-in { transform: translateY(0); opacity: 1; }

.card-header { text-align: center; margin-bottom: 30px; }

.title {
  font-size: 30px;
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 5px 0;
  text-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.subtitle { color: #ffffff; font-size: 15px; font-weight: 500; opacity: 0.9; }

/* Input Styling - High Readability */
.input-group { position: relative; margin-bottom: 20px; }

.input {
  width: 100%;
  padding: 18px 20px;
  background: rgba(255, 255, 255, 0.95); /* Nearly solid for clarity */
  border: 2px solid transparent;
  border-radius: 16px;
  color: #1e293b;
  font-size: 15px;
  font-weight: 600;
  outline: none;
  transition: all 0.3s ease;
}

.input:focus {
  background: #ffffff;
  border-color: #a855f7;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

/* Label logic */
.input-group label {
  position: absolute;
  left: 20px;
  top: 18px;
  color: #64748b;
  font-size: 15px;
  transition: all 0.3s ease;
  pointer-events: none;
}

.input:focus + label,
.input:not(:placeholder-shown) + label,
.label-fixed {
  top: -12px;
  left: 12px;
  font-size: 11px;
  font-weight: 800;
  color: #ffffff;
  background: #a855f7;
  padding: 2px 10px;
  border-radius: 6px;
  text-transform: uppercase;
}

/* Custom Select Styling */
.select-input {
  appearance: none;
  cursor: pointer;
}

/* Button Styling */
.btn-register {
  width: 100%;
  height: 56px;
  background: #ffffff;
  color: #a855f7;
  border: none;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.btn-register:hover {
  background: #a855f7;
  color: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(168, 85, 247, 0.4);
}

.footer { text-align: center; margin-top: 25px; }

.link { color: #ffffff; text-decoration: none; font-size: 14px; font-weight: 500; }
.link span { font-weight: 700; text-decoration: underline; }

/* Messages */
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
  .card { padding: 30px 20px; }
}
</style>