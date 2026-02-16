<template>
  <div id="app">
    <nav class="navbar">
      <div class="container">
        <h1 class="logo">KB Builder</h1>
        <div class="nav-links">
          <router-link to="/">Home</router-link>
          <router-link to="/create">Create KB</router-link>
        </div>
      </div>
    </nav>
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
import Toast from './components/Toast.vue'
import { useToast } from './composables/useToast'

export default {
  name: 'App',
  components: {
    Toast
  },
  setup() {
    const { toastState, closeToast } = useToast()
    return { toastState, closeToast }
  }
}
</script>

<style scoped>
.navbar {
  background: var(--glass-white);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border-glass);
  color: white;
  padding: 1rem 0;
  margin-bottom: 2rem;
  border-radius: 16px;
  box-shadow: var(--shadow-glass);
}

.navbar .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  margin: 0;
  font-size: 1.5rem;
  background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-links a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  background: var(--glass-white-soft);
  border-color: var(--border-glass);
  transform: translateY(-1px);
}
</style>
