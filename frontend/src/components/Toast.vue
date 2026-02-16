<template>
  <transition name="toast">
    <div v-if="visible" :class="['toast', type]">
      {{ message }}
    </div>
  </transition>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  name: 'Toast',
  props: {
    message: String,
    type: {
      type: String,
      default: 'info'
    },
    duration: {
      type: Number,
      default: 3000
    },
    show: Boolean
  },
  setup(props, { emit }) {
    const visible = ref(false)

    watch(() => props.show, (newVal) => {
      if (newVal) {
        visible.value = true
        setTimeout(() => {
          visible.value = false
          emit('close')
        }, props.duration)
      }
    })

    return { visible }
  }
}
</script>

<style scoped>
.toast {
  position: fixed;
  top: 2rem;
  right: 2rem;
  padding: 1rem 1.5rem;
  border-radius: 4px;
  color: white;
  font-weight: 500;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 2000;
  min-width: 250px;
}

.toast.success {
  background: #28a745;
}

.toast.error {
  background: #dc3545;
}

.toast.info {
  background: #17a2b8;
}

.toast.warning {
  background: #ffc107;
  color: #333;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.toast-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}
</style>
