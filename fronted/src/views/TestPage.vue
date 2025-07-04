<template>
  <div class="test-page">
    <h1>API Test Page</h1>
    
    <div class="test-section">
      <h2>User Status</h2>
      <p>Is Authenticated: {{ userStore.isAuthenticated }}</p>
      <p>User Email: {{ userStore.user?.email || 'Not logged in' }}</p>
      <p>User Name: {{ userStore.user?.name || 'N/A' }}</p>
    </div>
    
    <div class="test-section">
      <h2>API Tests</h2>
      <button @click="testBasicAPI" :disabled="loading">Test Basic API</button>
      <button @click="testWorkflowAPI" :disabled="loading">Test Workflow API</button>
      <button @click="loginDev" :disabled="loading">Login as Dev</button>
    </div>
    
    <div class="test-section">
      <h2>Results</h2>
      <pre>{{ results }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/modules/user'
import { http } from '@/services/http'

const userStore = useUserStore()
const loading = ref(false)
const results = ref('')

const testBasicAPI = async () => {
  loading.value = true
  try {
    results.value = 'Testing basic API...\n'
    const response = await http.get('/test')
    results.value += `Success: ${JSON.stringify(response.data, null, 2)}\n`
  } catch (error: any) {
    results.value += `Error: ${error.message}\n`
    console.error('API test error:', error)
  } finally {
    loading.value = false
  }
}

const testWorkflowAPI = async () => {
  loading.value = true
  try {
    results.value = 'Testing workflow API...\n'
    const requestData = {
      email: userStore.user?.email || 'dev@test.com',
      node_input: {
        keyword: 'test keyword',
        target_market: 'us',
        article_language: 'English'
      },
      new_workflow: true
    }
    
    const response = await http.post('/workflows', requestData)
    results.value += `Success: ${JSON.stringify(response.data, null, 2)}\n`
  } catch (error: any) {
    results.value += `Error: ${error.message}\n`
    console.error('Workflow test error:', error)
  } finally {
    loading.value = false
  }
}

const loginDev = async () => {
  loading.value = true
  try {
    results.value = 'Logging in as dev...\n'
    await userStore.login({
      email: 'dev@test.com',
      password: 'dev123456',
      remember: false
    })
    results.value += 'Login successful!\n'
  } catch (error: any) {
    results.value += `Login error: ${error.message}\n`
    console.error('Login error:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.test-page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.test-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

button {
  margin-right: 10px;
  margin-bottom: 10px;
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

pre {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  white-space: pre-wrap;
  max-height: 400px;
  overflow-y: auto;
}
</style>