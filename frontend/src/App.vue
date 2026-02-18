<template>
  <div id="app">
    <nav class="navbar">
      <div class="container">
        <h1 class="logo">
          <span class="logo-icon" aria-hidden="true">
            <span class="logo-dot"></span>
          </span>
          <span class="logo-text">KB Builder</span>
        </h1>
        <div class="nav-links">
          <router-link to="/">Home</router-link>
          <span class="key-status" :class="{ active: hasOpenAIApiKey }">
            {{ hasOpenAIApiKey ? 'OpenAI Ready' : 'No API Key' }}
          </span>
          <button class="admin-link" @click="showAdminModal = true">Admin</button>
        </div>
      </div>
    </nav>
    <div v-if="showAdminModal" class="modal" @click.self="showAdminModal = false">
      <div class="modal-content">
        <h3>Session Settings</h3>
        <p class="modal-note">OpenAI API key is stored in memory only and cleared when you refresh/close the app.</p>
        <label for="session-openai-key">OpenAI API Key</label>
        <input
          id="session-openai-key"
          v-model="draftApiKey"
          type="password"
          placeholder="sk-proj-..."
          autocomplete="off"
          spellcheck="false"
        >
        <div class="modal-actions">
          <button class="btn btn-secondary" @click="clearSessionKey">Clear</button>
          <button class="btn btn-primary" :disabled="validatingKey" @click="saveSessionKey">
            {{ validatingKey ? 'Validating...' : 'Save' }}
          </button>
        </div>
      </div>
    </div>
    <main class="container">
      <router-view />
    </main>
    <Toast 
      :show="toastState.show" 
      :message="toastState.message" 
      :type="toastState.type"
      @close="closeToast"
    />
  </div>
</template>

<script>
import { ref } from 'vue'
import Toast from './components/Toast.vue'
import { useToast } from './composables/useToast'
import { useSessionApiKey } from './composables/useSessionApiKey'
import api from './services/api'

export default {
  name: 'App',
  components: {
    Toast
  },
  setup() {
    const { toastState, closeToast, success, error, info, warning } = useToast()
    const { openaiApiKey, hasOpenAIApiKey, setOpenAIApiKey, clearOpenAIApiKey } = useSessionApiKey()
    const showAdminModal = ref(false)
    const draftApiKey = ref(openaiApiKey.value)
    const validatingKey = ref(false)

    async function saveSessionKey() {
      const key = (draftApiKey.value || '').trim()
      if (!key) {
        warning('Enter an OpenAI API key first')
        return
      }

      validatingKey.value = true
      try {
        await api.validateOpenAIKey(key)
        setOpenAIApiKey(key)
        showAdminModal.value = false
        success('OpenAI API key validated for this session')
      } catch (err) {
        error(err?.response?.data?.detail || err.message || 'OpenAI key validation failed')
      } finally {
        validatingKey.value = false
      }
    }

    function clearSessionKey() {
      draftApiKey.value = ''
      clearOpenAIApiKey()
      info('Session OpenAI key cleared')
    }

    return {
      toastState,
      closeToast,
      showAdminModal,
      draftApiKey,
      validatingKey,
      hasOpenAIApiKey,
      saveSessionKey,
      clearSessionKey
    }
  }
}
</script>

<style scoped>
.navbar {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 2px solid rgba(191, 219, 254, 0.6);
  color: white;
  padding: 1rem 0;
  margin-bottom: 2rem;
  box-shadow: 0 10px 22px rgba(30, 64, 175, 0.22);
}

.navbar .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.7rem;
  font-size: 2rem;
  line-height: 1;
  font-weight: 800;
}

.logo-text {
  background: linear-gradient(135deg, #dbeafe 0%, #a5b4fc 55%, #c4b5fd 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 12px rgba(165, 180, 252, 0.25);
}

.logo-icon {
  width: 2.15rem;
  height: 2.15rem;
  border-radius: 999px;
  background: linear-gradient(140deg, #3b82f6 0%, #4f46e5 55%, #7e22ce 100%);
  border: 1px solid rgba(255, 255, 255, 0.55);
  box-shadow:
    0 6px 16px rgba(30, 64, 175, 0.35),
    inset 0 1px 3px rgba(255, 255, 255, 0.35);
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.logo-icon::before {
  content: '';
  width: 1rem;
  height: 0.74rem;
  border-radius: 0.15rem;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 0 0 1px rgba(79, 70, 229, 0.25);
}

.logo-dot {
  position: absolute;
  width: 0.36rem;
  height: 0.36rem;
  border-radius: 999px;
  background: #60a5fa;
  bottom: 0.32rem;
  right: 0.32rem;
  box-shadow: 0 0 8px rgba(96, 165, 250, 0.8);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-links a,
.admin-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  background: transparent;
  font: inherit;
  cursor: pointer;
}

.key-status {
  font-size: 0.82rem;
  padding: 0.35rem 0.6rem;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.9);
}

.key-status.active {
  border-color: rgba(147, 197, 253, 0.85);
  background: rgba(96, 165, 250, 0.2);
  color: #dbeafe;
}

.nav-links a:hover,
.nav-links a.router-link-active,
.admin-link:hover {
  background: var(--glass-white-soft);
  border-color: var(--border-glass);
  transform: translateY(-1px);
}

.modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1200;
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
}

.modal-content {
  width: min(520px, 92vw);
  padding: 1.4rem;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.16);
  border: 1px solid var(--border-glass);
  box-shadow: var(--shadow-glass-hover);
}

.modal-content h3 {
  color: white;
  margin: 0 0 0.65rem 0;
}

.modal-note {
  color: rgba(255, 255, 255, 0.85);
  margin: 0 0 0.9rem 0;
  font-size: 0.92rem;
}

.modal-content label {
  display: block;
  margin-bottom: 0.5rem;
  color: white;
  font-weight: 600;
}

.modal-content input {
  width: 100%;
  padding: 0.7rem 0.8rem;
  border: 1px solid var(--border-glass);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.modal-content input:focus {
  outline: none;
  border-color: var(--border-glass-hover);
  background: rgba(255, 255, 255, 0.15);
}

.modal-actions {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.7rem;
}
</style>
