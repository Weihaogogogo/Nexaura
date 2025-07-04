import { io, Socket } from 'socket.io-client'

interface SocketEventMap {
  'workflow_update': (data: any) => void
  'step_completed': (data: any) => void
  'error': (error: any) => void
  'connection': () => void
  'disconnect': () => void
}

class WebSocketService {
  private socket: Socket | null = null
  private isConnected = false
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000

  connect(token?: string): void {
    if (this.socket?.connected) {
      return
    }

    const socketUrl = import.meta.env.VITE_WS_URL || (import.meta.env.PROD ? 'ws://116.63.139.71' : 'ws://localhost:3000')
    
    this.socket = io(socketUrl, {
      auth: {
        token: token || localStorage.getItem('auth_token')
      },
      transports: ['websocket'],
      autoConnect: true
    })

    this.setupEventListeners()
  }

  private setupEventListeners(): void {
    if (!this.socket) return

    this.socket.on('connect', () => {
      console.log('WebSocket connected')
      this.isConnected = true
      this.reconnectAttempts = 0
    })

    this.socket.on('disconnect', (reason) => {
      console.log('WebSocket disconnected:', reason)
      this.isConnected = false
      
      if (reason === 'io server disconnect') {
        // Server disconnected, try to reconnect
        this.reconnect()
      }
    })

    this.socket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error)
      this.reconnect()
    })
  }

  private reconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached')
      return
    }

    this.reconnectAttempts++
    
    setTimeout(() => {
      console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
      this.socket?.connect()
    }, this.reconnectDelay * this.reconnectAttempts)
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
      this.isConnected = false
    }
  }

  emit(event: string, data?: any): void {
    if (this.socket?.connected) {
      this.socket.emit(event, data)
    } else {
      console.warn('WebSocket not connected, cannot emit event:', event)
    }
  }

  on<K extends keyof SocketEventMap>(event: K, callback: SocketEventMap[K]): void {
    if (this.socket) {
      this.socket.on(event as string, callback)
    }
  }

  off<K extends keyof SocketEventMap>(event: K, callback?: SocketEventMap[K]): void {
    if (this.socket) {
      if (callback) {
        this.socket.off(event as string, callback)
      } else {
        this.socket.off(event as string)
      }
    }
  }

  // Workflow specific methods
  joinWorkflowRoom(sessionId: string): void {
    this.emit('join_workflow', { session_id: sessionId })
  }

  leaveWorkflowRoom(sessionId: string): void {
    this.emit('leave_workflow', { session_id: sessionId })
  }

  onWorkflowUpdate(callback: (data: any) => void): void {
    this.on('workflow_update', callback)
  }

  onStepCompleted(callback: (data: any) => void): void {
    this.on('step_completed', callback)
  }

  onError(callback: (error: any) => void): void {
    this.on('error', callback)
  }

  getConnectionStatus(): boolean {
    return this.isConnected
  }
}

export const websocketService = new WebSocketService()

export default websocketService