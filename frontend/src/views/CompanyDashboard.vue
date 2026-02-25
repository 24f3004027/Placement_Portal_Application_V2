<template>
  <div class="dashboard">

    <!-- TOP BAR -->
    <div class="top-bar">
      <h1>Welcome {{ companyName }}</h1>
      <button class="logout-btn" @click="logout">Logout</button>
    </div>

    <!-- SUMMARY -->
    <div class="cards">
      <div class="card">
        <h3>Jobs Posted</h3>
        <p>{{ jobs.length }}</p>
      </div>
    </div>
    <button @click="showProfile = !showProfile" class="create-btn">
  {{ showProfile ? "Cancel Profile Edit" : "Edit Profile" }}
</button>

<div v-if="showProfile" class="form">
  <input v-model="profile.name" placeholder="Company Name" />
  <input v-model="profile.email" placeholder="Email" />
  <input v-model="profile.password" placeholder="New Password (optional)" type="password" />

  <button @click="updateProfile">
    Update Profile
  </button>

  <p v-if="profileMessage" class="error">
    {{ profileMessage }}
  </p>
</div>

    <!-- CREATE BUTTON -->
    <button class="create-btn" @click="toggleForm">
      {{ showForm ? "Cancel" : "Create Job" }}
    </button>

    <!-- FORM -->
    <div v-if="showForm" class="form">
      <input v-model="newJob.title" placeholder="Job Title" />
      <input v-model="newJob.location" placeholder="Location" />
      <input v-model="newJob.salary" placeholder="Salary" />
      <textarea v-model="newJob.description" placeholder="Description"></textarea>

      <p v-if="salaryError" class="error">
        {{ salaryError }}
      </p>

      <button @click="saveJob">
        {{ editingJobId ? "Update Job" : "Add Job" }}
      </button>
    </div>

    <!-- JOB LIST -->
    <div v-for="job in jobs" :key="job.id" class="job-card">
      <h3>{{ job.title }}</h3>
      <p><b>Location:</b> {{ job.location }}</p>
      <p><b>Salary:</b> {{ job.salary }}</p>
      <p>{{ job.description }}</p>

      <button @click="startEdit(job)">Edit</button>
      <button class="delete-btn" @click="deleteJob(job.id)">Delete</button>
    </div>

    <p v-if="loading">Loading...</p>

  </div>
</template>

<script>
import axios from "axios"

export default {
  data() {
    return {
      companyName: localStorage.getItem("name"),
      jobs: [],
      showForm: false,
      loading: true,
      salaryError: "",
      editingJobId: null,
      newJob: {
        title: "",
        location: "",
        salary: "",
        description: ""
      },
      showProfile: false,
      profileMessage: "",
      profile: {
        name: "",
        email: "",
        password: ""
      }
    }
  },

  mounted() {
    this.fetchJobs(),
    this.fetchProfile()
  },

  methods: {

    toggleForm() {
      this.resetForm()
      this.showForm = !this.showForm
    },
    async fetchProfile() {
  const token = localStorage.getItem("access_token")

      try {
        const res = await axios.get(
          "http://127.0.0.1:5000/company/profile",
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        )

        this.profile.name = res.data.name
        this.profile.email = res.data.email

      } catch (err) {
        console.error(err)
      }
    },

    async updateProfile() {
  const token = localStorage.getItem("access_token")

  try {
    await axios.put(
      "http://127.0.0.1:5000/company/profile",
      this.profile,
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    )

        this.profileMessage = "Profile updated successfully"

        // Update local storage name if changed
        localStorage.setItem("name", this.profile.name)

        setTimeout(() => {
          this.profileMessage = ""
          this.showProfile = false
        }, 1500)

      } catch (err) {
        console.error(err)
        this.profileMessage = "Update failed"
      }
    },

    async fetchJobs() {
      try {
        const token = localStorage.getItem("access_token")

        const res = await axios.get(
          "http://127.0.0.1:5000/company/jobs",
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        )

        this.jobs = res.data

      } catch (err) {
        console.error(err)
        this.$router.push("/login")
      } finally {
        this.loading = false
      }
    },

    async saveJob() {

      this.salaryError = ""
      const salaryValue = Number(this.newJob.salary)

      if (!Number.isInteger(salaryValue) || salaryValue <= 0) {
        this.salaryError = "Salary must be a positive integer"
        return
      }

      const token = localStorage.getItem("access_token")

      try {

        if (this.editingJobId) {
          // UPDATE
          await axios.put(
            `http://127.0.0.1:5000/company/jobs/${this.editingJobId}`,
            this.newJob,
            { headers: { Authorization: `Bearer ${token}` } }
          )
        } else {
          // CREATE
          await axios.post(
            "http://127.0.0.1:5000/company/jobs",
            this.newJob,
            { headers: { Authorization: `Bearer ${token}` } }
          )
        }

        this.resetForm()
        this.showForm = false
        this.fetchJobs()

      } catch (err) {
        console.error(err)
      }
    },

    startEdit(job) {
      this.newJob = {
        title: job.title,
        location: job.location,
        salary: job.salary,
        description: job.description
      }
      this.editingJobId = job.id
      this.showForm = true
    },

    async deleteJob(jobId) {
      const token = localStorage.getItem("access_token")

      try {
        await axios.delete(
          `http://127.0.0.1:5000/company/jobs/${jobId}`,
          { headers: { Authorization: `Bearer ${token}` } }
        )

        this.fetchJobs()

      } catch (err) {
        console.error(err)
      }
    },

    resetForm() {
      this.newJob = {
        title: "",
        location: "",
        salary: "",
        description: ""
      }
      this.editingJobId = null
      this.salaryError = ""
    },

    logout() {
      localStorage.clear()
      this.$router.push("/login")
    }

  }
}
</script>

<style scoped>
.dashboard {
  padding: 40px;
  font-family: Arial;
  background: #0f172a;
  min-height: 100vh;
  color: white;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
}

.cards {
  margin-bottom: 20px;
}

.card {
  background: #1e293b;
  padding: 20px;
  border-radius: 10px;
}

.create-btn {
  margin-bottom: 20px;
  padding: 8px 16px;
}

.form input,
.form textarea {
  display: block;
  margin: 10px 0;
  padding: 8px;
  width: 300px;
}

.job-card {
  background: #1e293b;
  padding: 15px;
  margin-top: 15px;
  border-radius: 8px;
}

.delete-btn {
  background: #dc2626;
  color: white;
  border: none;
  padding: 6px 10px;
}

.error {
  color: #f87171;
}
</style>