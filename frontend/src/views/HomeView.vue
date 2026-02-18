<template>
  <div class="home">
    <div class="header">
      <h2>Knowledge Bases</h2>
      <router-link to="/create" class="btn btn-primary">+ New KB</router-link>
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

.header h2 {
  color: white;
  font-size: 2rem;
  font-weight: 700;
}

.subtitle {
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 2rem;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: white;
  font-size: 1.1rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: var(--glass-white);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border-glass);
  border-radius: 16px;
  box-shadow: var(--shadow-glass);
}

.empty-state p {
  margin-bottom: 1.5rem;
  color: white;
  font-size: 1.1rem;
}

.kb-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.kb-card {
  background: var(--glass-white);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1.5px solid rgba(255, 255, 255, 0.3);
  padding: 1.5rem;
  border-radius: 16px;
  box-shadow:
    0 12px 28px rgba(15, 23, 42, 0.22),
    0 2px 6px rgba(79, 70, 229, 0.25);
  transition: all 0.3s ease;
}

.kb-card:hover {
  transform: translateY(-4px);
  box-shadow:
    0 18px 36px rgba(15, 23, 42, 0.28),
    0 4px 12px rgba(79, 70, 229, 0.35);
  border-color: rgba(255, 255, 255, 0.5);
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
  color: white;
}

.kb-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-icon {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid var(--border-glass);
  border-radius: 8px;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.4rem 0.6rem;
  transition: all 0.3s ease;
}

.btn-icon:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.kb-info {
  margin-bottom: 1rem;
}

.kb-info p {
  margin: 0.5rem 0;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
}

.kb-info strong {
  color: white;
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
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--glass-white-strong);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border: 1px solid var(--border-glass);
  padding: 2rem;
  border-radius: 16px;
  max-width: 500px;
  width: 90%;
  box-shadow: var(--shadow-glass-hover);
}

.modal-content.large {
  max-width: 800px;
}

.modal-content h3 {
  margin-top: 0;
  color: white;
}

.modal-content p,
.modal-content label {
  color: rgba(255, 255, 255, 0.9);
}

.modal-content input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-glass);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 1rem;
}

.modal-content input:focus {
  outline: none;
  border-color: var(--border-glass-hover);
  background: rgba(255, 255, 255, 0.15);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.details-section {
  margin: 1.5rem 0;
}

.details-section h4 {
  margin-bottom: 0.75rem;
  color: white;
}

.details-section p {
  color: rgba(255, 255, 255, 0.9);
}

.details-section table {
  width: 100%;
  border-collapse: collapse;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  overflow: hidden;
}

.details-section th,
.details-section td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--border-glass);
  color: white;
}

.details-section th {
  background: rgba(255, 255, 255, 0.1);
  font-weight: 600;
}

.status-completed {
  color: rgba(255, 255, 255, 1);
  font-weight: 600;
}

.status-processing {
  color: rgba(255, 223, 186, 1);
  font-weight: 600;
}

.status-failed {
  color: rgba(255, 182, 193, 1);
  font-weight: 600;
}

.error {
  background: rgba(245, 87, 108, 0.2);
  color: white;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  border: 1px solid rgba(245, 87, 108, 0.4);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
</style>
