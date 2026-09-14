import API from "./api";

export const companyService = {
  async getDashboard() {
    const res = await API.get("/company/dashboard");
    return res.data;
  },

  async createJob(jobData) {
    const res = await API.post("/company/jobs", jobData);
    return res.data;
  },

  async getJobs() {
    const res = await API.get("/company/jobs");
    return res.data;
  },

  async updateJob(jobId, jobData) {
    const res = await API.put(`/company/jobs/${jobId}`, jobData);
    return res.data;
  },

  async deleteJob(jobId) {
    const res = await API.delete(`/company/jobs/${jobId}`);
    return res.data;
  },

  async getApplicants() {
    const res = await API.get("/company/applicants");
    return res.data;
  },

  async decideApplication(appId, status, feedback) {
    const res = await API.post(`/company/application/${appId}/decision`, { status, feedback });
    return res.data;
  },

  async scheduleInterview(appId, interviewDate, interviewLink) {
    const res = await API.put(`/company/application/${appId}/schedule`, {
      interview_date: interviewDate,
      interview_link: interviewLink
    });
    return res.data;
  },

  async exportCSV() {
    const res = await API.post("/company/export");
    return res.data;
  }
};
