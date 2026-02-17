<template>
  <div class="hero">
    <div class="particles">
      <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
      <div class="particle" style="left: 20%; animation-delay: 2s;"></div>
      <div class="particle" style="left: 30%; animation-delay: 4s;"></div>
      <div class="particle" style="left: 50%; animation-delay: 1s;"></div>
      <div class="particle" style="left: 70%; animation-delay: 3s;"></div>
      <div class="particle" style="left: 80%; animation-delay: 5s;"></div>
      <div class="particle" style="left: 90%; animation-delay: 0.5s;"></div>
    </div>

    <div class="overlay"></div>

    <div class="content">
      <h1 class="title">
        Welcome to
        <span class="highlight">Placement Portal</span>
      </h1>

      <p class="subtitle">
        Connecting Students, Companies, and Opportunities.
      </p>

      <div class="buttons">
        <router-link to="/login">
          <button class="btn login">
            <span>Login</span>
            <div class="btn-glow"></div>
          </button>
        </router-link>

        <router-link to="/register">
          <button class="btn register">
            <span>Register</span>
            <div class="btn-glow"></div>
          </button>
        </router-link>
      </div>

      <p class="footer-text">
        {{ dynamicMessage }}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      hour: new Date().getHours()
    }
  },
  computed: {
    dynamicMessage() {
      if (this.hour < 12) return "Good Morning ☀️"
      if (this.hour < 18) return "Good Afternoon 🌤️"
      return "Good Evening 🌙"
    }
  },
  mounted() {
    this.$el.querySelector('.content').classList.add('animate-in');
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

.hero {
  height: 100vh;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533a7a 100%);
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  color: white;
  overflow: hidden;
  font-family: 'Inter', sans-serif;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  animation: float 6s linear infinite;
  box-shadow: 0 0 10px rgba(0, 198, 255, 0.5);
}

@keyframes float {
  0% {
    transform: translateY(100vh) scale(0);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100px) scale(1);
    opacity: 0;
  }
}

.overlay {
  position: absolute;
  width: 200%;
  height: 200%;
  background: 
    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
  animation: move 20s linear infinite;
}

@keyframes move {
  from { transform: translate(-25%, -25%) rotate(0deg); }
  to { transform: translate(-25%, -25%) rotate(360deg); }
}

.content {
  text-align: center;
  background: rgba(255, 255, 255, 0.12);
  padding: 60px 40px;
  border-radius: 24px;
  backdrop-filter: blur(20px) saturate(180%);
  box-shadow: 
    0 25px 45px rgba(0,0,0,0.25),
    inset 0 1px 0 rgba(255,255,255,0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
  z-index: 2;
  width: min(450px, 90%);
  display: flex;
  flex-direction: column;
  gap: 24px;
  transform: translateY(30px);
  opacity: 0;
  transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.content.animate-in {
  transform: translateY(0);
  opacity: 1;
}

.title {
  font-size: clamp(32px, 5vw, 42px);
  font-weight: 800;
  margin: 0;
  background: linear-gradient(135deg, #fff 0%, #00c6ff 50%, #ff6b9d 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
  overflow: hidden;
}

.title::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}

.highlight {
  background: linear-gradient(45deg, #00c6ff, #ff6b9d);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: highlightPulse 2s ease-in-out infinite alternate;
}

@keyframes highlightPulse {
  from { filter: hue-rotate(0deg) brightness(1); }
  to { filter: hue-rotate(10deg) brightness(1.1); }
}

.subtitle {
  margin: 0;
  font-size: 16px;
  font-weight: 400;
  opacity: 0.95;
  line-height: 1.6;
  max-width: 300px;
  margin-inline: auto;
}

.buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.btn {
  position: relative;
  width: 140px;
  height: 50px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  font-size: 15px;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: left 0.5s;
}

.btn:hover::before {
  left: 100%;
}

.btn span {
  position: relative;
  z-index: 2;
}

.btn-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.2) 50%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s;
}

.btn:hover .btn-glow {
  opacity: 1;
  animation: glow 1.5s infinite;
}

@keyframes glow {
  0%, 100% { opacity: 0; }
  50% { opacity: 1; }
}

.login {
  background: linear-gradient(135deg, #007bff, #0056b3);
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.3);
}

.login:hover {
  transform: translateY(-4px) scale(1.05);
  box-shadow: 0 15px 35px rgba(0, 123, 255, 0.4);
}

.register {
  background: linear-gradient(135deg, #28a745, #1e7e34);
  box-shadow: 0 8px 25px rgba(40, 167, 69, 0.3);
}

.register:hover {
  transform: translateY(-4px) scale(1.05);
  box-shadow: 0 15px 35px rgba(40, 167, 69, 0.4);
}

.footer-text {
  font-size: 14px;
  opacity: 0.85;
  font-weight: 400;
}

@media (max-width: 480px) {
  .buttons {
    flex-direction: column;
  }
  .btn {
    width: 100%;
  }
}
</style>