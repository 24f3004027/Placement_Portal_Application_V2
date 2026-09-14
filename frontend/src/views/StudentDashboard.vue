<template>
  <div class="dashboard-page">
    <div class="dashboard-header">
      <div class="header-text">
        <h1>Welcome, {{ name || 'Student' }}</h1>
        <p>Explore placement drives, track applications, and manage your academic profile</p>
      </div>
      
      <div class="header-actions">
        <button class="btn btn-purple" @click="exportReport">📊 Generate Report</button>
        <button class="btn btn-outline" @click="downloadReport">📥 PDF Report</button>

        <template v-if="view === 'applications'">
          <button class="btn btn-outline" @click="exportData">📤 Export CSV</button>
          <button v-if="exportReady" class="btn btn-success" @click="downloadCSV">💾 Download CSV</button>
        </template>
        
        <button class="btn btn-primary" @click="view = 'profile'">⚙️ Edit Profile</button>
      </div>
    </div>

    <div class="tab-navigation">
      <button :class="['tab-btn', { active: view === 'jobs' }]" @click="view = 'jobs'">
        💼 Browse Jobs ({{ jobs.length }})
      </button>
      <button :class="['tab-btn', { active: view === 'applications' }]" @click="view = 'applications'">
        📑 My Applications ({{ applications.length }})
      </button>
      <button :class="['tab-btn', { active: view === 'profile' }]" @click="view = 'profile'">
        👤 My Profile
      </button>
    </div>

    <!-- Browse Jobs Tab -->
    <div v-if="view === 'jobs'" class="tab-content">
      <div class="search-bar-container">
        <input 
          v-model="searchQuery" 
          placeholder="🔍 Search opportunities by job title, skills, or company name..." 
          class="search-input" 
        />
      </div>

      <div class="cards-grid">
        <div v-for="job in filteredJobs" :key="job.id" class="data-card job-card">
          <div class="card-main">
            <div class="card-title-row">
              <h3>{{ job.title }}</h3>
              <span class="company-tag">🏢 {{ job.company_name }}</span>
            </div>
            <p class="card-desc">{{ job.description }}</p>
            <div class="card-meta">
              <span>📍 {{ job.location || 'Remote' }}</span>
              <span>💰 ₹{{ job.salary ? job.salary.toLocaleString() : 'N/A' }}/yr</span>
              <span>💼 {{ job.experience }} yrs exp</span>
            </div>
            <p class="skills-list" v-if="job.skills"><strong>Skills:</strong> {{ job.skills }}</p>
          </div>
          <button 
            @click="apply(job.id)" 
            :class="['btn', job.applied ? 'btn-applied' : 'btn-primary']"
            :disabled="job.applied"
          >
            {{ job.applied ? "✓ Applied" : "Apply Now" }}
          </button>
        </div>
      </div>
    </div>

    <!-- Applications Tab -->
    <div v-if="view === 'applications'" class="tab-content">
      <div class="cards-list">
        <div v-for="app in applications" :key="app.id" class="data-card app-card">
          <div class="app-header-row">
            <h3>{{ app.job_title }}</h3>
            <span :class="['status-badge', app.status]">{{ (app.status || 'applied').toUpperCase() }}</span>
          </div>

          <div class="app-details">
            <p v-if="app.interview_date">📅 <strong>Interview Scheduled:</strong> {{ app.interview_date }}</p>
            <p v-if="app.interview_link">🔗 <strong>Meeting Link:</strong> <a :href="app.interview_link" target="_blank">{{ app.interview_link }}</a></p>
            <p v-if="app.feedback">💬 <strong>Feedback:</strong> {{ app.feedback }}</p>
            <a v-if="app.offer_letter && (app.status === 'selected' || app.status === 'offer')" :href="app.offer_letter" target="_blank" class="offer-link">
              📄 Download Offer Letter
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Profile Tab -->
    <div v-if="view === 'profile'" class="tab-content">
      <div class="profile-card-container">
        <div class="form-section">
          <h3>Personal Information</h3>
          <div class="form-grid">
            <div class="form-group">
              <label>Full Name</label>
              <input v-model="profile.name" placeholder="Full Name" class="form-control" />
            </div>
            <div class="form-group">
              <label>Email Address</label>
              <input v-model="profile.email" placeholder="Email" class="form-control" />
            </div>
            <div class="form-group">
              <label>Department</label>
              <input v-model="profile.department" placeholder="e.g. Computer Science" class="form-control" />
            </div>
            <div class="form-group">
              <label>Current CGPA</label>
              <input v-model="profile.cgpa" placeholder="8.5" class="form-control" />
            </div>
          </div>
        </div>

        <div class="form-section">
          <h3>Academic & Professional Details</h3>
          <div class="form-stack">
            <div class="form-group">
              <label>Education</label>
              <input v-model="profile.education" placeholder="Degree, University" class="form-control" />
            </div>
            <div class="form-group">
              <label>Technical Skills</label>
              <input v-model="profile.skills" placeholder="Java, Python, Vue, Flask, Redis" class="form-control" />
            </div>
            <div class="form-group">
              <label>Work / Project Experience</label>
              <textarea v-model="profile.experience" placeholder="Describe your key projects and internships..." class="form-control textarea"></textarea>
            </div>
            <div class="form-group">
              <label>Resume Link</label>
              <input v-model="profile.resume" placeholder="Public Google Drive / GitHub Resume URL" class="form-control" />
            </div>
          </div>
        </div>

        <button class="btn btn-save" @click="updateProfile">💾 Save Profile Changes</button>
      </div>
    </div>
  </div>
</template>

<script>
import { studentService } from "../services/studentService";
import { adminService } from "../services/adminService";

export default {
  name: "StudentDashboard",
  data() {
    return {
      name: localStorage.getItem("user_name") || "",
      view: "jobs",
      searchQuery: "",
      reportReady: false,
      exportReady: false,
      jobs: [],
      applications: [],
      profile: {
        name: "",
        email: "",
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
      const q = this.searchQuery.toLowerCase();
      return this.jobs.filter(job =>
        (job.title && job.title.toLowerCase().includes(q)) ||
        (job.skills && job.skills.toLowerCase().includes(q)) ||
        (job.company_name && job.company_name.toLowerCase().includes(q))
      );
    }
  },
  async mounted() {
    await this.fetchJobs();
    await this.fetchApplications();
    await this.fetchProfile();

    this.interval = setInterval(() => {
      if (this.view === "applications") {
        this.fetchApplications();
      }
    }, 5000);
  },
  beforeUnmount() {
    if (this.interval) clearInterval(this.interval);
  },
  methods: {
    async fetchJobs() {
      try {
        this.jobs = await studentService.getJobs();
      } catch (err) {
        console.error("Failed to fetch jobs", err);
      }
    },
    async fetchApplications() {
      try {
        this.applications = await studentService.getApplications();
      } catch (err) {
        console.error("Failed to fetch applications", err);
      }
    },
    async fetchProfile() {
      try {
        this.profile = await studentService.getProfile();
      } catch (err) {
        console.error("Failed to fetch profile", err);
      }
    },
    async apply(jobId) {
      if (!this.profile.cgpa) {
        alert("Please fill in your CGPA in your profile before applying.");
        this.view = "profile";
        return;
      }
      try {
        const res = await studentService.applyJob(jobId);
        alert(res.msg || "Applied successfully!");
        await this.fetchJobs();
        await this.fetchApplications();
      } catch (err) {
        alert(err.response?.data?.msg || "Application failed.");
      }
    },
    async exportReport() {
      try {
        await adminService.generateReport();
        this.reportReady = true;
        alert("Placement report generated successfully!");
      } catch (err) {
        alert("Failed to generate report.");
      }
    },
    downloadReport() {
      if (!this.reportReady) {
        alert("Please click 'Generate Report' first.");
        return;
      }
      window.open("http://127.0.0.1:5000/admin/download-report/placement_report_latest.pdf");
    },
    async exportData() {
      try {
        await studentService.exportCSV();
        this.exportReady = true;
        alert("CSV Export task started! Click 'Download CSV' when ready.");
      } catch (err) {
        alert("Export failed.");
      }
    },
    downloadCSV() {
      const userId = localStorage.getItem("user_id");
      window.open(`http://127.0.0.1:5000/student/download/export_${userId}.csv`);
    },
    async updateProfile() {
      try {
        await studentService.updateProfile(this.profile);
        await this.fetchProfile();
        localStorage.setItem("user_name", this.profile.name);
        this.name = this.profile.name;
        alert("Profile updated successfully!");
      } catch (err) {
        alert(err.response?.data?.msg || "Update failed.");
      }
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
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-text h1 {
  font-size: 1.8rem;
  margin: 0;
  color: #ffffff;
}

.header-text p {
  margin: 0.2rem 0 0 0;
  color: #94a3b8;
  font-size: 0.9rem;
}

.header-actions {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.6rem 1rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
}

.btn-primary { background: #3b82f6; color: white; }
.btn-primary:hover { background: #2563eb; }

.btn-purple { background: #8b5cf6; color: white; }
.btn-purple:hover { background: #7c3aed; }

.btn-outline { background: transparent; border: 1px solid rgba(255, 255, 255, 0.2); color: #cbd5e1; }
.btn-outline:hover { background: rgba(255, 255, 255, 0.1); }

.btn-success { background: #10b981; color: white; }
.btn-success:hover { background: #059669; }

.btn-applied { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); cursor: default; }

.tab-navigation {
  display: flex;
  gap: 0.5rem;
  background: rgba(18, 24, 38, 0.6);
  padding: 0.4rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.tab-btn {
  flex: 1;
  padding: 0.65rem;
  background: transparent;
  border: none;
  color: #94a3b8;
  font-weight: 600;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-btn.active {
  background: #3b82f6;
  color: white;
}

.search-input {
  width: 100%;
  padding: 0.85rem 1.2rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(18, 24, 38, 0.8);
  color: white;
  font-size: 0.95rem;
  outline: none;
  box-sizing: border-box;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.data-card {
  background: rgba(18, 24, 38, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.25rem;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 1rem;
}

.card-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.card-title-row h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #f8fafc;
}

.company-tag {
  font-size: 0.78rem;
  color: #60a5fa;
  background: rgba(59, 130, 246, 0.15);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}

.card-desc {
  font-size: 0.85rem;
  color: #94a3b8;
  line-height: 1.4;
  margin: 0 0 0.75rem 0;
}

.card-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: #cbd5e1;
}

.skills-list {
  font-size: 0.8rem;
  color: #a7f3d0;
  margin: 0.5rem 0 0 0;
}

.app-card {
  align-items: stretch;
}

.app-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-badge {
  padding: 0.25rem 0.6rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
}

.status-badge.applied { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
.status-badge.selected, .status-badge.offer { background: rgba(16, 185, 129, 0.2); color: #34d399; }
.status-badge.rejected { background: rgba(239, 68, 68, 0.2); color: #f87171; }
.status-badge.shortlisted, .status-badge.interview { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }

.app-details {
  font-size: 0.85rem;
  color: #cbd5e1;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.offer-link {
  color: #34d399;
  font-weight: 600;
  text-decoration: none;
}

.profile-card-container {
  background: rgba(18, 24, 38, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 12px;
}

.form-section {
  margin-bottom: 2rem;
}

.form-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  color: #60a5fa;
  border-left: 3px solid #3b82f6;
  padding-left: 0.6rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-stack {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  text-align: left;
}

.form-group label {
  font-size: 0.8rem;
  color: #cbd5e1;
  font-weight: 600;
}

.form-control {
  padding: 0.65rem 0.85rem;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(10, 14, 23, 0.6);
  color: white;
  font-size: 0.9rem;
  outline: none;
}

.form-control.textarea {
  min-height: 90px;
  resize: vertical;
}

.btn-save {
  width: 100%;
  padding: 0.85rem;
  background: #3b82f6;
  color: white;
  font-size: 1rem;
}
</style>