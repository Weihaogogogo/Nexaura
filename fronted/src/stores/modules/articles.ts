import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Article {
  id: string
  title: string
  content: string
  status: 'pending' | 'in_progress' | 'completed' | 'failed'
  keywords: string[]
  language: string
  market: string
  word_count: number
  created_at: string
  updated_at: string
  user_id: string
}

export const useArticlesStore = defineStore('articles', () => {
  // State
  const articles = ref<Article[]>([])
  const currentArticle = ref<Article | null>(null)
  const isLoading = ref(false)
  const total = ref(0)
  const currentPage = ref(1)
  const pageSize = ref(10)

  // Getters
  const completedArticles = computed(() => 
    articles.value.filter(article => article.status === 'completed')
  )
  
  const inProgressArticles = computed(() =>
    articles.value.filter(article => article.status === 'in_progress')
  )
  
  const recentArticles = computed(() =>
    articles.value
      .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
      .slice(0, 5)
  )

  // Actions
  const fetchArticles = async (params?: {
    page?: number
    limit?: number
    status?: string
    search?: string
  }): Promise<void> => {
    try {
      isLoading.value = true
      // TODO: Implement API call
      // const response = await articlesApi.getArticles(params)
      // articles.value = response.data
      // total.value = response.total
    } catch (error) {
      console.error('Failed to fetch articles:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const fetchArticleById = async (id: string): Promise<void> => {
    try {
      isLoading.value = true
      // TODO: Implement API call
      // const article = await articlesApi.getArticleById(id)
      // currentArticle.value = article
    } catch (error) {
      console.error('Failed to fetch article:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const createArticle = async (articleData: Partial<Article>): Promise<Article> => {
    try {
      isLoading.value = true
      // TODO: Implement API call
      // const newArticle = await articlesApi.createArticle(articleData)
      // articles.value.unshift(newArticle)
      // return newArticle
      return {} as Article
    } catch (error) {
      console.error('Failed to create article:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const updateArticle = async (id: string, updates: Partial<Article>): Promise<void> => {
    try {
      isLoading.value = true
      // TODO: Implement API call
      // const updatedArticle = await articlesApi.updateArticle(id, updates)
      
      // Update in local state
      const index = articles.value.findIndex(article => article.id === id)
      if (index !== -1) {
        // articles.value[index] = updatedArticle
      }
      
      if (currentArticle.value?.id === id) {
        // currentArticle.value = updatedArticle
      }
    } catch (error) {
      console.error('Failed to update article:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const deleteArticle = async (id: string): Promise<void> => {
    try {
      isLoading.value = true
      // TODO: Implement API call
      // await articlesApi.deleteArticle(id)
      
      // Remove from local state
      articles.value = articles.value.filter(article => article.id !== id)
      
      if (currentArticle.value?.id === id) {
        currentArticle.value = null
      }
    } catch (error) {
      console.error('Failed to delete article:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const clearCurrentArticle = (): void => {
    currentArticle.value = null
  }

  return {
    // State
    articles,
    currentArticle,
    isLoading,
    total,
    currentPage,
    pageSize,
    // Getters
    completedArticles,
    inProgressArticles,
    recentArticles,
    // Actions
    fetchArticles,
    fetchArticleById,
    createArticle,
    updateArticle,
    deleteArticle,
    clearCurrentArticle
  }
})