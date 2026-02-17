<template>
  <div class="dashboard">
    <h1>Welcome {{ name }}</h1>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: localStorage.getItem("name")
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 40px;
  font-size: 22px;
}
</style>