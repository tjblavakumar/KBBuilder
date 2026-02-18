import axios from 'axios'
import { useSessionApiKey } from '../composables/useSessionApiKey'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

const { openaiApiKey } = useSessionApiKey()

api.interceptors.request.use((config) => {
  if (openaiApiKey.value) {
    config.headers['X-Session-OpenAI-Key'] = openaiApiKey.value
  } else if (config.headers && config.headers['X-Session-OpenAI-Key']) {
    delete config.headers['X-Session-OpenAI-Key']
  }
  return config
})

export default {
  // Scan URL for PDFs
  scanUrl(url) {
    return api.post('/scan-url', { url })
  },

  // Validate PDF URLs
  validatePdfs(urls) {
    return api.post('/validate-pdfs', { urls })
  },

  // Get models (Bedrock or OpenAI)
  getModels(provider = 'bedrock') {
    return api.get(`/${provider}/models`)
  },

  // Validate OpenAI API key
  validateOpenAIKey(apiKey) {
    return api.post('/openai/validate-key', { api_key: apiKey })
  },

  // List all KBs
  listKBs() {
    return api.get('/kb')
  },

  // Get KB details
  getKB(kbId) {
    return api.get(`/kb/${kbId}`)
  },

  // Create knowledge base
  createKB(data, apiKey = null) {
    return api.post('/kb', {
      ...data,
      api_key: apiKey
    })
  },

  // Update KB
  updateKB(kbId, data) {
    return api.put(`/kb/${kbId}`, data)
  },

  // Delete KB
  deleteKB(kbId) {
    return api.delete(`/kb/${kbId}`)
  },

  // Chat with KB
  chat(kbId, message, apiKey = null) {
    return api.post(`/kb/${kbId}/chat`, {
      message,
      api_key: apiKey
    })
  },

  // Get chat history
  getHistory(kbId) {
    return api.get(`/kb/${kbId}/history`)
  },

  // Cleanup old history
  cleanupHistory(kbId) {
    return api.delete(`/kb/${kbId}/history/cleanup`)
  }
}
