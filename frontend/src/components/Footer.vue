<template>
  <footer class="app-footer">
    <div class="footer-content">
      <p class="copyleft-text">
        🄯 Copyleft 2026 Ramrup Satpati | All Rights Reversed | Released under the GNU General Public License (GPLv3)
      </p>
      <div class="footer-meta">
        <span>Modern Application Development II (MAD-II)</span>
        <span class="dot">•</span>
        <span>IIT Madras BS Degree Program</span>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer"
};
</script>

<style scoped>
.app-footer {
  margin-top: auto;
  padding: 1.5rem 2rem;
  background: rgba(10, 14, 23, 0.9);
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  text-align: center;
  color: #94a3b8;
  font-size: 0.85rem;
}

.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
}

.copyleft-text {
  margin: 0;
  color: #cbd5e1;
  font-family: monospace;
}

.footer-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.78rem;
  color: #64748b;
}

.dot {
  color: #475569;
}
</style>
