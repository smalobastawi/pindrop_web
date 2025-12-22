<template>
  <AdminLayout>
    <div class="admin-backup">
      <div class="page-header">
        <h1>System Backup</h1>
        <p>Manage system backups and restore operations</p>
      </div>
      
      <div class="content-placeholder">
        <i class="icon-database"></i>
        <h2>System Backup</h2>
        <p>This section will provide backup management:</p>
        <ul>
          <li>Create manual system backups</li>
          <li>Configure automatic backup schedules</li>
          <li>Monitor backup status and progress</li>
          <li>Restore from previous backups</li>
          <li>Manage backup storage and retention</li>
        </ul>
        <p><em>This feature is coming soon!</em></p>
      </div>
    </div>
  </AdminLayout>
</template>

<script>
import AdminLayout from '@/components/admin/AdminLayout.vue'

export default {
  name: 'AdminBackup',
  components: {
    AdminLayout
  }
}
</script>

<style scoped>
.admin-backup {
  padding: 0;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.page-header p {
  color: #6c757d;
  font-size: 1.1rem;
  margin: 0;
}

.content-placeholder {
  background: white;
  padding: 3rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
}

.content-placeholder i {
  font-size: 4rem;
  color: #6c757d;
  margin-bottom: 1rem;
}

.content-placeholder h2 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.content-placeholder p {
  color: #6c757d;
  margin-bottom: 1rem;
}

.content-placeholder ul {
  text-align: left;
  max-width: 500px;
  margin: 0 auto 1.5rem;
  color: #495057;
}

.content-placeholder li {
  margin-bottom: 0.5rem;
}

.content-placeholder em {
  color: #007bff;
  font-style: italic;
}
</style>