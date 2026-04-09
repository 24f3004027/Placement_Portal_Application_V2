<template>
  <div class="dashboard">
    <div class="top-bar">
      <h1>Welcome, {{ name }}</h1>
      <div style="display: flex; gap: 10px;">
      <button @click="view = 'profile'">Edit Profile</button>
      <button @click="logout">Logout</button>
    </div>
  </div>

  <div class="menu">
    <button :class="{ active: view === 'jobs' }" @click="view = 'jobs'">
      Browse Jobs
    </button>

    <button :class="{ active: view === 'applications' }" @click="view = 'applications'">
      My Applications
    </button>

    <button :class="{ active: view === 'profile' }" @click="view = 'profile'">
      My Profile
    </button>
  </div>

  <input 
    v-model="searchQuery" 
    placeholder="Search by title, skills, company..." 
    class="search-bar"
  />
  <!-- JOBS -->
    <div v-if="view === 'jobs'">
      <h2>Available Jobs</h2>
      <div v-for="job in filteredJobs" :key="job.id" class="card">
        <h3>{{ job.title }}</h3>
        <p>{{ job.description }}</p>
        <p><b>Skills:</ b> {{ job.skills }}</p>
        <button 
          @click="apply(job.id)" 
          :disabled="appliedJobs.has(job.id)"
        >
          {{ appliedJobs.has(job.id) ? "Applied" : "Apply" }}
        </button>
      </div>
    </div>

    <!-- APPLICATIONS -->
    <div v-if="view === 'applications'">
      <h2>My Applications</h2>
      
      <div style="margin-bottom: 15px;">
        <button @click="exportData">Export CSV</button>
        <button @click="downloadCSV">Download CSV</button>
      </div>

      <div v-for="app in applications" :key="app.id" class="card">
        <h3>{{ app.job_title }}</h3>
        <p><b>Status:</b> {{ app.status.toUpperCase() }}</p>
        <a 
        v-if="app.offer_letter && app.status === 'selected'" 
        :href="app.offer_letter" 
        target="_blank"
      >
        📄 View Offer Letter
      </a>

        <p v-if="app.status === 'interview'">📅 Interview Scheduled</p>
        <p v-if="app.status === 'offer'">🎉 Offer Received</p>
        <p v-if="app.status === 'placed'">🏆 Successfully Placed</p>
        <p v-if="app.status === 'rejected'">❌ Rejected</p>
        
        <p v-if="app.feedback">Feedback: {{ app.feedback }}</p>
        <p v-if="app.interview_date">Interview: {{ app.interview_date }}</p>
      </div>
    </div>

    <div v-if="view === 'profile'">
      <input v-model="profile.education" placeholder="Education (e.g. B.Tech CSE IIT Madras)" />
      <input v-model="profile.skills" placeholder="Skills (comma separated)" />
      <textarea v-model="profile.experience" placeholder="Experience (internships, projects)"></textarea>
      
      <h2>My Profile</h2>
      <input v-model="profile.name" placeholder="Name" />
      <input v-model="profile.email" placeholder="Email" />
      <input v-model="profile.password" placeholder="New Password" type="password" />
      <input v-model="profile.department" placeholder="Department" />
      <input v-model="profile.cgpa" placeholder="CGPA" />
      <input v-model="profile.resume" placeholder="Resume Link" />
      <button @click="updateProfile">Save</button>
    </div>
  </div>
</template>

<script>
  import axios from "axios";

  export default {
    data() {
      return {
        name: localStorage.getItem("name"),
        view: "jobs",
        searchQuery: "",
        jobs: [],
        appliedJobs: new Set(),
        applications: [],
        profile: {
          name: "",
          email: "",
          password: "",
          education: "",
          skills: "",
          experience: "",
          department: "",
          cgpa: "",
          resume: ""
        }
      };
    },
    computed: {
      filteredJobs() {
        return this.jobs.filter(job =>
          job.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          job.skills?.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          job.company_name?.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }
    },

    mounted() {
      this.fetchJobs();
      this.fetchApplications();
      this.fetchProfile();

      this.interval = setInterval(() => {
        if (this.view === "applications") {
          this.fetchApplications();
        }
      }, 5000);
    },

    beforeUnmount() {
      clearInterval(this.interval);
    },

    methods: {
      async fetchJobs() {
        const token = localStorage.getItem("access_token");
        const res = await axios.get("http://127.0.0.1:5000/student/jobs", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.jobs = res.data;
      },

      async apply(jobId) {
        const token = localStorage.getItem("access_token");
        if (!this.profile.cgpa) {
          alert("Please fill your CGPA before applying");
          this.view = "profile";
          return;
        }
        try {
          const res = await axios.post(
            `http://127.0.0.1:5000/student/apply/${jobId}`,
            {},
            { headers: { Authorization: `Bearer ${token}` } }
          );

            alert(res.data.msg || "Applied successfully");

          } catch (err) {
            alert(err.response?.data?.msg || "Apply failed");
          }

          await this.fetchApplications();
          await this.fetchJobs();
          
      },
      async exportData() {
        const token = localStorage.getItem("access_token");

        await axios.post("http://127.0.0.1:5000/student/export", {}, {
          headers: { Authorization: `Bearer ${token}` }
        });

        alert("Export started!");
      },
      async downloadCSV() {
        const token = localStorage.getItem("access_token");

        try {
          const response = await fetch("http://127.0.0.1:5000/student/download/export_2.csv", {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });

          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);

          const a = document.createElement("a");
          a.href = url;
          a.download = "export.csv";
          a.click();
        } catch (err) {
          console.error(err);
          alert("Download failed");
        }
      },
      async fetchApplications() {
        const token = localStorage.getItem("access_token");
        const res = await axios.get("http://127.0.0.1:5000/student/applications", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.applications = res.data;
        this.appliedJobs = new Set(res.data.map(a => a.job_id));
      },

      async fetchProfile() {
        const token = localStorage.getItem("access_token");
        const res = await axios.get("http://127.0.0.1:5000/student/profile", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.profile = res.data;
      },

      async updateProfile() {
        const token = localStorage.getItem("access_token");

        try {
          await axios.put(
            "http://127.0.0.1:5000/student/profile",
            this.profile,
            { headers: { Authorization: `Bearer ${token}` } }
          );

          await this.fetchProfile();
          localStorage.setItem("name", this.profile.name);
          this.name = this.profile.name;

          alert("Profile updated");

        } catch (err) {
          alert(err.response?.data?.msg || "Update failed");
        }
      },

      logout() {
        localStorage.clear();
        this.$router.push("/login");
      }
    },
    watch: {
      view(newVal) {
        if (newVal === "applications") this.fetchApplications();
        if (newVal === "jobs") this.fetchJobs();
        if (newVal === "profile") this.fetchProfile();
      }
    }
  };
</script>

<style scoped>

  .dashboard {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #333;
    background-color: #f8f9fa;
    min-height: 100vh;
  }

  .top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 15px;
    border-bottom: 2px solid #eee;
  }

  .top-bar h1 {
    font-size: 1.8rem;
    color: #2c3e50;
    margin: 0;
  }

  .top-bar button {
    background-color: #e74c3c;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.3s;
  }

  .top-bar button:hover {
    background-color: #c0392b;
  }

  .menu button.active {
    background-color: #3498db;
    color: white;
  }

  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }

  .menu {
    display: flex;
    gap: 10px;
    margin-bottom: 30px;
  }

  .menu button {
    flex: 1;
    padding: 12px;
    border: 1px solid #ddd;
    background: white;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    color: #666;
    transition: all 0.2s ease;
  }

  .menu button:hover {
    background-color: #f0f4f8;
    border-color: #3498db;
    color: #3498db;
  }

  .top-bar div button:first-child {
    background-color: #3498db;
    color: white;
  }

  .card {
    background: white;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    border-left: 5px solid #3498db;
    transition: transform 0.2s;
  }

  .card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  }

  .card h3 {
    margin-top: 0;
    color: #2c3e50;
  }

  .card p {
    line-height: 1.6;
    color: #555;
  }

  .card button {
    background-color: #27ae60;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
  }

  .card button:hover {
    background-color: #219150;
  }

  input {
    display: block;
    width: 100%;
    padding: 12px;
    margin-bottom: 15px;
    border: 1px solid #ddd;
    border-radius: 6px;
    box-sizing: border-box; 
    font-size: 1rem;
  }

  input:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
  }

  div[v-if="view === 'profile'"] button {
    width: 100%;
    background-color: #3498db;
    color: white;
    border: none;
    padding: 12px;
    border-radius: 6px;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
  }

  div[v-if="view === 'profile'"] button:hover {
    background-color: #2980b9;
  }

  .card p b {
    color: #34495e;
  }

  .menu button.active:hover {
    background-color: #2980b9;
  }
</style>