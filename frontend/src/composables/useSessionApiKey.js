import { computed, ref } from 'vue'

// In-memory only: cleared on page refresh/browser close.
const openaiApiKey = ref('')

export function useSessionApiKey() {
  function setOpenAIApiKey(value) {
    openaiApiKey.value = (value || '').trim()
  }

  function clearOpenAIApiKey() {
    openaiApiKey.value = ''
  }

  const hasOpenAIApiKey = computed(() => openaiApiKey.value.length > 0)

  return {
    openaiApiKey,
    hasOpenAIApiKey,
    setOpenAIApiKey,
    clearOpenAIApiKey
  }
}
