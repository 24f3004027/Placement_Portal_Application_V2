<template>
  <div class="dashboard">
    <div class="top-bar">
      <h1>Welcome, {{ companyName }}</h1>
      
      <div style="display: flex; gap: 10px;">
        <button class="edit-profile-btn" @click="openProfileEdit">
          Edit Profile
        </button>
        <button class="logout-btn" @click="logout">Logout</button>
      </div>
    </div>

    <div class="main-content">
      <div v-if="showProfileForm" class="form-container">
        <div class="section-header">
          <h2>Edit Company Profile</h2>
          <button class="close-btn" @click="showProfileForm = false">✕</button>
        </div>

        <input v-model="profileForm.name" placeholder="Company Name" />
        <input v-model="profileForm.email" placeholder="Email" />
        <input v-model="profileForm.password" type="password" placeholder="New Password (optional)" />

        <button class="btn-save" @click="updateProfile">
          Save Changes
        </button>
      </div>
      <div class="cards-grid">
        <div class="card">
          <p class="card-label">Jobs Posted</p>
          <h2 class="card-value">{{ summary.jobs_posted }}</h2>
        </div>

        <div class="card clickable" @click="viewApplicants">
          <p class="card-label">Candidates Applied</p>
          <h2 class="card-value">{{ summary.candidates_applied }}</h2>
          <span class="card-action">View Applicants →</span>
        </div>

        <div class="card clickable" @click="viewShortlisted">
          <p class="card-label">Shortlisted</p>
          <h2 class="card-value">{{ summary.candidates_shortlisted }}</h2>
          <span class="card-action">View List →</span>
        </div>
      </div>

      <div v-if="showApplicants" class="section-container">
        <div class="section-header">
          <h2>Candidate Applications</h2>
          <button class="close-btn" @click="showApplicants = false">✕</button>
        </div>
        
        <div v-for="a in applicants" :key="a.application_id" class="item-card">
          <div class="item-info">
            <h3>{{ a.student_name }}</h3>
            <p><b>Applied For:</b> {{ a.job_title }} | <b>CGPA:</b> {{ a.cgpa }}</p>
          </div>

          <div v-if="!a.status || a.status === 'applied'" class="action-area">
            <textarea v-model="a.feedback" placeholder="Add feedback..." class="feedback-input"></textarea>
            <div class="btn-group">
              <button class="btn-shortlist" @click="handleDecision(a, 'shortlisted')">Shortlist</button>
              <button class="btn-reject" @click="handleDecision(a, 'rejected')">Reject</button>
            </div>
          </div>

          <div v-else class="status-badge" :class="a.status">
            <p><strong>Status:</strong> {{ a.status.toUpperCase() }}</p>
            <p v-if="a.feedback"><strong>Feedback:</strong> {{ a.feedback }}</p>
            <p v-if="a.status === 'shortlisted'" style="font-size: 0.85rem; margin-top: 5px; color: #166534;">
              <i>Go to "Shortlisted List" to schedule the interview.</i>
            </p>
          </div>
        </div>
      </div>

      <div v-if="showShortlisted" class="section-container">
        <div class="section-header">
          <h2>Shortlisted Candidates</h2>
          <button class="close-btn" @click="showShortlisted = false">✕</button>
        </div>

        <div v-if="shortlistedStudents.length === 0" class="empty-state">No shortlisted candidates yet.</div>

        <div class="table-container" v-else>
          <table class="styled-table">
            <thead>
              <tr>
                <th>Candidate Details</th>
                <th>Position</th>
                <th>Interview Scheduling</th>
                <th>Resume</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in shortlistedStudents" :key="s.application_id">
                <td>
                  <b>{{ s.name }}</b><br>
                  <small>{{ s.department }} | {{ s.cgpa }} CGPA</small>
                </td>
                <td>{{ s.job_title }}</td>
                <td>
                  <div v-if="s.status === 'shortlisted' && !s.interview_date">
                    <input type="datetime-local" v-model="s.temp_date" class="interview-input" />
                    <input type="text" v-model="s.temp_link" placeholder="Meeting Link" class="interview-input" />
                    <button class="btn-shortlist" style="padding: 5px 10px; font-size: 0.8rem;" @click="scheduleInterview(s)">
                      Set Interview
                    </button>
                  </div>

                  <div v-else-if="s.status === 'shortlisted' && s.interview_date">
                    <div class="status-tag active" style="padding: 8px; display: block; text-align: center; margin-bottom: 5px;">
                      📅 {{ s.interview_date }}<br>
                      <a :href="s.interview_link" target="_blank" style="color: inherit; font-size: 0.75rem;">Join Meeting</a>
                    </div>
                    
                    <div class="btn-group" style="justify-content: center; gap: 5px;">
                      <button 
                        class="btn-shortlist" 
                        style="padding: 4px 8px; font-size: 0.75rem;" 
                        @click="finalDecision(s, 'selected')"
                      >
                        Select
                      </button>
                      <button 
                        class="btn-reject" 
                        style="padding: 4px 8px; font-size: 0.75rem;" 
                        @click="finalDecision(s, 'rejected')"
                      >
                        Reject
                      </button>
                    </div>
                  </div>

                  <div v-else>
                    <div :class="['status-badge', s.status]" style="margin: 0; padding: 10px; text-align: center;">
                       <strong style="text-transform: uppercase;">{{ s.status }}</strong>
                       <p v-if="s.status === 'selected'" style="font-size: 0.7rem; margin: 5px 0 0;">Candidate Hired</p>
                    </div>
                  </div>
                </td>
                <td>
                  <a v-if="s.resume" :href="s.resume" target="_blank" class="resume-link">View</a>
                  <span v-else>No File</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <hr class="divider" />

      <div class="section-header">
        <h2>Active Job Listings</h2>
        <button class="create-btn" @click="toggleForm">
          {{ showForm ? "Cancel" : "+ Create Job" }}
        </button>
      </div>

      <div v-if="showForm" class="form-container">
        <input v-model="newJob.title" placeholder="Job Title" />
        <div class="input-row">
          <input v-model="newJob.location" placeholder="Location" />
          <input v-model="newJob.salary" placeholder="Salary" type="number" />
        </div>
        <textarea v-model="newJob.description" placeholder="Job Description"></textarea>
        <button class="btn-save" @click="saveJob">
          {{ editingJobId ? "Update Listing" : "Post Job" }}
        </button>
      </div>

      <div class="jobs-list">
        <div v-for="job in jobs" :key="job.id" class="item-card" :class="{ 'job-closed': job.status === 'closed' }">
          <div class="item-header">
            <div>
              <h3>{{ job.title }} 
                <span :class="['status-tag', job.status]">{{ job.status }}</span>
              </h3>
              <p class="text-muted">{{ job.location }} • ${{ job.salary }}</p>
            </div>
            <div class="item-actions">
              <button v-if="job.status === 'active'" class="btn-icon warning" @click="toggleJobStatus(job, 'close')">Close</button>
              <button v-else class="btn-icon success-alt" @click="toggleJobStatus(job, 'open')">Reopen</button>
              <button class="btn-icon" @click="startEdit(job)">Edit</button>
              <button class="btn-icon delete" @click="deleteJob(job.id)">Delete</button>
            </div>
          </div>
          <p>{{ job.description }}</p>
        </div>
      </div>

      <p v-if="loading" class="loading-overlay">Loading...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      companyName: localStorage.getItem("name"),
      jobs: [],
      applicants: [],
      shortlistedStudents: [],
      loading: true,
      showForm: false,
      showApplicants: false,
      showShortlisted: false,
      editingJobId: null,
      summary: { jobs_posted: 0, candidates_applied: 0, candidates_shortlisted: 0 },
      newJob: { title: "", location: "", salary: "", description: "" },
      showProfileForm: false,
      profileForm: {
      name: "",
      email: "",
      password: ""
      }
    };
  },
  mounted() {
    this.initData();
  },
  methods: {
    async initData() {
      await this.fetchSummary();
      await this.fetchJobs();
      this.loading = false;
    },
    async openProfileEdit() {
      const token = localStorage.getItem("access_token");

      try {
          const res = await axios.get("http://127.0.0.1:5000/company/profile", {
            headers: { Authorization: `Bearer ${token}` }
          });

          // Fill form with backend data
          this.profileForm.name = res.data.name;
          this.profileForm.email = res.data.email;
          this.profileForm.password = "";

          this.showProfileForm = true;

        } catch (err) {
          console.error("Profile load failed:", err);
        }
      },

      async updateProfile() {
        const token = localStorage.getItem("access_token");

        try {
          await axios.put(
            "http://127.0.0.1:5000/company/profile",
            this.profileForm,
            { headers: { Authorization: `Bearer ${token}` } }
          );

          alert("Profile updated successfully");

          this.companyName = this.profileForm.name;
          localStorage.setItem("name", this.profileForm.name);

          this.showProfileForm = false;

        } catch (err) {
           
          if (err.response && err.response.data && err.response.data.msg) {
            alert(err.response.data.msg);
          } 
          else {
            alert("Something went wrong");
          }
          
          console.error("Profile update failed:", err);
        }
      },
    async fetchSummary() {
      const token = localStorage.getItem("access_token");
      try {
        const res = await axios.get("http://127.0.0.1:5000/company/dashboard", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.summary = res.data;
      } catch (err) { console.error("Summary Load Failed:", err); }
    },

    async viewApplicants() {
      const token = localStorage.getItem("access_token");
      try {
        const res = await axios.get("http://127.0.0.1:5000/company/applicants", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.applicants = res.data;
        this.showApplicants = true;
        this.showShortlisted = false;
      } catch (err) { console.error("Applicants View Failed:", err); }
    },

    async viewShortlisted() {
      const token = localStorage.getItem("access_token");
      try {
        const res = await axios.get("http://127.0.0.1:5000/company/shortlisted", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.shortlistedStudents = res.data.map(s => ({ ...s, temp_date: "", temp_link: "" }));
        this.showShortlisted = true;
        this.showApplicants = false;
      } catch (err) { console.error("Shortlist View Failed:", err); }
    },

    async handleDecision(applicant, status) {
      const token = localStorage.getItem("access_token");
      try {
        await axios.post(`http://127.0.0.1:5000/company/application/${applicant.application_id}/decision`, 
          { status: status, feedback: applicant.feedback },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        applicant.status = status;
        await this.fetchSummary(); 
      } catch (err) { console.error(err); }
    },

    async finalDecision(applicant, decision) {
      const token = localStorage.getItem("access_token");
      try {
        await axios.put(
          `http://127.0.0.1:5000/company/application/${applicant.application_id}/final`,
          { decision: decision },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        alert("Final decision saved");
        await this.viewShortlisted(); 
        await this.fetchSummary();     
      } catch (err) {
        console.error(err);
      }
    },

    async scheduleInterview(student) {
      const token = localStorage.getItem("access_token");
      if (!student.temp_date || !student.temp_link) {
        alert("Please select a date and enter a link.");
        return;
      }

      try {
        await axios.put(
          `http://127.0.0.1:5000/company/application/${student.application_id}/schedule`,
          { date: student.temp_date, link: student.temp_link },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        alert("Interview Scheduled Successfully");
        await this.viewShortlisted();
      } catch (err) { console.error("Interview Scheduling Failed:", err); }
    },

    async fetchJobs() {
      const token = localStorage.getItem("access_token");
      try {
        const res = await axios.get("http://127.0.0.1:5000/company/jobs", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.jobs = res.data;
      } catch (err) { this.$router.push("/login"); }
    },

    async saveJob() {
      const token = localStorage.getItem("access_token");
      try {
        const payload = { ...this.newJob, salary: parseInt(this.newJob.salary) };
        if (this.editingJobId) {
          await axios.put(`http://127.0.0.1:5000/company/jobs/${this.editingJobId}`, payload, {
            headers: { Authorization: `Bearer ${token}` }
          });
        } else {
          await axios.post("http://127.0.0.1:5000/company/jobs", payload, {
            headers: { Authorization: `Bearer ${token}` }
          });
        }
        this.showForm = false;
        await this.fetchJobs();
        await this.fetchSummary();
      } catch (err) { console.error(err); }
    },

    async toggleJobStatus(job, action) {
      const token = localStorage.getItem("access_token");
      try {
        await axios.put(`http://127.0.0.1:5000/company/jobs/${job.id}/${action}`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
        job.status = (action === 'close') ? 'closed' : 'active';
      } catch (err) { console.error(err); }
    },

    startEdit(job) {
      this.newJob = { ...job };
      this.editingJobId = job.id;
      this.showForm = true;
    },

    async deleteJob(jobId) {
      const token = localStorage.getItem("access_token");
      if (!confirm("Delete this job?")) return;
      try {
        await axios.delete(`http://127.0.0.1:5000/company/jobs/${jobId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        await this.fetchJobs();
        await this.fetchSummary();
      } catch (err) { console.error(err); }
    },

    toggleForm() { 
      this.editingJobId = null; 
      this.newJob = { title: "", location: "", salary: "", description: "" }; 
      this.showForm = !this.showForm; 
    },
    
    logout() { 
      localStorage.clear(); 
      this.$router.push("/login"); 
    }
  }
};
</script>

<style scoped>
  .dashboard { background: #f8fafc; min-height: 100vh; font-family: sans-serif; color: #1e293b; }
  .main-content { max-width: 1000px; margin: 0 auto; padding: 2rem; }
  .top-bar { background: white; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e8f0; }
  .cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2.5rem; }
  .card { background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; text-align: center; }
  .card.clickable { cursor: pointer; transition: transform 0.2s; }
  .card.clickable:hover { transform: translateY(-4px); border-color: #4f46e5; }
  .item-card { background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 1rem; }
  .interview-input { width: 100%; padding: 8px; margin-bottom: 8px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; }
  .table-container { overflow-x: auto; background: white; border-radius: 8px; border: 1px solid #e2e8f0; }
  .styled-table { width: 100%; border-collapse: collapse; }
  .styled-table th, .styled-table td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #f1f5f9; }
  .styled-table th { background: #f8fafc; color: #64748b; font-size: 0.8rem; text-transform: uppercase; }
  .resume-link { color: #4f46e5; text-decoration: none; font-weight: bold; }
  .status-tag { font-size: 0.7rem; padding: 2px 8px; border-radius: 12px; text-transform: uppercase; vertical-align: middle; }
  .status-tag.active { background: #dcfce7; color: #166534; }
  .status-tag.closed { background: #fee2e2; color: #991b1b; }
  button { border-radius: 6px; padding: 0.6rem 1.2rem; cursor: pointer; font-weight: 600; border: none; }
  .btn-shortlist { background: #22c55e; color: white; }
  .btn-reject { background: #ef4444; color: white; }
  .create-btn { background: #4f46e5; color: white; }
  .btn-save { background: #1e293b; color: white; width: 100%; margin-top: 10px; }
  .btn-icon { background: #f1f5f9; font-size: 0.8rem; margin-left: 5px; padding: 5px 10px; }
  .form-container { background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #4f46e5; margin-bottom: 2rem; }
  .form-container input, .form-container textarea { width: 100%; padding: 0.8rem; margin: 0.5rem 0; border: 1px solid #e2e8f0; border-radius: 6px; box-sizing: border-box; }
  .input-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .section-header { display: flex; justify-content: space-between; align-items: center; margin: 2rem 0 1rem; }
  .divider { border: 0; border-top: 1px solid #e2e8f0; margin: 3rem 0; }
  .status-badge { margin-top: 1rem; padding: 1rem; border-radius: 8px; }
  .status-badge.shortlisted { background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; }
  .status-badge.rejected { background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; }
  .status-badge.selected { background: #eef2ff; border: 1px solid #c7d2fe; color: #3730a3; }
</style>