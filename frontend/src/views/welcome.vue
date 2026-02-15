<template>
  <div class="container">
    <div class="card">
      <h1>Welcome to Placement Portal</h1>
      <p>Your gateway to opportunities.</p>

      <div class="buttons">
        <router-link to="/login">
          <button class="login-btn">Login</button>
        </router-link>

        <router-link to="/register">
          <button class="register-btn">Register</button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<style>
.container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #007bff, #00c6ff);
}

.card {
  background: white;
  padding: 50px;
  border-radius: 10px;
  text-align: center;
  width: 400px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

h1 {
  margin-bottom: 10px;
}

p {
  margin-bottom: 30px;
  color: #555;
}

.buttons {
  display: flex;
  justify-content: space-between;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 120px;
}

.login-btn {
  background: #007bff;
  color: white;
}

.register-btn {
  background: #28a745;
  color: white;
}

button:hover {
  opacity: 0.9;
}
</style>