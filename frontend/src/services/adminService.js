import API from "./api";

export const adminService = {
  async getDashboard() {
    const res = await API.get("/admin/dashboard");
    return res.data;
  },

  async approveCompany(userId) {
    const res = await API.post(`/admin/approve/${userId}`);
    return res.data;
  },

  async toggleUser(userId) {
    const res = await API.post(`/admin/toggle/${userId}`);
    return res.data;
  },

  async getJobs() {
    const res = await API.get("/admin/jobs");
    return res.data;
  },

  async deleteJob(jobId) {
    const res = await API.delete(`/admin/jobs/${jobId}`);
    return res.data;
  },

  async getApplications() {
    const res = await API.get("/admin/applications");
    return res.data;
  },

  async generateReport() {
    const res = await API.get("/admin/generate-report");
    return res.data;
  }
};
