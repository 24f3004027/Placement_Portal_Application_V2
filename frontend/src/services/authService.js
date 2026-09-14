import API from "./api";

export const authService = {
  async login(email, password) {
    const res = await API.post("/login", { email, password });
    if (res.data.access_token) {
      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("role", res.data.role);
      localStorage.setItem("user_name", res.data.name);
      localStorage.setItem("user_id", res.data.user_id);
    }
    return res.data;
  },

  async register(name, email, password, role) {
    const res = await API.post("/req", { name, email, password, role });
    return res.data;
  },

  logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("role");
    localStorage.removeItem("user_name");
    localStorage.removeItem("user_id");
  }
};
