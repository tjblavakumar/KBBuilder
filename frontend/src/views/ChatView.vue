<template>
  <div class="chat-view">
    <div class="chat-header">
      <h2>{{ kbName }}</h2>
      <router-link to="/" class="btn btn-secondary">Back to Home</router-link>
    </div>

    <div class="chat-container">
      <div class="messages" ref="messagesContainer">
        <div v-for="(msg, index) in messages" :key="index" class="message-group">
          <div class="message user">
            <strong>You:</strong> {{ msg.user }}
          </div>
          <div class="message bot">
            <strong>Assistant:</strong>
            <div class="markdown-content" v-html="renderMarkdown(msg.bot)"></div>
            <div v-if="msg.sources && msg.sources.length > 0" class="sources">
              <details>
                <summary>Sources ({{ msg.sources.length }})</summary>
                <div v-for="(source, idx) in msg.sources" :key="idx" class="source">
                  <strong>{{ source.filename }}</strong> - Page {{ source.page_number }}
                  <p>{{ source.text }}</p>
                </div>
              </details>
            </div>
          </div>
        </div>
        
        <div v-if="loading" class="message bot loading">
          <strong>Assistant:</strong> Thinking...
        </div>
      </div>

      <div class="input-area">
        <textarea 
          v-model="userInput" 
          placeholder="Ask a question..."
          @keyup.enter.ctrl="sendMessage"
          rows="3"
        ></textarea>
        <button @click="sendMessage" :disabled="!userInput.trim() || loading" class="btn btn-primary">
          Send
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from '../composables/useToast'
import api from '../services/api'
import { marked } from 'marked'

// Configure marked for better rendering
marked.setOptions({
  breaks: true,
  gfm: true
})

export default {
  name: 'ChatView',
  setup() {
    const route = useRoute()
    const toast = useToast()
    const kbId = ref(route.params.id)
    const kbName = ref('Loading...')
    const messages = ref([])
    const userInput = ref('')
    const loading = ref(false)
    const messagesContainer = ref(null)

    onMounted(async () => {
      await loadKBInfo()
      await loadHistory()
    })

    async function loadKBInfo() {
      try {
        const response = await api.getKB(kbId.value)
        kbName.value = response.data.name
      } catch (err) {
        console.error('Failed to load KB info:', err)
        kbName.value = 'Knowledge Base'
      }
    }

    async function loadHistory() {
      try {
        const response = await api.getHistory(kbId.value)
        messages.value = response.data.history.reverse().map(h => ({
          user: h.user_message,
          bot: h.bot_response,
          sources: []
        }))
        scrollToBottom()
      } catch (err) {
        console.error('Failed to load history:', err)
      }
    }

    async function sendMessage() {
      if (!userInput.value.trim() || loading.value) return

      const message = userInput.value.trim()
      userInput.value = ''
      loading.value = true

      try {
        const response = await api.chat(kbId.value, message)
        messages.value.push({
          user: message,
          bot: response.data.response,
          sources: response.data.sources
        })
        await nextTick()
        scrollToBottom()
      } catch (err) {
        messages.value.push({
          user: message,
          bot: 'Error: Failed to get response. Please try again.',
          sources: []
        })
        toast.error('Failed to get response')
      } finally {
        loading.value = false
      }
    }

    function scrollToBottom() {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }

    function renderMarkdown(text) {
      return marked(text)
    }

    return {
      kbName,
      messages,
      userInput,
      loading,
      messagesContainer,
      sendMessage,
      renderMarkdown
    }
  }
}
</script>

<style scoped>
.chat-view {
  max-width: 1000px;
  margin: 0 auto;
  height: calc(100vh - 200px);
  display: flex;
  flex-direction: column;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.chat-header h2 {
  color: white;
  font-size: 1.8rem;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--glass-white);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border-glass);
  border-radius: 16px;
  box-shadow: var(--shadow-glass);
  overflow: hidden;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.message-group {
  margin-bottom: 1.5rem;
}

.message {
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 0.5rem;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid var(--border-glass);
  transition: all 0.3s ease;
}

.message:hover {
  transform: translateX(2px);
}

.message.user {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
  margin-left: 20%;
  color: white;
}

.message.bot {
  background: rgba(255, 255, 255, 0.1);
  margin-right: 20%;
  color: white;
}

.message.loading {
  opacity: 0.6;
  font-style: italic;
}

.message strong {
  color: rgba(255, 255, 255, 0.95);
}

.markdown-content {
  margin-top: 0.5rem;
  line-height: 1.6;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  color: white;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.markdown-content h1 {
  font-size: 1.5rem;
}

.markdown-content h2 {
  font-size: 1.3rem;
}

.markdown-content h3 {
  font-size: 1.1rem;
}

.markdown-content p {
  margin: 0.5rem 0;
}

.markdown-content ul,
.markdown-content ol {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
}

.markdown-content li {
  margin: 0.25rem 0;
}

.markdown-content code {
  background: rgba(0, 0, 0, 0.3);
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.markdown-content pre {
  background: rgba(0, 0, 0, 0.3);
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 0.5rem 0;
}

.markdown-content pre code {
  background: none;
  padding: 0;
}

.markdown-content blockquote {
  border-left: 3px solid rgba(255, 255, 255, 0.5);
  padding-left: 1rem;
  margin: 0.5rem 0;
  font-style: italic;
  opacity: 0.9;
}

.markdown-content table {
  border-collapse: collapse;
  width: 100%;
  margin: 0.5rem 0;
}

.markdown-content table th,
.markdown-content table td {
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.5rem;
  text-align: left;
}

.markdown-content table th {
  background: rgba(255, 255, 255, 0.1);
  font-weight: 600;
}

.markdown-content a {
  color: rgba(144, 238, 144, 1);
  text-decoration: underline;
}

.markdown-content a:hover {
  color: rgba(173, 255, 173, 1);
}

.markdown-content hr {
  border: none;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  margin: 1rem 0;
}

.sources {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-glass);
}

.sources summary {
  cursor: pointer;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.sources summary:hover {
  background: rgba(255, 255, 255, 0.1);
}

.source {
  background: rgba(255, 255, 255, 0.1);
  padding: 0.75rem;
  margin: 0.5rem 0;
  border-left: 3px solid rgba(255, 255, 255, 0.8);
  border-radius: 6px;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.source strong {
  color: rgba(255, 255, 255, 1);
  font-weight: 600;
}

.source p {
  margin: 0.5rem 0 0 0;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

.input-area {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid var(--border-glass);
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.input-area textarea {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid var(--border-glass);
  border-radius: 8px;
  resize: none;
  font-family: inherit;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  transition: all 0.3s ease;
}

.input-area textarea::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.input-area textarea:focus {
  outline: none;
  border-color: var(--border-glass-hover);
  background: rgba(255, 255, 255, 0.15);
}

.input-area button {
  align-self: flex-end;
}
</style>
