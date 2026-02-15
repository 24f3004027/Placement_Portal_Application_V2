<template>
  <div class="container">
    <div class="card">
      <h2>Login</h2>

      <form @submit.prevent="loginUser">
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Login</button>
      </form>

      <router-link to="/register">Create an account</router-link>

      <p class="message">{{ message }}</p>
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
      message: ""
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

        this.message = "Login Successful"

      } catch (err) {
        this.message = err.response?.data?.msg || "Login Failed"
      }
    }
  }
}
</script>

<style>
.container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f4f6f9;
}

.card {
  background: white;
  padding: 40px;
  width: 320px;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  text-align: center;
}

input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
  border: 1px solid #ccc;
}

button {
  width: 100%;
  padding: 10px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background: #0056b3;
}

.message {
  margin-top: 10px;
  color: green;
}
</style>