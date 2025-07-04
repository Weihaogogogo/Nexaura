import { createPinia } from 'pinia'

export const store = createPinia()

export default store

// Re-export stores for easy access
export { useUserStore } from './modules/user'
export { useArticlesStore } from './modules/articles'