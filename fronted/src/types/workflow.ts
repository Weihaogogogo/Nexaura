// Workflow data types matching backend WorkflowsModel structure

export interface WorkflowsModel {
  session_id: number // Primary key from backend
  email: string // User email
  current_node_index: number // Current workflow step (1-8)
  status: 'in_progress' | 'completed' | 'failed' // Workflow status
  failed_message?: string // Error message if failed
  created_time: string // Creation timestamp - Format: YYYY-MM-DD HH:MM:SS
  updated_time: string // Last update timestamp - Format: YYYY-MM-DD HH:MM:SS
  
  // Step 1 - Keywords input
  keyword: string // Main keyword
  target_market: string // Target market (e.g., 'us')
  article_language: string // Article language (e.g., 'English')
  
  // Step 2 - Search intent generation
  gen_search_intent?: string // Generated search intent
  
  // Step 3 - Topic ideas generation
  gen_topic_ideas?: any[] // Generated topic ideas (JSON)
  chosen_topic?: string // User selected/input topic
  
  // Step 4 - Research data generation
  gen_research_data?: string // Generated research report
  background_information?: string // Background information
  
  // Step 5 - Title generation
  title_generation_demands?: string // Title generation requirements
  gen_article_titles?: any[] // Generated article titles (JSON)
  article_title?: string // User selected/input title
  
  // Step 6 - Outline generation
  additional_knowledge_points?: string // Additional knowledge points
  outline_demand?: string // Outline requirements
  gen_article_outline?: string // Generated outline
  article_outline?: string // User selected/input outline
  
  // Step 7 - Article generation
  narrative_perspective?: string // Narrative perspective
  gen_article_content?: string // Generated article content
  article_content?: string // User selected/input content
  
  // Step 8 - Article optimization
  secondary_keywords?: string // Secondary keywords
  gen_optimized_article_content?: string // Generated optimized content
  final_article_content?: string // Final MD format article
  seo_title?: string // SEO title (≤70 chars)
  seo_description?: string // SEO description
  article_description?: string // Article description/summary
  url_example?: string // URL example
  main_image_option?: boolean // Generate blog cover image
  sub_images_option?: boolean // Generate H2 title images
  final_article_html?: string // Final HTML format article
}

// Frontend workflow state (simplified for UI)
export interface WorkflowState {
  session_id: string
  user_email: string
  current_step: number
  status: 'pending' | 'in_progress' | 'completed' | 'failed'
  created_at: string
  updated_at: string
  loading_text?: string
  failed_message?: string
  
  // Direct mapping from backend fields
  keyword?: string
  target_market?: string
  article_language?: string
  gen_search_intent?: string | string[]
  gen_topic_ideas?: any[]
  chosen_topic?: string
  gen_research_data?: string
  background_information?: string
  title_generation_demands?: string
  gen_article_titles?: any[]
  article_title?: string
  additional_knowledge_points?: string
  outline_demand?: string
  gen_article_outline?: string
  article_outline?: string
  narrative_perspective?: string
  gen_article_content?: string
  article_content?: string
  secondary_keywords?: string
  gen_optimized_article_content?: string
  final_article_content?: string
  gen_final_article_content?: string
  final_article_html?: string
  seo_title?: string
  seo_description?: string
  url_example?: string
  article_description?: string
  main_image_option?: boolean
  sub_images_option?: boolean
  
  // Structured step data (for backward compatibility)
  step1_data?: Step1Data
  step2_data?: Step2Data
  step3_data?: Step3Data
  step4_data?: Step4Data
  step5_data?: Step5Data
  step6_data?: Step6Data
  step7_data?: Step7Data
  step8_data?: Step8Data
}

// Step-specific data structures
export interface Step1Data {
  keyword: string
  target_market: string
  article_language: string
}

export interface Step2Data {
  gen_search_intent: string | string[]
  selectedIntent?: string
}

export interface Step3Data {
  gen_topic_ideas: TopicIdea[]
  chosen_topic?: string
}

export interface TopicIdea {
  title: string
  description: string
  relevance_score?: number
}

export interface Step4Data {
  gen_research_data: string
  background_information?: string
}

export interface Step5Data {
  title_generation_demands?: string
  gen_article_titles: GeneratedTitle[]
  article_title?: string
}

export interface GeneratedTitle {
  title: string
  seo_score?: number
  length: number
  keywords_included?: string[]
}

export interface Step6Data {
  additional_knowledge_points?: string
  outline_demand?: string
  gen_article_outline: string
  article_outline?: string
}

export interface Step7Data {
  narrative_perspective?: string
  gen_article_content: string
  article_content?: string
}

export interface Step8Data {
  secondary_keywords?: string
  gen_optimized_article_content: string
  final_article_content: string
  seo_title: string
  seo_description: string
  url_example: string
  main_image_option: boolean
  sub_images_option: boolean
  final_article_html?: string
}

// API request/response interfaces
export interface WorkflowRequest {
  email: string
  node_input: any
  session_id?: number
  current_node_index?: number
  new_workflow?: boolean
}

export interface WorkflowResponse {
  code: number
  message: string
  data?: {
    session_id: number
    current_node_index: number
    status: string
    [key: string]: any
  }
}

export interface WorkflowStatusResponse {
  code: number
  message: string
  data?: WorkflowsModel
}

// Node input interfaces for each step
export interface Node1Input {
  keyword: string
  target_market: string
  article_language: string
}

export interface Node2Input {
  keyword: string
  target_market: string
  article_language: string
  search_intent: string
}

export interface Node3Input {
  keyword: string
  target_market: string
  article_language: string
  search_intent: string
  chosen_topic: string
}

export interface Node4Input {
  keyword: string
  target_market: string
  article_language: string
  chosen_topic: string
  research_data: string
  background_information?: string
}

export interface Node5Input {
  keyword: string
  target_market: string
  article_language: string
  chosen_topic: string
  article_title: string
  secondary_keywords?: string
  outline_demand?: string
  additional_knowledge_points?: string
}

export interface Node6Input {
  keyword: string
  target_market: string
  article_language: string
  article_title: string
  article_outline: string
  narrative_perspective: string
  main_image_option: boolean
  sub_images_option: boolean
}

export interface Node7Input {
  keyword: string
  secondary_keywords?: string
  article_language: string
  article_title: string
  additional_knowledge_points?: string
  article_content: string
}

export interface Node8Input {
  main_image_option: boolean
  sub_images_option: boolean
  gen_optimized_article_content: string
}