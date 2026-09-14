<template>
  <div class="dashboard-page">
    <div class="dashboard-header">
      <div class="header-text">
        <h1>Recruiter Dashboard</h1>
        <p>Manage job drives, evaluate candidate applications, and schedule interview rounds</p>
      </div>

      <div class="header-actions">
        <button class="btn btn-outline" @click="openProfileEdit">⚙️ Profile Settings</button>
        <button class="btn btn-purple" @click="exportCompanyCSV">📤 Export CSV</button>
        <button class="btn btn-success" @click="downloadCompanyCSV" :disabled="!exportReady">💾 Download CSV</button>
        <button class="btn btn-outline" @click="generateReport">📊 Report PDF</button>
        <button class="btn btn-success" @click="downloadReport" :disabled="!reportFile">📥 Download PDF</button>
      </div>
    </div>

    <!-- Stats Summary Section -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">💼</div>
        <div class="stat-info">
          <p class="stat-label">Active Jobs Posted</p>
          <h2 class="stat-value">{{ summary.jobs_posted }}</h2>
        </div>
      </div>

      <div class="stat-card clickable" @click="viewApplicants()">
        <div class="stat-icon">👥</div>
        <div class="stat-info">
          <p class="stat-label">Candidates Applied</p>
          <h2 class="stat-value">{{ summary.candidates_applied }}</h2>
          <span class="stat-link">Review Applicants →</span>
        </div>
      </div>

      <div class="stat-card clickable" @click="viewShortlisted">
        <div class="stat-icon">⭐</div>
        <div class="stat-info">
          <p class="stat-label">Shortlisted Candidates</p>
          <h2 class="stat-value">{{ summary.candidates_shortlisted }}</h2>
          <span class="stat-link">Manage Shortlist →</span>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal / Form -->
    <div v-if="showProfileForm" class="modal-card">
      <div class="modal-header">
        <h3>Edit Company Profile</h3>
        <button class="btn-close" @click="showProfileForm = false">✕</button>
      </div>
      <div class="form-grid">
        <div class="form-group">
          <label>Company Name</label>
          <input v-model="profileForm.name" placeholder="Company Name" class="form-control" />
        </div>
        <div class="form-group">
          <label>Official Email</label>
          <input v-model="profileForm.email" placeholder="Email" class="form-control" />
        </div>
        <div class="form-group">
          <label>New Password (optional)</label>
          <input v-model="profileForm.password" type="password" placeholder="••••••••" class="form-control" />
        </div>
      </div>
      <button class="btn btn-primary btn-block" @click="updateProfile">Save Profile Changes</button>
    </div>

    <!-- Applicants Section -->
    <div v-if="showApplicants" class="modal-card">
      <div class="modal-header">
        <h3>Candidate Applications</h3>
        <button class="btn-close" @click="showApplicants = false">✕</button>
      </div>
      <div v-if="applicants.length === 0" class="empty-text">No candidate applications found.</div>
      <div v-for="a in applicants" :key="a.application_id" class="applicant-item">
        <div class="applicant-info">
          <h4>{{ a.student_name }}</h4>
          <p><strong>Position:</strong> {{ a.job_title }} | <strong>Department:</strong> {{ a.department || 'N/A' }} | <strong>CGPA:</strong> {{ a.cgpa || 'N/A' }}</p>
          <a v-if="a.resume" :href="a.resume" target="_blank" class="link-resume">📄 View Resume</a>
        </div>

        <div v-if="!a.status || a.status === 'applied'" class="decision-box">
          <textarea v-model="a.feedback" placeholder="Add candidate feedback..." class="form-control textarea-small"></textarea>
          <div class="btn-group">
            <button class="btn btn-success" @click="handleDecision(a, 'shortlisted')">Shortlist</button>
            <button class="btn btn-danger" @click="handleDecision(a, 'rejected')">Reject</button>
          </div>
        </div>
        <div v-else class="status-pill" :class="a.status">
          <strong>Status: {{ a.status.toUpperCase() }}</strong>
          <p v-if="a.feedback">Feedback: {{ a.feedback }}</p>
        </div>
      </div>
    </div>

    <!-- Shortlisted Section -->
    <div v-if="showShortlisted" class="modal-card">
      <div class="modal-header">
        <h3>Shortlisted Candidates & Interview Schedules</h3>
        <button class="btn-close" @click="showShortlisted = false">✕</button>
      </div>
      <div v-if="shortlistedStudents.length === 0" class="empty-text">No shortlisted candidates yet.</div>
      <div v-else class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Candidate</th>
              <th>Position</th>
              <th>Interview Scheduling / Final Offer</th>
              <th>Resume</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in shortlistedStudents" :key="s.application_id">
              <td>
                <strong>{{ s.name }}</strong><br>
                <small>{{ s.department }} | {{ s.cgpa }} CGPA</small>
              </td>
              <td>{{ s.job_title }}</td>
              <td>
                <div v-if="s.status === 'shortlisted' && !s.interview_date" class="schedule-inputs">
                  <input type="datetime-local" v-model="s.temp_date" class="form-control" />
                  <input type="text" v-model="s.temp_link" placeholder="Google Meet / Zoom Link" class="form-control" />
                  <button class="btn btn-primary" @click="scheduleInterview(s)">Schedule Interview</button>
                </div>

                <div v-else-if="s.status === 'shortlisted' || s.status === 'interview'" class="decision-inputs">
                  <div class="interview-badge">📅 {{ s.interview_date }}</div>
                  <input type="text" v-model="s.offer_letter" placeholder="Offer Letter URL" class="form-control" />
                  <div class="btn-group">
                    <button class="btn btn-success" @click="finalDecision(s, 'selected')">Offer Job</button>
                    <button class="btn btn-danger" @click="finalDecision(s, 'rejected')">Reject</button>
                  </div>
                </div>

                <div v-else>
                  <span class="status-pill" :class="s.status">{{ s.status.toUpperCase() }}</span>
                </div>
              </td>
              <td>
                <a v-if="s.resume" :href="s.resume" target="_blank" class="link-resume">View</a>
                <span v-else class="text-muted">None</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Active Job Drives Header -->
    <div class="section-title-row">
      <h2>Active Job Openings</h2>
      <button class="btn btn-primary" @click="toggleForm">
        {{ showForm ? "Cancel" : "+ Create New Job Drive" }}
      </button>
    </div>

    <!-- Create / Edit Job Form -->
    <div v-if="showForm" class="modal-card">
      <h3>{{ editingJobId ? "Edit Job Drive" : "Post New Job Opening" }}</h3>
      <div class="form-grid">
        <div class="form-group">
          <label>Job Title</label>
          <input v-model="newJob.title" placeholder="e.g. Software Engineer" class="form-control" />
        </div>
        <div class="form-group">
          <label>Location</label>
          <input v-model="newJob.location" placeholder="e.g. Remote / Bangalore" class="form-control" />
        </div>
        <div class="form-group">
          <label>Annual Salary (₹ / yr)</label>
          <input v-model="newJob.salary" type="number" placeholder="1200000" class="form-control" />
        </div>
        <div class="form-group">
          <label>Years of Experience Required</label>
          <input v-model.number="newJob.experience" type="number" placeholder="0" class="form-control" />
        </div>
      </div>
      <div class="form-group">
        <label>Job Description</label>
        <textarea v-model="newJob.description" placeholder="Role responsibilities..." class="form-control textarea"></textarea>
      </div>
      <div class="form-group">
        <label>Required Technical Skills</label>
        <input v-model="newJob.skills" placeholder="Python, SQL, Vue, Flask" class="form-control" />
      </div>
      <div class="form-group">
        <label>Benefits & Perks</label>
        <textarea v-model="newJob.benefits" placeholder="Health insurance, performance bonus..." class="form-control textarea-small"></textarea>
      </div>

      <button class="btn btn-primary btn-block" @click="saveJob">
        {{ editingJobId ? "Update Job Drive" : "Publish Job Opening" }}
      </button>
    </div>

    <!-- Job Cards List -->
    <div class="jobs-grid">
      <div v-if="jobs.length === 0" class="empty-text">No job drives posted yet.</div>
      <div v-for="job in jobs" :key="job.id" class="job-card-item" :class="{ 'closed-card': job.status === 'closed' }">
        <div class="job-card-header">
          <div>
            <h3>{{ job.title }} <span class="status-pill" :class="job.status">{{ job.status }}</span></h3>
            <p class="job-subtitle">📍 {{ job.location }} • ₹{{ job.salary ? job.salary.toLocaleString() : 'N/A' }}/yr</p>
          </div>
          <div class="card-actions">
            <button class="btn btn-sm btn-outline" @click="viewApplicants(job.id)">Applicants</button>
            <button v-if="job.status === 'active'" class="btn btn-sm btn-warning" @click="toggleJobStatus(job, 'close')">Close</button>
            <button v-else class="btn btn-sm btn-success" @click="toggleJobStatus(job, 'open')">Reopen</button>
            <button class="btn btn-sm btn-outline" @click="startEdit(job)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="deleteJob(job.id)">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { companyService } from "../services/companyService";
import { adminService } from "../services/adminService";

export default {
  name: "CompanyDashboard",
  data() {
    return {
      jobs: [],
      applicants: [],
      shortlistedStudents: [],
      reportReady: false,
      exportReady: false,
      reportFile: null,
      showForm: false,
      showApplicants: false,
      showShortlisted: false,
      editingJobId: null,
      summary: { jobs_posted: 0, candidates_applied: 0, candidates_shortlisted: 0 },
      newJob: {
        title: "",
        location: "",
        salary: "",
        description: "",
        skills: "",
        experience: 0,
        benefits: ""
      },
      showProfileForm: false,
      profileForm: { name: "", email: "", password: "" }
    };
  },
  async mounted() {
    await this.refreshDashboard();
  },
  methods: {
    async refreshDashboard() {
      try {
        this.summary = await companyService.getDashboard();
        this.jobs = await companyService.getJobs();
      } catch (err) {
        console.error("Dashboard load failed", err);
      }
    },
    async openProfileEdit() {
      this.showProfileForm = !this.showProfileForm;
    },
    async updateProfile() {
      try {
        await companyService.updateProfile(this.profileForm);
        alert("Company profile updated!");
        this.showProfileForm = false;
        await this.refreshDashboard();
      } catch (err) {
        alert(err.response?.data?.msg || "Update failed");
      }
    },
    async viewApplicants(jobId = null) {
      try {
        const data = await companyService.getApplicants();
        this.applicants = jobId ? data.filter(a => a.job_id === jobId) : data;
        this.showApplicants = true;
        this.showShortlisted = false;
      } catch (err) {
        console.error("Applicants fetch failed", err);
      }
    },
    async viewShortlisted() {
      try {
        const data = await companyService.getShortlisted();
        this.shortlistedStudents = data.map(s => ({
          ...s,
          temp_date: "",
          temp_link: "",
          offer_letter: ""
        }));
        this.showShortlisted = true;
        this.showApplicants = false;
      } catch (err) {
        console.error("Shortlist fetch failed", err);
      }
    },
    async handleDecision(applicant, status) {
      try {
        await companyService.decideApplication(applicant.application_id, status, applicant.feedback);
        applicant.status = status;
        await this.refreshDashboard();
      } catch (err) {
        alert("Decision failed");
      }
    },
    async finalDecision(applicant, decision) {
      try {
        await companyService.finalDecision(applicant.application_id, decision, applicant.offer_letter);
        alert("Decision recorded!");
        await this.viewShortlisted();
        await this.refreshDashboard();
      } catch (err) {
        alert(err.response?.data?.msg || "Decision failed");
      }
    },
    async scheduleInterview(student) {
      if (!student.temp_date || !student.temp_link) {
        alert("Please select a date and enter a meeting link.");
        return;
      }
      try {
        await companyService.scheduleInterview(student.application_id, student.temp_date, student.temp_link);
        alert("Interview scheduled!");
        await this.viewShortlisted();
        await this.refreshDashboard();
      } catch (err) {
        alert("Scheduling failed");
      }
    },
    async exportCompanyCSV() {
      try {
        await companyService.exportCSV();
        this.exportReady = true;
        alert("Export started! Click 'Download CSV' in a few seconds.");
      } catch (err) {
        alert("Export failed");
      }
    },
    downloadCompanyCSV() {
      const userId = localStorage.getItem("user_id");
      window.open(`http://127.0.0.1:5000/company/download/export_${userId}.csv`);
    },
    async generateReport() {
      try {
        await adminService.generateReport();
        this.reportFile = "placement_report_latest.pdf";
        alert("Report generated!");
      } catch (err) {
        alert("Report generation failed");
      }
    },
    downloadReport() {
      window.open("http://127.0.0.1:5000/admin/download-report/placement_report_latest.pdf");
    },
    async saveJob() {
      if (!this.newJob.title || !this.newJob.description || !this.newJob.skills) {
        alert("Title, description, and skills are required.");
        return;
      }
      try {
        if (this.editingJobId) {
          await companyService.updateJob(this.editingJobId, this.newJob);
        } else {
          await companyService.createJob(this.newJob);
        }
        alert("Job saved!");
        this.showForm = false;
        await this.refreshDashboard();
      } catch (err) {
        alert(err.response?.data?.msg || "Job save failed");
      }
    },
    async toggleJobStatus(job, action) {
      try {
        if (action === 'close') {
          await companyService.closeJob(job.id);
        } else {
          await companyService.openJob(job.id);
        }
        await this.refreshDashboard();
      } catch (err) {
        alert("Status update failed");
      }
    },
    async deleteJob(jobId) {
      if (!confirm("Are you sure you want to delete this job drive?")) return;
      try {
        await companyService.deleteJob(jobId);
        await this.refreshDashboard();
      } catch (err) {
        alert("Delete failed");
      }
    },
    startEdit(job) {
      this.newJob = { ...job };
      this.editingJobId = job.id;
      this.showForm = true;
    },
    toggleForm() {
      this.editingJobId = null;
      this.newJob = { title: "", location: "", salary: "", description: "", skills: "", experience: 0, benefits: "" };
      this.showForm = !this.showForm;
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
.header-actions { display: flex; gap: 0.5rem; flex-wrap: wrap; }

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
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
}

.stat-card.clickable {
  cursor: pointer;
  transition: transform 0.2s, border-color 0.2s;
}

.stat-card.clickable:hover {
  transform: translateY(-3px);
  border-color: #3b82f6;
}

.stat-icon { font-size: 2rem; }
.stat-label { margin: 0; font-size: 0.8rem; color: #94a3b8; font-weight: 600; }
.stat-value { margin: 0.2rem 0; font-size: 1.75rem; color: white; }
.stat-link { font-size: 0.78rem; color: #60a5fa; font-weight: 600; }

.modal-card {
  background: rgba(18, 24, 38, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  padding: 1.5rem;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.modal-header h3 { margin: 0; color: white; }
.btn-close { background: transparent; border: none; color: #ef4444; font-size: 1.2rem; cursor: pointer; }

.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1rem; }
.form-group { display: flex; flex-direction: column; gap: 0.3rem; text-align: left; margin-bottom: 0.75rem; }
.form-group label { font-size: 0.8rem; color: #cbd5e1; font-weight: 600; }

.form-control {
  padding: 0.65rem 0.85rem;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(10, 14, 23, 0.6);
  color: white;
  font-size: 0.9rem;
  outline: none;
}
.form-control.textarea { min-height: 90px; }
.form-control.textarea-small { min-height: 60px; }

.btn { padding: 0.6rem 1rem; border-radius: 6px; font-weight: 600; font-size: 0.85rem; cursor: pointer; border: none; }
.btn-primary { background: #3b82f6; color: white; }
.btn-purple { background: #8b5cf6; color: white; }
.btn-success { background: #10b981; color: white; }
.btn-danger { background: #ef4444; color: white; }
.btn-warning { background: #f59e0b; color: white; }
.btn-outline { background: transparent; border: 1px solid rgba(255, 255, 255, 0.2); color: #cbd5e1; }
.btn-block { width: 100%; margin-top: 1rem; }
.btn-sm { padding: 0.35rem 0.65rem; font-size: 0.78rem; }

.applicant-item {
  background: rgba(10, 14, 23, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 0.75rem;
}

.link-resume { color: #60a5fa; font-weight: 600; text-decoration: none; font-size: 0.85rem; }

.section-title-row { display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; }
.section-title-row h2 { color: white; margin: 0; }

.jobs-grid { display: flex; flex-direction: column; gap: 0.75rem; }
.job-card-item { background: rgba(18, 24, 38, 0.75); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 1rem 1.25rem; }
.job-card-header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; }
.job-card-header h3 { margin: 0; color: white; font-size: 1.1rem; }
.job-subtitle { margin: 0.2rem 0 0 0; font-size: 0.85rem; color: #94a3b8; }
.card-actions { display: flex; gap: 0.4rem; }

.status-pill { font-size: 0.75rem; padding: 0.2rem 0.5rem; border-radius: 12px; font-weight: 700; text-transform: uppercase; }
.status-pill.active { background: rgba(16, 185, 129, 0.2); color: #34d399; }
.status-pill.closed { background: rgba(239, 68, 68, 0.2); color: #f87171; }

.data-table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; font-size: 0.85rem; }
.data-table th, .data-table td { padding: 0.75rem; text-align: left; border-bottom: 1px solid rgba(255, 255, 255, 0.08); color: #cbd5e1; }
.data-table th { background: rgba(10, 14, 23, 0.6); color: #94a3b8; font-weight: 600; }
</style>