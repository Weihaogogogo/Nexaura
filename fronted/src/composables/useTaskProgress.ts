import { ref, computed, onUnmounted } from 'vue'
import { useWebSocket, type SocketProgress } from '@/services/websocket/index'
import { generationApi } from '@/services/api/generation'

export interface TaskProgressState {
  sessionId: string | null
  currentStep: number
  totalSteps: number
  progress: number
  status: 'pending' | 'in_progress' | 'completed' | 'failed'
  message: string
  error: string | null
  isLoading: boolean
}

export function useTaskProgress() {
  const { subscribeToProgress, unsubscribeFromProgress, isConnected } = useWebSocket()
  
  const state = ref<TaskProgressState>({
    sessionId: null,
    currentStep: 0,
    totalSteps: 7,
    progress: 0,
    status: 'pending',
    message: '',
    error: null,
    isLoading: false
  })

  // Polling fallback
  let pollingInterval: any = null
  const pollingEnabled = ref(false)

  // Computed properties
  const progressPercentage = computed(() => {
    if (state.value.totalSteps === 0) return 0
    return Math.round((state.value.currentStep / state.value.totalSteps) * 100)
  })

  const isCompleted = computed(() => state.value.status === 'completed')
  const isFailed = computed(() => state.value.status === 'failed')
  const isActive = computed(() => state.value.status === 'in_progress')

  // WebSocket event handlers
  const handleProgress = (progress: SocketProgress) => {
    state.value.currentStep = progress.step
    state.value.progress = progress.progress
    state.value.status = progress.status
    state.value.message = progress.message || ''
    
    if (progress.status === 'failed') {
      state.value.error = progress.error || 'Unknown error occurred'
    }
  }

  const handleStepComplete = (data: any) => {
    console.log('Step completed with data:', data)
    // Handle step completion if needed
  }

  const handleError = (error: string) => {
    state.value.error = error
    state.value.status = 'failed'
    state.value.isLoading = false
  }

  // API polling fallback
  const startPolling = (sessionId: string, interval: number = 2000) => {
    if (pollingInterval) {
      clearInterval(pollingInterval)
    }

    pollingEnabled.value = true
    pollingInterval = setInterval(async () => {
      try {
        const status = await generationApi.getWorkflowStatus(sessionId)
        
        state.value.currentStep = status.current_step
        state.value.totalSteps = status.total_steps
        state.value.progress = status.progress
        state.value.status = status.status
        state.value.message = status.message || ''
        state.value.error = status.error || null

        // Stop polling if completed or failed
        if (status.status === 'completed' || status.status === 'failed') {
          stopPolling()
        }
      } catch (error) {
        console.error('Polling error:', error)
        state.value.error = 'Failed to fetch progress'
        stopPolling()
      }
    }, interval)
  }

  const stopPolling = () => {
    if (pollingInterval) {
      clearInterval(pollingInterval)
      pollingInterval = null
    }
    pollingEnabled.value = false
  }

  // Main functions
  const startTracking = (sessionId: string, usePollingFallback: boolean = true) => {
    state.value.sessionId = sessionId
    state.value.isLoading = true
    state.value.error = null

    // Try WebSocket first
    if (isConnected.value) {
      subscribeToProgress(
        sessionId,
        handleProgress,
        handleStepComplete,
        handleError
      )
    } else if (usePollingFallback) {
      // Fallback to polling if WebSocket is not available
      console.warn('WebSocket not connected, using polling fallback')
      startPolling(sessionId)
    }
  }

  const stopTracking = () => {
    if (state.value.sessionId) {
      unsubscribeFromProgress(state.value.sessionId)
    }
    stopPolling()
    state.value.isLoading = false
  }

  const resetState = () => {
    stopTracking()
    state.value = {
      sessionId: null,
      currentStep: 0,
      totalSteps: 7,
      progress: 0,
      status: 'pending',
      message: '',
      error: null,
      isLoading: false
    }
  }

  // Manual progress update (for development/testing)
  const updateProgress = (progress: Partial<TaskProgressState>) => {
    Object.assign(state.value, progress)
  }

  // Get current step data
  const getCurrentStepData = async (): Promise<any | null> => {
    if (!state.value.sessionId || state.value.currentStep === 0) {
      return null
    }

    try {
      return await generationApi.getStepData(
        state.value.sessionId, 
        state.value.currentStep
      )
    } catch (error) {
      console.error('Failed to get step data:', error)
      return null
    }
  }

  // Wait for specific step completion
  const waitForStep = (targetStep: number, timeout: number = 30000): Promise<any> => {
    return new Promise((resolve, reject) => {
      const timeoutId = setTimeout(() => {
        reject(new Error(`Timeout waiting for step ${targetStep}`))
      }, timeout)

      const checkStep = () => {
        if (state.value.currentStep >= targetStep) {
          clearTimeout(timeoutId)
          resolve(state.value)
        } else if (state.value.status === 'failed') {
          clearTimeout(timeoutId)
          reject(new Error(state.value.error || 'Step failed'))
        } else {
          // Check again in 500ms
          setTimeout(checkStep, 500)
        }
      }

      checkStep()
    })
  }

  // Cleanup on unmount
  onUnmounted(() => {
    stopTracking()
  })

  return {
    // State
    state: computed(() => state.value),
    
    // Computed
    progressPercentage,
    isCompleted,
    isFailed,
    isActive,
    isConnected,
    pollingEnabled: computed(() => pollingEnabled.value),
    
    // Methods
    startTracking,
    stopTracking,
    resetState,
    updateProgress,
    getCurrentStepData,
    waitForStep,
    
    // Polling controls
    startPolling,
    stopPolling
  }
}