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
        <button @click="nextStep" :disabled="selectedPdfs.length === 0" class="btn btn-primary">
          Next ({{ selectedPdfs.length }} selected)
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
      </div>

      <div class="form-group" v-if="selectedProvider === 'openai'">
        <label>OpenAI API Key</label>
        <input 
          v-model="apiKey" 
          type="password" 
          placeholder="sk-..."
          autocomplete="off"
        >
        <small class="help-text">Your API key is stored securely and only used for this knowledge base</small>
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
        <ul>
          <li v-for="pdf in selectedPdfs" :key="pdf.url">{{ pdf.filename }}</li>
        </ul>
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
    const loading = ref(false)
    const creating = ref(false)
    const error = ref('')
    const kbName = ref('')
    const selectedModel = ref('')
    const selectedProvider = ref('openai')  // Default to OpenAI (easier setup)
    const apiKey = ref('')
    const createdKBId = ref(null)
    const successMessage = ref('')

    const pdfs = computed(() => store.pdfs)
    const selectedPdfs = computed(() => store.selectedPdfs)
    const models = computed(() => store.models)
    const allSelected = computed(() => 
      pdfs.value.length > 0 && selectedPdfs.value.length === pdfs.value.length
    )
    const canCreate = computed(() => {
      if (!kbName.value) return false
      if (selectedProvider.value === 'openai' && !apiKey.value) return false
      return true
    })

    onMounted(async () => {
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
        urlInput.value = ''
        toast.success(`Found ${response.data.total} PDFs`)
      } catch (err) {
        error.value = 'Failed to scan URL: ' + err.message
        toast.error('Failed to scan URL')
      } finally {
        loading.value = false
      }
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
      step.value = 2
    }

    async function createKB() {
      if (!kbName.value.trim()) {
        toast.warning('Please enter a knowledge base name')
        return
      }
      
      if (selectedProvider.value === 'openai' && !apiKey.value) {
        toast.warning('Please enter your OpenAI API key')
        return
      }
      
      if (selectedPdfs.value.length === 0) {
        toast.warning('Please select at least one PDF')
        return
      }
      
      creating.value = true
      error.value = ''
      
      try {
        const response = await api.createKB({
          name: kbName.value,
          model_id: selectedModel.value,
          provider: selectedProvider.value,
          api_key: selectedProvider.value === 'openai' ? apiKey.value : null,
          documents: selectedPdfs.value.map(pdf => ({
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
      creating,
      error,
      kbName,
      selectedModel,
      selectedProvider,
      apiKey,
      createdKBId,
      successMessage,
      pdfs,
      selectedPdfs,
      models,
      allSelected,
      canCreate,
      scanUrl,
      togglePdf,
      toggleAll,
      isSelected,
      addMoreUrls,
      nextStep,
      onProviderChange,
      createKB
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
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 1rem;
}

.card.success {
  background: #d4edda;
  border: 1px solid #c3e6cb;
  text-align: center;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.help-text {
  display: block;
  margin-top: 0.25rem;
  color: #666;
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

table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}

th, td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background: #f5f5f5;
  font-weight: 600;
}

.selected-docs {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  margin: 1rem 0;
}

.selected-docs ul {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0 0 0;
}

.selected-docs li {
  padding: 0.25rem 0;
}

.actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.error {
  background: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}
</style>
