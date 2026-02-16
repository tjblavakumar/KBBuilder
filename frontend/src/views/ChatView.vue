<template>
  <div class="chat-view">
    <div class="chat-header">
      <h2>Chat with Knowledge Base</h2>
      <router-link to="/" class="btn btn-secondary">Back to Home</router-link>
    </div>

    <div class="chat-container">
      <div class="messages" ref="messagesContainer">
        <div v-for="(msg, index) in messages" :key="index" class="message-group">
          <div class="message user">
            <strong>You:</strong> {{ msg.user }}
          </div>
          <div class="message bot">
            <strong>Assistant:</strong> {{ msg.bot }}
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
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from '../composables/useToast'
import api from '../services/api'

export default {
  name: 'ChatView',
  setup() {
    const route = useRoute()
    const toast = useToast()
    const kbId = ref(route.params.id)
    const messages = ref([])
    const userInput = ref('')
    const loading = ref(false)
    const messagesContainer = ref(null)

    onMounted(async () => {
      await loadHistory()
    })

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

    return {
      messages,
      userInput,
      loading,
      messagesContainer,
      sendMessage
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

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.message.user {
  background: #e3f2fd;
  margin-left: 20%;
}

.message.bot {
  background: #f5f5f5;
  margin-right: 20%;
}

.message.loading {
  opacity: 0.6;
  font-style: italic;
}

.sources {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #ddd;
}

.sources summary {
  cursor: pointer;
  font-weight: 500;
  color: #2c3e50;
}

.source {
  background: white;
  padding: 0.75rem;
  margin: 0.5rem 0;
  border-left: 3px solid #42b983;
  border-radius: 4px;
}

.source strong {
  color: #2c3e50;
}

.source p {
  margin: 0.5rem 0 0 0;
  color: #666;
  font-size: 0.9rem;
}

.input-area {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #ddd;
  background: #f9f9f9;
}

.input-area textarea {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: none;
  font-family: inherit;
  font-size: 1rem;
}

.input-area button {
  align-self: flex-end;
}
</style>
