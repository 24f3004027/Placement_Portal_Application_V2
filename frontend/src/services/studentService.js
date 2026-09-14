import API from "./api";

export const studentService = {
  async getDashboard() {
    const res = await API.get("/student/dashboard");
    return res.data;
  },

  async getJobs() {
    const res = await API.get("/student/jobs");
    return res.data;
  },

  async applyJob(jobId) {
    const res = await API.post(`/student/apply/${jobId}`);
    return res.data;
  },

  async getApplications() {
    const res = await API.get("/student/applications");
    return res.data;
  },

  async getProfile() {
    const res = await API.get("/student/profile");
    return res.data;
  },

  async updateProfile(profileData) {
    const res = await API.put("/student/profile", profileData);
    return res.data;
  },

  async exportCSV() {
    const res = await API.post("/student/export");
    return res.data;
  }
};
