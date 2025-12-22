<template>
  <AdminLayout>
    <div class="admin-profile">
      <div class="page-header">
        <h1>My Profile</h1>
        <p>Manage your admin profile and preferences</p>
      </div>
      
      <div class="content-placeholder">
        <i class="icon-user"></i>
        <h2>Admin Profile</h2>
        <p>This section will provide profile management:</p>
        <ul>
          <li>View and edit personal information</li>
          <li>Change password and security settings</li>
          <li>Manage notification preferences</li>
          <li>Update contact information</li>
          <li>View login history and activity</li>
        </ul>
        <p><em>This feature is coming soon!</em></p>
      </div>
    </div>
  </AdminLayout>
</template>

<script>
import AdminLayout from '@/components/admin/AdminLayout.vue'

export default {
  name: 'AdminProfile',
  components: {
    AdminLayout
  }
}
</script>

<style scoped>
.admin-profile {
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