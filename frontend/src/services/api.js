import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

export default {
  // Scan URL for PDFs
  scanUrl(url) {
    return api.post('/scan-url', { url })
  },

  // Get models (Bedrock or OpenAI)
  getModels(provider = 'bedrock') {
    return api.get(`/${provider}/models`)
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
  createKB(data) {
    return api.post('/kb', data)
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
  chat(kbId, message) {
    return api.post(`/kb/${kbId}/chat`, { message })
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
