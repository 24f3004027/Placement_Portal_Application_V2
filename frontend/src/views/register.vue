<template>
  <div class="container">
    <div class="card">
      <h2>Register</h2>

      <form @submit.prevent="registerUser">
        <input v-model="name" placeholder="Full Name" required />
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Password" required />

        <select v-model="role" required>
          <option value="">Select Role</option>
          <option value="student">Student</option>
          <option value="company">Company</option>
        </select>

        <button type="submit">Register</button>
      </form>

      <router-link to="/login">Back to Login</router-link>

      <p class="message">{{ message }}</p>
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
      message: ""
    }
  },
  methods: {
    async registerUser() {
      try {
        const res = await axios.post("http://127.0.0.1:5000/req", {
          name: this.name,
          email: this.email,
          password: this.password,
          role: this.role
        })

        this.message = res.data.msg

      } catch (err) {
        this.message = err.response?.data?.msg || "Registration Failed"
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

input, select {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
  border: 1px solid #ccc;
}

button {
  width: 100%;
  padding: 10px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background: #1e7e34;
}

.message {
  margin-top: 10px;
  color: green;
}
</style>