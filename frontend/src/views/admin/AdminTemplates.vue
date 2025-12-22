<template>
  <AdminLayout>
    <div class="admin-templates">
      <div class="page-header">
        <h1>Notification Templates</h1>
        <p>Manage email and SMS notification templates</p>
      </div>
      
      <div class="content-placeholder">
        <i class="icon-mail"></i>
        <h2>Notification Templates</h2>
        <p>This section will provide template management:</p>
        <ul>
          <li>Create and edit email templates</li>
          <li>Manage SMS notification templates</li>
          <li>Customize notification variables</li>
          <li>Preview templates before sending</li>
          <li>Template usage analytics</li>
        </ul>
        <p><em>This feature is coming soon!</em></p>
      </div>
    </div>
  </AdminLayout>
</template>

<script>
import AdminLayout from '@/components/admin/AdminLayout.vue'

export default {
  name: 'AdminTemplates',
  components: {
    AdminLayout
  }
}
</script>

<style scoped>
.admin-templates {
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