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
  background: #2c3e50;
  color: white;
  padding: 1rem 0;
  margin-bottom: 2rem;
}

.navbar .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  margin: 0;
  font-size: 1.5rem;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-links a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background 0.3s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  background: #34495e;
}
</style>
