<template>
  <div class="dashboard">

    <h1>Welcome {{ companyName }}</h1>

    <div class="cards">

      <div class="card">
        <h3>People Applied</h3>
        <p class="count">{{ peopleApplied.length }}</p>
      </div>

      <div class="card">
        <h3>Job Posts</h3>
        <p class="count">{{ jobPosts.length }}</p>
      </div>

    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      companyName: localStorage.getItem("name"),
      peopleApplied: [],
      jobPosts: []
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 40px;
  font-family: Arial, sans-serif;
}

h1 {
  margin-bottom: 30px;
}

.cards {
  display: flex;
  gap: 20px;
}

.card {
  background: #f5f5f5;
  padding: 20px;
  border-radius: 10px;
  width: 200px;
  text-align: center;
}

.count {
  font-size: 28px;
  font-weight: bold;
}
</style>