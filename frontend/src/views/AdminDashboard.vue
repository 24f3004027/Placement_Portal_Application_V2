<template>
  <div class="dashboard-page">
    <div class="dashboard-header">
      <div class="header-text">
        <h1>Administrator Control Panel</h1>
        <p>Manage system users, company approvals, job drive audits, and placement reports</p>
      </div>

      <div class="header-actions">
        <button class="btn btn-purple" @click="generateReport">📊 Trigger PDF Report</button>
        <button class="btn btn-success" @click="downloadReport">📥 Download Report</button>
      </div>
    </div>

    <!-- Stats Summary Cards -->
    <div class="stats-grid">
      <div class="stat-card" :class="{ 'active-card': currentView === 'students' }" @click="currentView = 'students'">
        <div class="stat-icon">🎓</div>
        <div class="stat-info">
          <p class="stat-label">Total Students</p>
          <h2 class="stat-value">{{ stats.total_students }}</h2>
        </div>
      </div>

      <div class="stat-card" :class="{ 'active-card': currentView === 'companies' }" @click="currentView = 'companies'">
        <div class="stat-icon">🏢</div>
        <div class="stat-info">
          <p class="stat-label">Total Companies</p>
          <h2 class="stat-value">{{ stats.total_companies }}</h2>
        </div>
      </div>

      <div class="stat-card" :class="{ 'active-card': currentView === 'jobs' }" @click="showJobs">
        <div class="stat-icon">💼</div>
        <div class="stat-info">
          <p class="stat-label">Total Job Openings</p>
          <h2 class="stat-value">{{ stats.total_jobs }}</h2>
        </div>
      </div>

      <div class="stat-card" :class="{ 'active-card': currentView === 'applications' }" @click="showApplications">
        <div class="stat-icon">📑</div>
        <div class="stat-info">
          <p class="stat-label">Total Applications</p>
          <h2 class="stat-value">{{ stats.total_applications }}</h2>
        </div>
      </div>
    </div>

    <!-- Search input -->
    <div class="search-bar-container">
      <input 
        v-model="searchQuery" 
        :placeholder="'🔍 Filter ' + currentView + ' by name, email, or title...'" 
        class="search-input"
      />
    </div>

    <!-- Table Views -->
    <div v-if="currentView === 'students' || currentView === 'companies'" class="data-table-card">
      <div class="table-header-row">
        <h3>Directory of {{ currentView === 'students' ? 'Students' : 'Companies' }}</h3>
      </div>
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Approval Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredUsers" :key="user.ids">
              <td>#{{ user.ids }}</td>
              <td><strong>{{ user.name }}</strong></td>
              <td>{{ user.email }}</td>
              <td>
                <span class="status-pill" :class="user.is_approved ? 'approved' : 'pending'">
                  {{ user.is_approved ? 'Approved' : 'Pending / Blacklisted' }}
                </span>
              </td>
              <td>
                <button 
                  v-if="!user.is_approved" 
                  @click="toggleApproval(user.ids)" 
                  class="btn btn-sm btn-success">
                  Approve
                </button>
                <button 
                  v-else 
                  @click="toggleApproval(user.ids)" 
                  class="btn btn-sm btn-danger">
                  Blacklist
                </button>
              </td>
            </tr>
            <tr v-if="filteredUsers.length === 0">
              <td colspan="5" class="empty-text">No records matching "{{ searchQuery }}"</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="currentView === 'jobs'" class="data-table-card">
      <div class="table-header-row">
        <h3>All Job Listings</h3>
      </div>
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Job Title</th>
              <th>Company</th>
              <th>Location</th>
              <th>Salary (₹/yr)</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="job in filteredJobs" :key="job.id">
              <td>#{{ job.id }}</td>
              <td><strong>{{ job.title }}</strong></td>
              <td>🏢 {{ job.company_name }}</td>
              <td>{{ job.location || 'Remote' }}</td>
              <td>₹{{ job.salary ? job.salary.toLocaleString() : 'N/A' }}</td>
              <td>
                <span class="status-pill" :class="job.status">{{ job.status }}</span>
              </td>
              <td>
                <button class="btn btn-sm btn-danger" @click="deleteJob(job.id)">Delete Drive</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="currentView === 'applications'" class="data-table-card">
      <div class="table-header-row">
        <h3>All Applications</h3>
      </div>
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Candidate Name</th>
              <th>Email</th>
              <th>Job Position</th>
              <th>Company</th>
              <th>Status</th>
              <th>Interview Schedule</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="app in filteredApplications" :key="app.application_id">
              <td>#{{ app.application_id }}</td>
              <td><strong>{{ app.student_name }}</strong></td>
              <td>{{ app.student_email }}</td>
              <td>{{ app.job_title }}</td>
              <td>🏢 {{ app.company_name }}</td>
              <td>
                <span class="status-pill" :class="app.status">{{ (app.status || 'applied').toUpperCase() }}</span>
              </td>
              <td>
                <div v-if="app.interview_date">
                  📅 {{ app.interview_date }}<br>
                  <a v-if="app.interview_link" :href="app.interview_link" target="_blank" class="link-meet">Join Call</a>
                </div>
                <span v-else class="text-muted">—</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { adminService } from "../services/adminService";

export default {
  name: "AdminDashboard",
  data() {
    return {
      students: [],
      companies: [],
      currentView: 'companies',
      stats: {
        total_students: 0,
        total_companies: 0,
        total_jobs: 0,
        total_applications: 0
      },
      applications: [],
      jobs: [],
      searchQuery: ""
    };
  },
  computed: {
    filteredUsers() {
      const list = this.currentView === 'students' ? this.students : this.companies;
      const q = this.searchQuery.toLowerCase();
      return list.filter(u =>
        (u.name && u.name.toLowerCase().includes(q)) ||
        (u.email && u.email.toLowerCase().includes(q))
      );
    },
    filteredJobs() {
      const q = this.searchQuery.toLowerCase();
      return this.jobs.filter(j =>
        (j.title && j.title.toLowerCase().includes(q)) ||
        (j.company_name && j.company_name.toLowerCase().includes(q))
      );
    },
    filteredApplications() {
      const q = this.searchQuery.toLowerCase();
      return this.applications.filter(a =>
        (a.student_name && a.student_name.toLowerCase().includes(q)) ||
        (a.job_title && a.job_title.toLowerCase().includes(q))
      );
    }
  },
  async mounted() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      try {
        const data = await adminService.getDashboard();
        this.students = data.students || [];
        this.companies = data.companies || [];
        this.stats.total_students = data.total_students;
        this.stats.total_companies = data.total_companies;
        this.stats.total_jobs = data.total_jobs;
        this.stats.total_applications = data.total_applications;
      } catch (err) {
        console.error("Failed to load admin dashboard data", err);
      }
    },
    showJobs() {
      this.currentView = 'jobs';
      this.loadJobs();
    },
    async loadJobs() {
      try {
        this.jobs = await adminService.getJobs();
      } catch (err) {
        console.error("Failed to load jobs", err);
      }
    },
    showApplications() {
      this.currentView = 'applications';
      this.loadApplications();
    },
    async loadApplications() {
      try {
        this.applications = await adminService.getApplications();
      } catch (err) {
        console.error("Failed to load applications", err);
      }
    },
    async deleteJob(jobId) {
      if (!confirm("Are you sure you want to delete this job?")) return;
      try {
        await adminService.deleteJob(jobId);
        alert("Job deleted successfully!");
        await this.loadJobs();
        await this.loadData();
      } catch (err) {
        alert("Delete failed");
      }
    },
    async toggleApproval(userId) {
      try {
        await adminService.toggleUser(userId);
        await this.loadData();
      } catch (err) {
        alert("Action failed");
      }
    },
    async generateReport() {
      try {
        await adminService.generateReport();
        alert("Report generated successfully!");
      } catch (err) {
        alert("Report generation failed");
      }
    },
    downloadReport() {
      window.open("http://127.0.0.1:5000/admin/download-report/placement_report_latest.pdf");
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

.header-text h1 { font-size: 1.8rem; margin: 0; color: white; }
.header-text p { margin: 0.2rem 0 0 0; color: #94a3b8; font-size: 0.9rem; }
.header-actions { display: flex; gap: 0.5rem; }

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: rgba(18, 24, 38, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.stat-card:hover, .stat-card.active-card {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
  transform: translateY(-2px);
}

.stat-icon { font-size: 2rem; }
.stat-label { margin: 0; font-size: 0.8rem; color: #94a3b8; font-weight: 600; }
.stat-value { margin: 0.2rem 0 0 0; font-size: 1.75rem; color: white; }

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

.data-table-card {
  background: rgba(18, 24, 38, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1.5rem;
}

.table-header-row h3 { margin: 0 0 1rem 0; color: white; }
.table-wrapper { overflow-x: auto; }

.data-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
.data-table th, .data-table td { padding: 0.85rem; text-align: left; border-bottom: 1px solid rgba(255, 255, 255, 0.08); color: #cbd5e1; }
.data-table th { background: rgba(10, 14, 23, 0.6); color: #94a3b8; font-weight: 600; }

.btn { padding: 0.6rem 1rem; border-radius: 6px; font-weight: 600; font-size: 0.85rem; cursor: pointer; border: none; }
.btn-purple { background: #8b5cf6; color: white; }
.btn-success { background: #10b981; color: white; }
.btn-danger { background: #ef4444; color: white; }
.btn-sm { padding: 0.35rem 0.65rem; font-size: 0.78rem; }

.status-pill { font-size: 0.75rem; padding: 0.2rem 0.5rem; border-radius: 12px; font-weight: 700; text-transform: uppercase; }
.status-pill.approved, .status-pill.active, .status-pill.selected { background: rgba(16, 185, 129, 0.2); color: #34d399; }
.status-pill.pending, .status-pill.rejected { background: rgba(239, 68, 68, 0.2); color: #f87171; }
.status-pill.shortlisted { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }

.link-meet { color: #60a5fa; font-weight: 600; text-decoration: none; }
.empty-text { text-align: center; padding: 2rem; color: #94a3b8; font-style: italic; }
</style>