import { http } from '@/services/http'
import type { 
  WorkflowsModel, 
  WorkflowState, 
  Step1Data,
  Step2Data,
  Step3Data,
  Step4Data,
  Step5Data,
  Step6Data,
  Step7Data,
  Step8Data,
  Node1Input,
  Node2Input,
  Node3Input,
  Node4Input,
  Node5Input,
  WorkflowResponse,
  WorkflowStatusResponse
} from '@/types/workflow'

// Workflow API response interfaces
export interface StartWorkflowResponse {
  session_id: string
  status: string
  message: string
}

export interface GetWorkflowStatusResponse {
  workflow: WorkflowState
  current_step_data?: any
  // 轮询状态字段
  current_step?: number
  total_steps?: number
  progress?: number
  status?: 'pending' | 'in_progress' | 'completed' | 'failed'
  message?: string
  error?: string | null
}

export interface WorkflowListResponse {
  total: number
  completed: WorkflowsModel[]
  in_progress: WorkflowsModel[]
  failed: WorkflowsModel[]
}

// Article list interfaces
export interface ArticleListItem {
  session_id: number
  article_title: string
  seo_title?: string
  article_description?: string
  url_example?: string
  keyword: string
  target_market: string
  article_language: string
  created_time: string // Format: YYYY-MM-DD HH:MM:SS
  updated_time: string // Format: YYYY-MM-DD HH:MM:SS
  status: string
  final_article_content?: string
  final_article_html?: string
}

export interface PaginationInfo {
  total: number
  pages: number
  current_page: number
  per_page: number
  has_next: boolean
  has_prev: boolean
  next_page?: number
  prev_page?: number
}

export interface ArticleListResponse {
  articles: ArticleListItem[]
  pagination: PaginationInfo
}

export interface ArticleDetailResponse extends WorkflowsModel {
  // Contains all workflow fields
}

export interface ModifyArticleResponse {
  code: number
  message: string
}

// Backend response format
interface BackendResponse<T = any> {
  code: number
  message: string
  data?: T
}

export const generationApi = {
  // Start workflow with new_workflow flag
  startWorkflow: async (data: Step1Data): Promise<StartWorkflowResponse> => {
    const requestData = {
      new_workflow: "1",
      node_input: {
        keyword: data.keyword,
        target_market: data.target_market,
        article_language: data.article_language
      }
    }
    
    const response = await http.post<BackendResponse>('/workflows', requestData, { 
      skipGlobalErrorHandling: true 
    })
    
    if (response.data.code !== 200 && response.data.code !== 202) {
      throw new Error(response.data.message)
    }
    
    return {
      session_id: response.data.data?.session_id?.toString() || '',
      status: 'pending',
      message: response.data.message
    }
  },

  // Get workflow status and current data
  getWorkflowStatus: async (sessionId: string, skipGlobalErrorHandling?: boolean): Promise<GetWorkflowStatusResponse> => {
    const config = skipGlobalErrorHandling ? { skipGlobalErrorHandling: true } : {}
    const response = await http.get<BackendResponse>(`/workflows/status/${sessionId}`, config)
    
    if (response.data.code === 202) {
      // In progress - return basic workflow state
      // 优先使用loading_text，如果没有则使用message
      const loadingText = response.data.data?.loading_text || response.data.message || '正在处理中...'
      
      const workflow: WorkflowState = {
        session_id: sessionId,
        user_email: '',
        current_step: response.data.data?.current_node_index || 1,
        status: 'in_progress',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        loading_text: loadingText
      }
      
      return { workflow }
    } else if (response.data.code === 200) {
      // Completed - convert backend response to frontend format
      const workflowData = response.data.data || {}
      

      
      // 处理 gen_search_intent 数据
      let processedSearchIntent = workflowData.gen_search_intent
      if (typeof processedSearchIntent === 'string') {
        try {
          // 尝试解析JSON
          processedSearchIntent = JSON.parse(processedSearchIntent)
        } catch (e) {
          // 如果不是JSON，按行分割
          processedSearchIntent = processedSearchIntent.split('\n').filter(item => item.trim())
        }
      }
      
      // 处理 gen_topic_ideas 数据
      let processedTopicIdeas = workflowData.gen_topic_ideas
      if (typeof processedTopicIdeas === 'string') {
        try {
          processedTopicIdeas = JSON.parse(processedTopicIdeas)
        } catch (e) {
          processedTopicIdeas = processedTopicIdeas.split('\n').filter(item => item.trim())
        }
      }
      
      // 处理 gen_article_titles 数据
      let processedArticleTitles = workflowData.gen_article_titles
      if (typeof processedArticleTitles === 'string') {
        try {
          processedArticleTitles = JSON.parse(processedArticleTitles)
        } catch (e) {
          processedArticleTitles = processedArticleTitles.split('\n').filter(item => item.trim())
        }
      }
      
      const workflow: WorkflowState = {
        session_id: sessionId,
        user_email: workflowData.email || '',
        current_step: workflowData.current_node_index || 1,
        status: workflowData.status || 'completed',
        created_at: workflowData.created_time || new Date().toISOString(),
        updated_at: workflowData.updated_time || new Date().toISOString(),
        // Map all workflow data fields
        keyword: workflowData.keyword,
        target_market: workflowData.target_market,
        article_language: workflowData.article_language,
        gen_search_intent: processedSearchIntent,
        gen_topic_ideas: processedTopicIdeas,
        chosen_topic: workflowData.chosen_topic,
        gen_research_data: workflowData.gen_research_data,
        background_information: workflowData.background_information,
        title_generation_demands: workflowData.title_generation_demands,
        gen_article_titles: processedArticleTitles,
        article_title: workflowData.article_title,
        additional_knowledge_points: workflowData.additional_knowledge_points,
        outline_demand: workflowData.outline_demand,
        gen_article_outline: workflowData.gen_article_outline,
        article_outline: workflowData.article_outline,
        narrative_perspective: workflowData.narrative_perspective,
        gen_article_content: workflowData.gen_article_content,
        article_content: workflowData.article_content,
        secondary_keywords: workflowData.secondary_keywords,
        gen_optimized_article_content: workflowData.gen_optimized_article_content,
        final_article_content: workflowData.final_article_content,
        final_article_html: workflowData.final_article_html,
        seo_title: workflowData.seo_title,
        seo_description: workflowData.seo_description,
        url_example: workflowData.url_example,
        article_description: workflowData.article_description,
        main_image_option: workflowData.main_image_option,
        sub_images_option: workflowData.sub_images_option,
        failed_message: workflowData.failed_message
      }
      
      return { workflow, current_step_data: workflowData }
    } else {
      throw new Error(response.data.message || `Unexpected response code: ${response.data.code}`)
    }
  },

  // Get complete workflow result data
  getWorkflowResult: async (sessionId: string): Promise<WorkflowState> => {
    const response = await http.get<BackendResponse>(`/workflows/result/${sessionId}`)
    
    if (response.data.code !== 200) {
      throw new Error(response.data.message)
    }
    
    const workflowData = response.data.data || {}
    
    return {
      session_id: sessionId,
      user_email: workflowData.email || '',
      current_step: workflowData.current_node_index || 1,
      status: workflowData.status || 'completed',
      created_at: workflowData.created_time || new Date().toISOString(),
      updated_at: workflowData.updated_time || new Date().toISOString(),
      // Map all workflow data fields
      keyword: workflowData.keyword,
      target_market: workflowData.target_market,
      article_language: workflowData.article_language,
      gen_search_intent: workflowData.gen_search_intent,
      gen_topic_ideas: workflowData.gen_topic_ideas,
      chosen_topic: workflowData.chosen_topic,
      gen_research_data: workflowData.gen_research_data,
      background_information: workflowData.background_information,
      title_generation_demands: workflowData.title_generation_demands,
      gen_article_titles: workflowData.gen_article_titles,
      article_title: workflowData.article_title,
      additional_knowledge_points: workflowData.additional_knowledge_points,
      outline_demand: workflowData.outline_demand,
      gen_article_outline: workflowData.gen_article_outline,
      article_outline: workflowData.article_outline,
      narrative_perspective: workflowData.narrative_perspective,
      gen_article_content: workflowData.gen_article_content,
      article_content: workflowData.article_content,
      secondary_keywords: workflowData.secondary_keywords,
      gen_optimized_article_content: workflowData.gen_optimized_article_content,
      final_article_content: workflowData.final_article_content,
      final_article_html: workflowData.final_article_html,
      seo_title: workflowData.seo_title,
      seo_description: workflowData.seo_description,
      url_example: workflowData.url_example,
      article_description: workflowData.article_description,
      main_image_option: workflowData.main_image_option,
      sub_images_option: workflowData.sub_images_option
    }
  },

  // Continue workflow to next step
  continueWorkflow: async (sessionId: string, nodeInput: any): Promise<any> => {
    const sessionIdNumber = parseInt(sessionId)
    if (isNaN(sessionIdNumber)) {
      throw new Error(`Invalid session ID: ${sessionId}`)
    }
    
    const requestData = {
      session_id: sessionIdNumber,
      node_input: nodeInput
    }
    
    const response = await http.post<BackendResponse>('/workflows', requestData, { 
      skipGlobalErrorHandling: true 
    })
    
    if (response.data.code !== 200 && response.data.code !== 202) {
      throw new Error(response.data.message)
    }
    
    return response.data
  },

  // Get workflow list
  getWorkflowList: async (): Promise<WorkflowListResponse> => {
    const response = await http.get<BackendResponse>('/workflows/list')
    
    if (response.data.code !== 200) {
      throw new Error(response.data.message)
    }
    
    return response.data.data
  },

  // Get completed articles list
  getCompletedArticles: async (params?: {
    page?: number
    per_page?: number
    sort_by?: string
    sort_order?: 'asc' | 'desc'
  }): Promise<ArticleListResponse> => {
    const searchParams = new URLSearchParams()
    
    if (params?.page) searchParams.append('page', params.page.toString())
    if (params?.per_page) searchParams.append('per_page', params.per_page.toString())
    if (params?.sort_by) searchParams.append('sort_by', params.sort_by)
    if (params?.sort_order) searchParams.append('sort_order', params.sort_order)
    
    const url = `/workflows/completed_articles${searchParams.toString() ? '?' + searchParams.toString() : ''}`
    const response = await http.get<BackendResponse>(url)
    
    if (response.data.code !== 200) {
      throw new Error(response.data.message)
    }
    
    return response.data.data
  },

  // Get single article detail
  getArticleDetail: async (sessionId: number): Promise<ArticleDetailResponse> => {
    const response = await http.get<BackendResponse>(`/workflows/completed_articles/${sessionId}`)
    
    if (response.data.code !== 200) {
      throw new Error(response.data.message)
    }
    
    return response.data.data
  },

  // Modify article content
  modifyArticle: async (sessionId: string, modifiedArticle: string): Promise<ModifyArticleResponse> => {
    const requestData = {
      modified_article: modifiedArticle
    }
    
    const response = await http.post<BackendResponse>(`/workflows/modify_article/${sessionId}`, requestData)
    
    if (response.data.code !== 200) {
      throw new Error(response.data.message)
    }
    
    return {
      code: response.data.code,
      message: response.data.message
    }
  },

  // Helper function to extract step data from backend workflow
  getStepData: async (sessionId: string, step: number): Promise<any> => {
    const response = await generationApi.getWorkflowStatus(sessionId)
    const workflowData = response.current_step_data
    
    if (!workflowData || response.workflow.current_step < step) {
      return null
    }
    
    switch (step) {
      case 1:
        return {
          keyword: workflowData.keyword,
          target_market: workflowData.target_market,
          article_language: workflowData.article_language
        }
      case 2:
        return {
          gen_search_intent: workflowData.gen_search_intent
        }
      case 3:
        return {
          gen_topic_ideas: workflowData.gen_topic_ideas ? (
            typeof workflowData.gen_topic_ideas === 'string' 
              ? JSON.parse(workflowData.gen_topic_ideas) 
              : workflowData.gen_topic_ideas
          ) : [],
          chosen_topic: workflowData.chosen_topic
        }
      case 4:
        return {
          gen_research_data: workflowData.gen_research_data,
          background_information: workflowData.background_information
        }
      case 5:
        return {
          title_generation_demands: workflowData.title_generation_demands,
          gen_article_titles: workflowData.gen_article_titles ? JSON.parse(workflowData.gen_article_titles) : [],
          article_title: workflowData.article_title
        }
      case 6:
        return {
          additional_knowledge_points: workflowData.additional_knowledge_points,
          outline_demand: workflowData.outline_demand,
          gen_article_outline: workflowData.gen_article_outline,
          article_outline: workflowData.article_outline
        }
      case 7:
        return {
          narrative_perspective: workflowData.narrative_perspective,
          gen_article_content: workflowData.gen_article_content,
          article_content: workflowData.article_content
        }
      case 8:
        return {
          secondary_keywords: workflowData.secondary_keywords,
          gen_optimized_article_content: workflowData.gen_optimized_article_content,
          final_article_content: workflowData.final_article_content,
          seo_title: workflowData.seo_title,
          seo_description: workflowData.seo_description,
          url_example: workflowData.url_example,
          main_image_option: workflowData.main_image_option,
          sub_images_option: workflowData.sub_images_option,
          final_article_html: workflowData.final_article_html
        }
      default:
        return null
    }
  },

  // Polling mechanism for workflow status
  pollWorkflowStatus: async (sessionId: string, onUpdate: (workflow: WorkflowState) => void, intervalMs = 2000): Promise<() => void> => {
    const poll = async (): Promise<void> => {
      try {
        const response = await generationApi.getWorkflowStatus(sessionId)
        onUpdate(response.workflow)
        
        // Continue polling if workflow is still in progress
        if (response.workflow.status === 'in_progress') {
          timeoutId = window.setTimeout(poll, intervalMs) as any
        }
      } catch (error) {
        console.error('Polling error:', error)
        // Retry after longer interval on error
        timeoutId = window.setTimeout(poll, intervalMs * 2) as any
      }
    }
    
    let timeoutId: any
    await poll()
    
    // Return cleanup function
    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId)
      }
    }
  }
}