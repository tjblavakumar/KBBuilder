<template>
  <div class="home">
    <div class="header">
      <h2>Knowledge Bases</h2>
      <router-link to="/create" class="btn btn-primary">+ Create New</router-link>
    </div>
    <p class="subtitle">Manage your AI-powered knowledge bases</p>
    
    <div v-if="loading" class="loading">Loading...</div>
    
    <div v-else-if="kbs.length === 0" class="empty-state">
      <p>No knowledge bases yet. Create your first one!</p>
      <router-link to="/create" class="btn btn-primary">Create Knowledge Base</router-link>
    </div>

    <div v-else class="kb-grid">
      <div v-for="kb in kbs" :key="kb.id" class="kb-card">
        <div class="kb-header">
          <h3>{{ kb.name }}</h3>
          <div class="kb-actions">
            <button @click="viewDetails(kb.id)" class="btn-icon" title="View Details">📋</button>
            <button @click="editKB(kb.id)" class="btn-icon" title="Edit">✏️</button>
            <button @click="confirmDelete(kb.id)" class="btn-icon" title="Delete">🗑️</button>
          </div>
        </div>
        <div class="kb-info">
          <p><strong>Provider:</strong> {{ kb.provider === 'bedrock' ? 'AWS Bedrock' : 'OpenAI' }}</p>
          <p><strong>Model:</strong> {{ kb.model_id }}</p>
          <p><strong>Documents:</strong> {{ kb.document_count }}</p>
          <p><strong>Created:</strong> {{ formatDate(kb.created_at) }}</p>
        </div>
        <router-link :to="`/chat/${kb.id}`" class="btn btn-primary btn-block">Start Chat</router-link>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal" @click.self="showDeleteModal = false">
      <div class="modal-content">
        <h3>Delete Knowledge Base?</h3>
        <p>This will permanently delete the knowledge base and all associated data.</p>
        <div class="modal-actions">
          <button @click="showDeleteModal = false" class="btn btn-secondary">Cancel</button>
          <button @click="deleteKB" :disabled="deleting" class="btn btn-danger">
            {{ deleting ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal" @click.self="showEditModal = false">
      <div class="modal-content">
        <h3>Edit Knowledge Base</h3>
        <div class="form-group">
          <label>Name</label>
          <input v-model="editName" type="text">
        </div>
        <div class="modal-actions">
          <button @click="showEditModal = false" class="btn btn-secondary">Cancel</button>
          <button @click="saveEdit" :disabled="saving" class="btn btn-primary">
            {{ saving ? 'Saving...' : 'Save' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Details Modal -->
    <div v-if="showDetailsModal" class="modal" @click.self="showDetailsModal = false">
      <div class="modal-content large">
        <h3>{{ kbDetails?.name }}</h3>
        <div class="details-section">
          <p><strong>Provider:</strong> {{ kbDetails?.provider === 'bedrock' ? 'AWS Bedrock' : 'OpenAI' }}</p>
          <p><strong>Model:</strong> {{ kbDetails?.model_id }}</p>
          <p><strong>Created:</strong> {{ formatDate(kbDetails?.created_at) }}</p>
          <p><strong>Updated:</strong> {{ formatDate(kbDetails?.updated_at) }}</p>
        </div>
        <div class="details-section">
          <h4>Documents ({{ kbDetails?.document_count }})</h4>
          <table>
            <thead>
              <tr>
                <th>Filename</th>
                <th>Pages</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="doc in kbDetails?.documents" :key="doc.id">
                <td>{{ doc.filename }}</td>
                <td>{{ doc.page_count }}</td>
                <td><span :class="'status-' + doc.status">{{ doc.status }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="modal-actions">
          <button @click="showDetailsModal = false" class="btn btn-secondary">Close</button>
        </div>
      </div>
    </div>

    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import { useToast } from '../composables/useToast'

export default {
  name: 'HomeView',
  setup() {
    const toast = useToast()
    const kbs = ref([])
    const loading = ref(true)
    const error = ref('')
    const showDeleteModal = ref(false)
    const showEditModal = ref(false)
    const showDetailsModal = ref(false)
    const deleteKBId = ref(null)
    const editKBId = ref(null)
    const editName = ref('')
    const deleting = ref(false)
    const saving = ref(false)
    const kbDetails = ref(null)

    onMounted(async () => {
      await loadKBs()
    })

    async function loadKBs() {
      loading.value = true
      error.value = ''
      try {
        const response = await api.listKBs()
        kbs.value = response.data.knowledge_bases
      } catch (err) {
        error.value = 'Failed to load knowledge bases: ' + err.message
        toast.error('Failed to load knowledge bases')
      } finally {
        loading.value = false
      }
    }

    function confirmDelete(kbId) {
      deleteKBId.value = kbId
      showDeleteModal.value = true
    }

    async function deleteKB() {
      deleting.value = true
      try {
        await api.deleteKB(deleteKBId.value)
        showDeleteModal.value = false
        toast.success('Knowledge base deleted successfully')
        await loadKBs()
      } catch (err) {
        error.value = 'Failed to delete KB: ' + err.message
        toast.error('Failed to delete knowledge base')
      } finally {
        deleting.value = false
      }
    }

    function editKB(kbId) {
      const kb = kbs.value.find(k => k.id === kbId)
      if (kb) {
        editKBId.value = kbId
        editName.value = kb.name
        showEditModal.value = true
      }
    }

    async function saveEdit() {
      if (!editName.value.trim()) {
        toast.warning('Please enter a name')
        return
      }
      
      saving.value = true
      try {
        await api.updateKB(editKBId.value, { name: editName.value })
        showEditModal.value = false
        toast.success('Knowledge base updated successfully')
        await loadKBs()
      } catch (err) {
        error.value = 'Failed to update KB: ' + err.message
        toast.error('Failed to update knowledge base')
      } finally {
        saving.value = false
      }
    }

    async function viewDetails(kbId) {
      try {
        const response = await api.getKB(kbId)
        kbDetails.value = response.data
        showDetailsModal.value = true
      } catch (err) {
        error.value = 'Failed to load details: ' + err.message
        toast.error('Failed to load details')
      }
    }

    function formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
    }

    return {
      kbs,
      loading,
      error,
      showDeleteModal,
      showEditModal,
      showDetailsModal,
      deleting,
      saving,
      editName,
      kbDetails,
      confirmDelete,
      deleteKB,
      editKB,
      saveEdit,
      viewDetails,
      formatDate
    }
  }
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  margin-bottom: 2rem;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: #f5f5f5;
  border-radius: 8px;
}

.empty-state p {
  margin-bottom: 1.5rem;
  color: #666;
}

.kb-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.kb-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.kb-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.kb-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1rem;
}

.kb-header h3 {
  margin: 0;
  font-size: 1.25rem;
}

.kb-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-icon {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.25rem;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.btn-icon:hover {
  opacity: 1;
}

.kb-info {
  margin-bottom: 1rem;
}

.kb-info p {
  margin: 0.5rem 0;
  color: #666;
  font-size: 0.9rem;
}

.btn-block {
  width: 100%;
  text-align: center;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
}

.modal-content.large {
  max-width: 800px;
}

.modal-content h3 {
  margin-top: 0;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #c82333;
}

.details-section {
  margin: 1.5rem 0;
}

.details-section h4 {
  margin-bottom: 0.75rem;
}

.details-section table {
  width: 100%;
  border-collapse: collapse;
}

.details-section th,
.details-section td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.details-section th {
  background: #f5f5f5;
  font-weight: 600;
}

.status-completed {
  color: #28a745;
  font-weight: 500;
}

.status-processing {
  color: #ffc107;
  font-weight: 500;
}

.status-failed {
  color: #dc3545;
  font-weight: 500;
}

.error {
  background: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}
</style>
