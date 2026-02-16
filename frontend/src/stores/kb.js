import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useKBStore = defineStore('kb', () => {
  const currentKB = ref(null)
  const pdfs = ref([])
  const selectedPdfs = ref([])
  const models = ref([])
  const defaultModel = ref('')

  function setCurrentKB(kb) {
    currentKB.value = kb
  }

  function setPdfs(pdfList) {
    pdfs.value = pdfList
  }

  function togglePdf(pdf) {
    const index = selectedPdfs.value.findIndex(p => p.url === pdf.url)
    if (index > -1) {
      selectedPdfs.value.splice(index, 1)
    } else {
      selectedPdfs.value.push(pdf)
    }
  }

  function clearSelectedPdfs() {
    selectedPdfs.value = []
  }

  function setModels(modelList, defaultModelId) {
    models.value = modelList
    defaultModel.value = defaultModelId
  }

  function resetCreateKBState() {
    pdfs.value = []
    selectedPdfs.value = []
  }

  return {
    currentKB,
    pdfs,
    selectedPdfs,
    models,
    defaultModel,
    setCurrentKB,
    setPdfs,
    togglePdf,
    clearSelectedPdfs,
    setModels,
    resetCreateKBState
  }
})
