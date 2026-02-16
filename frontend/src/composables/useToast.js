import { ref } from 'vue'

const toastState = ref({
  show: false,
  message: '',
  type: 'info'
})

export function useToast() {
  function showToast(message, type = 'info') {
    toastState.value = {
      show: true,
      message,
      type
    }
  }

  function success(message) {
    showToast(message, 'success')
  }

  function error(message) {
    showToast(message, 'error')
  }

  function info(message) {
    showToast(message, 'info')
  }

  function warning(message) {
    showToast(message, 'warning')
  }

  function closeToast() {
    toastState.value.show = false
  }

  return {
    toastState,
    showToast,
    success,
    error,
    info,
    warning,
    closeToast
  }
}
