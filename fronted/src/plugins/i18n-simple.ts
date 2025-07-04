import { createI18n } from 'vue-i18n'

const messages = {
  en: {
    test: 'Test message',
    common: {
      loading: "Loading...",
      save: "Save",
      cancel: "Cancel",
      confirm: "Confirm",
      delete: "Delete",
      edit: "Edit",
      back: "Back",
      next: "Next",
      previous: "Previous",
      search: "Search",
      submit: "Submit",
      reset: "Reset",
      close: "Close",
      yes: "Yes",
      no: "No",
      error: "Error",
      success: "Success",
      warning: "Warning",
      info: "Information",
      back_home: "Back to Home",
      view: "View",
      retry: "Retry"
    },
    generation: {
      title: 'SEO Article Generator',
      steps: {
        step1: 'Keywords',
        step1_desc: 'Enter target keywords',
        step2: 'Intent Analysis',
        step2_desc: 'Analyze search intent',
        step3: 'Topic Selection',
        step3_desc: 'Choose your topic',
        step4: 'Title Generation',
        step4_desc: 'Generate article titles',
        step5: 'Outline Generation',
        step5_desc: 'Create content outline',
        step6: 'Article Generation',
        step6_desc: 'Generate full article',
        step7: 'Optimization',
        step7_desc: 'Optimize for SEO'
      },
      keywords: {
        title: 'Enter Your Target Keywords',
        description: 'Start by entering your main keyword and related long-tail keywords to generate SEO-optimized content.',
        main_keyword: 'Main Keyword',
        main_keyword_placeholder: 'Enter your primary keyword...',
        long_tail: 'Long-tail Keywords',
        long_tail_placeholder: 'Add related keywords...',
        tips: 'Press Enter to add each keyword. You can add up to 10 keywords.',
        language: 'Target Language',
        language_placeholder: 'Select target language',
        market: 'Target Market',
        market_placeholder: 'Select target market',
        suggestions: 'Keyword Suggestions',
        no_suggestions: 'Enter a main keyword to see suggestions',
        start_analysis: 'Start Analysis',
        analysis_started: 'Analysis started successfully!',
        analysis_failed: 'Analysis failed. Please try again.'
      },
      topics: {
        title: 'Topic Selection',
        description: 'Choose a topic for your article based on the search intent analysis.',
        ideas_title: 'Topic Ideas',
        select: 'Select',
        selected: 'Selected',
        edit_selected: 'Edit Selected Topic',
        edit_placeholder: 'Edit the selected topic to better match your content goals...',
        or_custom: 'Or Enter Custom Topic',
        custom_placeholder: 'Enter your own article topic...',
        please_select: 'Please select or enter a topic to continue',
        proceed_failed: 'Failed to proceed to next step',
        analysis_failed: 'Topic analysis failed'
      },
      intent: {
        title: 'Search Intent Analysis',
        description: 'Understanding user search intent helps create more targeted and relevant content.',
        select_instruction: 'Please select the search intent that best matches your content goals:',
        selected_intent: 'Selected Search Intent',
        please_select: 'Please select a search intent to continue',
        primary_intent: 'Primary Search Intent',
        secondary_intents: 'Secondary Intents',
        search_volume: 'Monthly Search Volume',
        competition: 'Competition Level',
        related_queries: 'Related Search Queries',
        queries_note: 'Select relevant queries to include in your content strategy',
        proceed_to_topics: 'Proceed to Topic Selection',
        analysis_complete: 'Intent analysis completed!',
        analysis_failed: 'Intent analysis failed',
        proceed_failed: 'Failed to proceed to next step',
        types: {
          informational: 'Informational',
          commercial: 'Commercial',
          transactional: 'Transactional',
          navigational: 'Navigational'
        },
        descriptions: {
          informational: 'Users are looking for information, answers, or how-to content',
          commercial: 'Users are researching products or services before making a decision',
          transactional: 'Users are ready to make a purchase or take a specific action',
          navigational: 'Users are looking for a specific website or page'
        },
        competition_levels: {
          low: 'Low',
          medium: 'Medium', 
          high: 'High'
        }
      },
      validation: {
        main_keyword_required: 'Main keyword is required',
        main_keyword_min: 'Main keyword must be at least 2 characters',
        language_required: 'Target language is required',
        market_required: 'Target market is required'
      },
      common: {
        error: 'Error',
        retry: 'Retry'
      }
    },
    loading: {
      analyzing: "Analyzing Search Intent",
      analyzing_desc: "Processing your keywords and understanding user intent",
      generating_topics: "Generating Topics",
      generating_topics_desc: "Creating relevant topic suggestions based on your keywords",
      generating_titles: "Generating Titles", 
      generating_titles_desc: "Creating SEO-optimized titles for your content",
      generating_outline: "Creating Outline",
      generating_outline_desc: "Structuring your article content logically",
      generating_article: "Writing Article",
      generating_article_desc: "Generating high-quality content based on your outline",
      optimizing: "Optimizing Content",
      optimizing_desc: "Fine-tuning your article for SEO and readability",
      default_title: "Processing...",
      default_subtitle: "Please wait while we process your request",
      status: {
        analyzing_keywords: "Analyzing your keywords...",
        processing_intent: "Processing search intent...",
        gathering_data: "Gathering relevant data...",
        preparing_results: "Preparing results...",
        analyzing_market: "Analyzing target market...",
        identifying_trends: "Identifying content trends...",
        generating_ideas: "Generating topic ideas...",
        ranking_topics: "Ranking topic relevance...",
        optimizing_seo: "Optimizing for SEO...",
        creating_variations: "Creating title variations...",
        scoring_titles: "Scoring title effectiveness...",
        structuring_content: "Structuring content flow...",
        organizing_sections: "Organizing article sections...",
        planning_flow: "Planning content flow...",
        finalizing_outline: "Finalizing outline structure...",
        writing_introduction: "Writing introduction...",
        developing_content: "Developing main content...",
        adding_details: "Adding supporting details...",
        polishing_text: "Polishing final text...",
        analyzing_content: "Analyzing content quality...",
        checking_seo: "Checking SEO optimization...",
        improving_readability: "Improving readability...",
        finalizing_article: "Finalizing your article..."
      }
    }
  }
}

export const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages,
  globalInjection: true
})