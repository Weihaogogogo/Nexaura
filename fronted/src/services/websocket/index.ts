import { io, Socket } from 'socket.io-client'
import { ref, computed } from 'vue'

export interface SocketProgress {
  session_id: string
  step: number
  progress: number
  status: 'pending' | 'in_progress' | 'completed' | 'failed'
  message?: string
  data?: any
  error?: string
}

export interface SocketMessage {
  type: 'progress' | 'step_complete' | 'step_failed' | 'workflow_complete' | 'error'
  data: SocketProgress
}

class WebSocketService {
  private socket: Socket | null = null
  private connected = ref(false)
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectTimeout: any = null
  
  // Progress tracking
  private currentProgress = ref<SocketProgress | null>(null)
  private progressCallbacks = new Map<string, (progress: SocketProgress) => void>()
  private stepCompleteCallbacks = new Map<string, (data: any) => void>()
  private errorCallbacks = new Map<string, (error: string) => void>()

  constructor() {
    this.connect()
  }

  // Connection management
  private connect() {
    try {
      const wsUrl = import.meta.env.VITE_WS_BASE_URL || (import.meta.env.PROD ? 'http://116.63.139.71' : 'http://localhost:5000')
      
      this.socket = io(wsUrl, {
        autoConnect: false,
        timeout: 20000,
        transports: ['websocket', 'polling'],
        upgrade: true,
        rememberUpgrade: true
      })

      this.setupEventListeners()
      this.socket.connect()
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error)
    }
  }

  private setupEventListeners() {
    if (!this.socket) return

    this.socket.on('connect', () => {
      console.log('WebSocket connected')
      this.connected.value = true
      this.reconnectAttempts = 0
      this.clearReconnectTimeout()
    })

    this.socket.on('disconnect', (reason) => {
      console.log('WebSocket disconnected:', reason)
      this.connected.value = false
      
      // Only attempt reconnection if it wasn't intentional
      if (reason === 'io server disconnect') {
        // Server initiated disconnect, don't reconnect
        return
      }
      
      this.attemptReconnect()
    })

    this.socket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error)
      this.connected.value = false
      this.attemptReconnect()
    })

    // Progress events
    this.socket.on('workflow_progress', (data: SocketProgress) => {
      console.log('Progress update:', data)
      this.currentProgress.value = data
      
      const callback = this.progressCallbacks.get(data.session_id)
      if (callback) {
        callback(data)
      }
    })

    this.socket.on('step_complete', (data: SocketProgress) => {
      console.log('Step completed:', data)
      this.currentProgress.value = data
      
      const callback = this.stepCompleteCallbacks.get(data.session_id)
      if (callback) {
        callback(data.data)
      }
    })

    this.socket.on('step_failed', (data: SocketProgress) => {
      console.error('Step failed:', data)
      this.currentProgress.value = data
      
      const callback = this.errorCallbacks.get(data.session_id)
      if (callback) {
        callback(data.error || 'Step failed')
      }
    })

    this.socket.on('workflow_complete', (data: SocketProgress) => {
      console.log('Workflow completed:', data)
      this.currentProgress.value = data
      
      const callback = this.stepCompleteCallbacks.get(data.session_id)
      if (callback) {
        callback(data.data)
      }
    })

    this.socket.on('error', (error: any) => {
      console.error('WebSocket error:', error)
      
      if (error.session_id) {
        const callback = this.errorCallbacks.get(error.session_id)
        if (callback) {
          callback(error.message || 'Unknown error occurred')
        }
      }
    })
  }

  private attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached')
      return
    }

    this.clearReconnectTimeout()
    
    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000)
    this.reconnectAttempts++
    
    console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`)
    
    this.reconnectTimeout = setTimeout(() => {
      if (this.socket) {
        this.socket.connect()
      }
    }, delay)
  }

  private clearReconnectTimeout() {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout)
      this.reconnectTimeout = null
    }
  }

  // Public API
  get isConnected() {
    return computed(() => this.connected.value)
  }

  get progress() {
    return computed(() => this.currentProgress.value)
  }

  // Subscribe to session progress
  subscribeToProgress(
    sessionId: string,
    onProgress: (progress: SocketProgress) => void,
    onStepComplete?: (data: any) => void,
    onError?: (error: string) => void
  ) {
    this.progressCallbacks.set(sessionId, onProgress)
    
    if (onStepComplete) {
      this.stepCompleteCallbacks.set(sessionId, onStepComplete)
    }
    
    if (onError) {
      this.errorCallbacks.set(sessionId, onError)
    }

    // Join the session room
    if (this.socket && this.connected.value) {
      this.socket.emit('join_session', sessionId)
    }
  }

  // Unsubscribe from session
  unsubscribeFromProgress(sessionId: string) {
    this.progressCallbacks.delete(sessionId)
    this.stepCompleteCallbacks.delete(sessionId)
    this.errorCallbacks.delete(sessionId)

    // Leave the session room
    if (this.socket && this.connected.value) {
      this.socket.emit('leave_session', sessionId)
    }
  }

  // Manual reconnection
  reconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket.connect()
    }
  }

  // Disconnect
  disconnect() {
    this.clearReconnectTimeout()
    this.progressCallbacks.clear()
    this.stepCompleteCallbacks.clear()
    this.errorCallbacks.clear()
    
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
    
    this.connected.value = false
  }

  // Send custom message
  emit(event: string, data: any) {
    if (this.socket && this.connected.value) {
      this.socket.emit(event, data)
    } else {
      console.warn('Cannot emit event: WebSocket not connected')
    }
  }
}

// Create singleton instance
export const webSocketService = new WebSocketService()

// Composable for using WebSocket in components
export function useWebSocket() {
  return {
    isConnected: webSocketService.isConnected,
    progress: webSocketService.progress,
    subscribeToProgress: webSocketService.subscribeToProgress.bind(webSocketService),
    unsubscribeFromProgress: webSocketService.unsubscribeFromProgress.bind(webSocketService),
    reconnect: webSocketService.reconnect.bind(webSocketService),
    disconnect: webSocketService.disconnect.bind(webSocketService),
    emit: webSocketService.emit.bind(webSocketService)
  }
}