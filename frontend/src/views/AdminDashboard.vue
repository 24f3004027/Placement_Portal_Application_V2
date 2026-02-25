<template>
  <div class="dashboard">
    <nav class="navbar">
      <h1>Admin Control Panel</h1>
      <div class="nav-right">
        <span>Logged in as: Admin</span>
        <button class="logout-btn" @click="logout">Logout</button>
      </div>
    </nav>
    

    <div class="container">
      <div class="stats-grid">
        <div class="stat-card">
          <h3>Students</h3>
          <p class="number">{{ students.length }}</p>
          <button @click="currentView = 'students'" class="view-btn">View Students</button>
        </div>
        <div class="stat-card">
          <h3>Companies</h3>
          <p class="number">{{ companies.length }}</p>
          <button @click="currentView = 'companies'" class="view-btn">View Companies</button>
        </div>
      </div>

      <div v-if="currentView" class="table-container">
        <h2>List of {{ currentView === 'students' ? 'Students' : 'Companies' }}</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Status</th>
              <th v-if="currentView === 'companies'">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in (currentView === 'students' ? students : companies)" :key="user.ids">
              <td>{{ user.ids }}</td>
              <td>{{ user.name }}</td>
              <td>{{ user.email }}</td>
              <td>
                <span :class="user.is_approved ? 'text-success' : 'text-danger'">
                  {{ user.is_approved ? 'Approved' : 'Pending/Blacklisted' }}
                </span>
              </td>
              <td v-if="currentView === 'companies'">
                <button v-if="!user.is_approved" @click="toggleApproval(user.ids)" class="approve-btn">Approve</button>
                <button v-else @click="toggleApproval(user.ids)" class="blacklist-btn">Blacklist</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      students: [],
      companies: [],
      currentView: 'companies' // Default to showing companies
    }
  },
  methods: {
    async loadData() {
      try {
        const token = localStorage.getItem('access_token');
        // This hits the backend to get the real numbers from the DB
        const res = await axios.get('http://127.0.0.1:5000/admin/dashboard', {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        // Note: Ensure your backend sends back the lists. 
        // If your current /admin/dashboard only sends a msg, 
        // we need to make sure the data is actually in the response.
        this.students = res.data.students || [];
        this.companies = res.data.companies || [];
      } catch (err) {
        console.error("Failed to load DB data:", err);
      }
    },
    async toggleApproval(userId) {
      try {
        const token = localStorage.getItem('access_token');
        // This hits your existing @app.route('/admin/approve/<int:user_id>')
        await axios.post(`http://127.0.0.1:5000/admin/approve/${userId}`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.loadData(); // Refresh the numbers immediately
      } catch (err) {
        alert("Action failed!");
      }
    },
    logout() {
      localStorage.clear();
      this.$router.push("/login");
    }
  },
  mounted() {
    this.loadData(); // This runs when the page opens
  }
}
</script>

<style scoped>
.dashboard { background: #f0f2f5; min-height: 100vh; font-family: sans-serif; }
.navbar { background: #007bff; color: white; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; }
.container { padding: 2rem; max-width: 1200px; margin: auto; }
.stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 2rem; }
.stat-card { background: white; padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
.number { font-size: 3rem; font-weight: bold; color: #007bff; margin: 10px 0; }
.table-container { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
th, td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
.approve-btn { background: #28a745; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; }
.blacklist-btn { background: #dc3545; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; }
.view-btn { background: #6c757d; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
.logout-btn { background: #ff4d4d; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
.text-success { color: #28a745; font-weight: bold; }
.text-danger { color: #dc3545; font-weight: bold; }
</style>