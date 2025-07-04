// Simple API test
async function testAPI() {
  try {
    console.log('Testing API connection...')
    
    const response = await fetch('http://localhost:5000/test', {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    console.log('Response status:', response.status)
    const data = await response.json()
    console.log('Response data:', data)
    
    // Test workflow creation
    const workflowResponse = await fetch('http://localhost:5000/workflows', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: 'dev@test.com',
        node_input: {
          keyword: 'test keyword',
          target_market: 'us',
          article_language: 'English'
        },
        new_workflow: true
      })
    })
    
    console.log('Workflow response status:', workflowResponse.status)
    const workflowData = await workflowResponse.json()
    console.log('Workflow response data:', workflowData)
    
  } catch (error) {
    console.error('API test failed:', error)
  }
}

// Run test
testAPI()