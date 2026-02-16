<template>
  <div class="create-kb">
    <h2>Create Knowledge Base</h2>
    
    <!-- Step 1: Scan URLs -->
    <div class="card" v-if="step === 1">
      <h3>Step 1: Discover PDFs</h3>
      <div class="form-group">
        <label>Enter Website URL</label>
        <div class="input-group">
          <input 
            v-model="urlInput" 
            type="text" 
            placeholder="https://example.com/documents"
            @keyup.enter="scanUrl"
          >
          <button @click="scanUrl" :disabled="loading" class="btn btn-primary">
            {{ loading ? 'Scanning...' : 'Scan' }}
          </button>
        </div>
      </div>

      <div v-if="pdfs.length > 0" class="pdf-list">
        <h4>Found {{ pdfs.length }} PDFs</h4>
        <table>
          <thead>
            <tr>
              <th><input type="checkbox" @change="toggleAll" :checked="allSelected"></th>
              <th>Filename</th>
              <th>Size</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="pdf in pdfs" :key="pdf.url">
              <td><input type="checkbox" :checked="isSelected(pdf)" @change="togglePdf(pdf)"></td>
              <td>{{ pdf.filename }}</td>
              <td>{{ pdf.size }}</td>
            </tr>
          </tbody>
        </table>
        <button @click="addMoreUrls" class="btn btn-secondary">Add More URLs</button>
        <button @click="nextStep" :disabled="selectedPdfs.length === 0 || validating" class="btn btn-primary">
          {{ validating ? 'Validating...' : `Next (${selectedPdfs.length} selected)` }}
        </button>
      </div>
    </div>

    <!-- Step 2: Configure KB -->
    <div class="card" v-if="step === 2">
      <h3>Step 2: Configure Knowledge Base</h3>
      <div class="form-group">
        <label>Knowledge Base Name</label>
        <input v-model="kbName" type="text" placeholder="My Knowledge Base">
      </div>

      <div class="form-group">
        <label>Select Provider</label>
        <select v-model="selectedProvider" @change="onProviderChange">
          <option value="bedrock">AWS Bedrock</option>
          <option value="openai">OpenAI</option>
        </select>
        <small class="help-text" v-if="selectedProvider === 'openai'">
          Using API key from backend/config.yml
        </small>
        <small class="help-text" v-if="selectedProvider === 'bedrock'">
          Using AWS credentials from your profile
        </small>
      </div>

      <div class="form-group">
        <label>Select Model</label>
        <select v-model="selectedModel">
          <option v-for="model in models" :key="model.model_id" :value="model.model_id">
            {{ model.model_name }}
          </option>
        </select>
      </div>

      <div class="selected-docs">
        <h4>Selected Documents ({{ selectedPdfs.length }})</h4>
        <div class="validation-summary" v-if="Object.keys(validationResults).length > 0">
          <span class="available">✓ {{ getAvailablePdfs().length }} Available</span>
          <span class="unavailable" v-if="selectedPdfs.length - getAvailablePdfs().length > 0">
            ✗ {{ selectedPdfs.length - getAvailablePdfs().length }} Unavailable
          </span>
        </div>
        <ul>
          <li v-for="pdf in selectedPdfs" :key="pdf.url" :class="getValidationStatus(pdf).status">
            {{ pdf.filename }}
            <span class="status-badge" v-if="getValidationStatus(pdf).status === 'unavailable'">
              ✗ {{ getValidationStatus(pdf).reason }}
            </span>
            <span class="status-badge available" v-if="getValidationStatus(pdf).status === 'available'">
              ✓
            </span>
          </li>
        </ul>
        <p class="info-text" v-if="selectedPdfs.length - getAvailablePdfs().length > 0">
          Note: Only available PDFs will be included in the knowledge base
        </p>
      </div>

      <div class="actions">
        <button @click="step = 1" class="btn btn-secondary">Back</button>
        <button @click="createKB" :disabled="!canCreate || creating" class="btn btn-primary">
          {{ creating ? 'Creating...' : 'Build KB' }}
        </button>
      </div>
    </div>

    <!-- Step 3: Success -->
    <div class="card success" v-if="step === 3">
      <h3>✓ Knowledge Base Created!</h3>
      <p>{{ successMessage }}</p>
      <div class="actions">
        <router-link :to="`/chat/${createdKBId}`" class="btn btn-primary">Start Chatting</router-link>
        <router-link to="/" class="btn btn-secondary">Go Home</router-link>
      </div>
    </div>

    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useKBStore } from '../stores/kb'
import { useToast } from '../composables/useToast'
import api from '../services/api'

export default {
  name: 'CreateKBView',
  setup() {
    const router = useRouter()
    const store = useKBStore()
    const toast = useToast()
    
    const step = ref(1)
    const urlInput = ref('')
    const scannedUrl = ref('')  // Store the scanned URL for KB name
    const loading = ref(false)
    const validating = ref(false)
    const creating = ref(false)
    const error = ref('')
    const kbName = ref('')
    const selectedModel = ref('')
    const selectedProvider = ref('openai')  // Default to OpenAI (easier setup)
    const createdKBId = ref(null)
    const successMessage = ref('')
    const validationResults = ref({})  // Store validation status for each PDF

    const pdfs = computed(() => store.pdfs)
    const selectedPdfs = computed(() => store.selectedPdfs)
    const models = computed(() => store.models)
    const allSelected = computed(() => 
      pdfs.value.length > 0 && selectedPdfs.value.length === pdfs.value.length
    )
    const canCreate = computed(() => {
      if (!kbName.value) return false
      return true
    })

    onMounted(async () => {
      // Reset the state when entering the create KB page
      store.resetCreateKBState()
      await loadModels()
    })

    async function loadModels() {
      try {
        const endpoint = selectedProvider.value === 'bedrock' ? 'bedrock' : 'openai'
        const response = await api.getModels(endpoint)
        store.setModels(response.data.models, response.data.default_model)
        selectedModel.value = response.data.default_model
      } catch (err) {
        error.value = 'Failed to load models: ' + err.message
        toast.error(`Failed to load ${selectedProvider.value} models`)
      }
    }

    async function onProviderChange() {
      await loadModels()
    }

    async function scanUrl() {
      if (!urlInput.value) {
        toast.warning('Please enter a URL')
        return
      }
      
      loading.value = true
      error.value = ''
      
      try {
        const response = await api.scanUrl(urlInput.value)
        store.setPdfs([...store.pdfs, ...response.data.pdfs])
        scannedUrl.value = urlInput.value  // Store for KB name generation
        urlInput.value = ''
        toast.success(`Found ${response.data.total} PDFs`)
      } catch (err) {
        error.value = 'Failed to scan URL: ' + err.message
        toast.error('Failed to scan URL')
      } finally {
        loading.value = false
      }
    }

    function extractDomain(url) {
      try {
        const urlObj = new URL(url)
        return urlObj.hostname.replace('www.', '')
      } catch {
        return 'unknown'
      }
    }

    async function validateAndProceed() {
      if (selectedPdfs.value.length === 0) {
        toast.warning('Please select at least one PDF')
        return
      }

      validating.value = true
      error.value = ''

      try {
        // Validate all selected PDFs
        const response = await api.validatePdfs(
          selectedPdfs.value.map(pdf => ({
            url: pdf.url,
            filename: pdf.filename
          }))
        )

        // Store validation results
        validationResults.value = {}
        response.data.results.forEach(result => {
          validationResults.value[result.url] = {
            status: result.status,
            reason: result.reason
          }
        })

        // Count available vs unavailable
        const available = response.data.results.filter(r => r.status === 'available').length
        const unavailable = response.data.results.filter(r => r.status === 'unavailable').length

        if (unavailable > 0) {
          toast.warning(`${available} available, ${unavailable} unavailable`)
        } else {
          toast.success(`All ${available} PDFs are available`)
        }

        // Generate default KB name from domain
        if (scannedUrl.value) {
          const domain = extractDomain(scannedUrl.value)
          kbName.value = `KB_${domain}`
        }

        // Move to step 2
        step.value = 2

      } catch (err) {
        error.value = 'Failed to validate PDFs: ' + err.message
        toast.error('Failed to validate PDFs')
      } finally {
        validating.value = false
      }
    }

    function getValidationStatus(pdf) {
      const result = validationResults.value[pdf.url]
      return result || { status: 'unknown', reason: '' }
    }

    function getAvailablePdfs() {
      return selectedPdfs.value.filter(pdf => {
        const status = getValidationStatus(pdf)
        return status.status === 'available'
      })
    }

    function togglePdf(pdf) {
      store.togglePdf(pdf)
    }

    function toggleAll() {
      if (allSelected.value) {
        store.clearSelectedPdfs()
      } else {
        pdfs.value.forEach(pdf => {
          if (!isSelected(pdf)) {
            store.togglePdf(pdf)
          }
        })
      }
    }

    function isSelected(pdf) {
      return selectedPdfs.value.some(p => p.url === pdf.url)
    }

    function addMoreUrls() {
      urlInput.value = ''
    }

    function nextStep() {
      validateAndProceed()
    }

    async function createKB() {
      if (!kbName.value.trim()) {
        toast.warning('Please enter a knowledge base name')
        return
      }
      
      const availablePdfs = getAvailablePdfs()
      
      if (availablePdfs.length === 0) {
        toast.error('No available PDFs to create knowledge base')
        return
      }
      
      creating.value = true
      error.value = ''
      
      try {
        const response = await api.createKB({
          name: kbName.value,
          model_id: selectedModel.value,
          provider: selectedProvider.value,
          api_key: null,  // Always null - backend will use config
          documents: availablePdfs.map(pdf => ({
            filename: pdf.filename,
            url: pdf.url
          }))
        })
        
        createdKBId.value = response.data.id
        successMessage.value = response.data.message
        step.value = 3
        toast.success('Knowledge base created successfully!')
      } catch (err) {
        error.value = 'Failed to create KB: ' + err.message
        toast.error('Failed to create knowledge base')
      } finally {
        creating.value = false
      }
    }

    return {
      step,
      urlInput,
      loading,
      validating,
      creating,
      error,
      kbName,
      selectedModel,
      selectedProvider,
      createdKBId,
      successMessage,
      pdfs,
      selectedPdfs,
      models,
      allSelected,
      canCreate,
      validationResults,
      scanUrl,
      togglePdf,
      toggleAll,
      isSelected,
      addMoreUrls,
      nextStep,
      onProviderChange,
      createKB,
      getValidationStatus,
      getAvailablePdfs
    }
  }
}
</script>

<style scoped>
.create-kb {
  max-width: 900px;
  margin: 0 auto;
}

.card {
  background: var(--glass-white);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border-glass);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: var(--shadow-glass);
  margin-bottom: 1rem;
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: var(--shadow-glass-hover);
}

.card.success {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  text-align: center;
  color: white;
}

.card h3 {
  color: white;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: white;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-glass);
  border-radius: 8px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  color: white;
  transition: all 0.3s ease;
}

.form-group input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--border-glass-hover);
  background: rgba(255, 255, 255, 0.15);
}

.help-text {
  display: block;
  margin-top: 0.25rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.875rem;
}

.input-group {
  display: flex;
  gap: 0.5rem;
}

.input-group input {
  flex: 1;
}

.pdf-list {
  margin-top: 2rem;
}

.pdf-list h4 {
  color: white;
  margin-bottom: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  overflow: hidden;
}

th, td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--border-glass);
  color: white;
}

th {
  background: rgba(255, 255, 255, 0.1);
  font-weight: 600;
}

tr:hover {
  background: rgba(255, 255, 255, 0.05);
}

.selected-docs {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  border: 1px solid var(--border-glass);
}

.selected-docs h4 {
  color: white;
  margin-bottom: 0.5rem;
}

.selected-docs ul {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0 0 0;
}

.selected-docs li {
  padding: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
  border-radius: 4px;
  margin-bottom: 0.25rem;
  transition: all 0.3s ease;
}

.selected-docs li:hover {
  background: rgba(255, 255, 255, 0.05);
}

.selected-docs li.unavailable {
  color: rgba(255, 182, 193, 1);
  text-decoration: line-through;
  opacity: 0.7;
}

.selected-docs li.available {
  color: rgba(255, 255, 255, 1);
  font-weight: 500;
}

.status-badge {
  font-size: 0.85rem;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  background: rgba(255, 182, 193, 0.3);
  color: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(255, 182, 193, 0.5);
  font-weight: 500;
}

.status-badge.available {
  background: rgba(144, 238, 144, 0.3);
  color: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(144, 238, 144, 0.5);
}

.validation-summary {
  margin: 0.5rem 0;
  font-size: 0.9rem;
}

.validation-summary .available {
  color: rgba(255, 255, 255, 1);
  margin-right: 1rem;
  font-weight: 600;
}

.validation-summary .unavailable {
  color: rgba(255, 182, 193, 1);
  font-weight: 600;
}

.info-text {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.9);
  background: rgba(240, 147, 251, 0.2);
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid rgba(240, 147, 251, 0.3);
}

.actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
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
