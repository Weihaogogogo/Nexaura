#节点3: 生成深度调研报告

import os
import re
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_tavily import TavilySearch, TavilyExtract
import time
import datetime
from flask import jsonify
from models.WorkflowsModel import WorkflowsModel
from exts import db

load_dotenv()

def generate_deep_research_report_and_article_titles(node_input, email, session_id, model_1="grok-3-deepsearch",model_2="gemini-2.5-flash-preview-05-20",api_key=os.getenv("GROK_API_KEY"),base_url=os.getenv("BLT_BASE_URL")):
    try:
        #node_input中有的数据，直接获取
        chosen_topic = node_input.get('chosen_topic')
        background_information = node_input.get('background_information')
        title_generation_demands = node_input.get('title_generation_demands')
        #node_input中没有的数据，需要从数据库中获取
        workflow = WorkflowsModel.query.filter_by(email=email, session_id=session_id).first()

        article_language = workflow.article_language
        search_intent = workflow.search_intent
        keyword = workflow.keyword
        target_market = workflow.target_market
        #research_data在数据库中没有，需要llm_1生成,生成后可以直接在llm_2中使用

        
        #生成深度调研报告research_data
        llm_1 = ChatOpenAI(model=model_1, api_key=api_key,base_url=base_url)
        messages = [
            SystemMessage("You are a Research Analyst specializing in information retrieval for RAG-enhanced SEO content. Your goal is to find diverse, credible evidence (data, expert opinions, user reviews, arguments)."),
            HumanMessage(f""""
            *Context for RAG:
            This information will directly feed a RAG system to enrich an SEO article. Output must be structured, concise, and consist of raw facts/quotes for easy parsing.

            *Inputs:
            1.  **USER_SEARCH_INTENT**: "{search_intent}"
            2.  **PRIMARY_KEYWORD**: "{keyword}"
            3.  **ARTICLE_TOPIC**: "{chosen_topic}"
            4.  **ARTICLE_LANGUAGE**: "{article_language}"
            5.  **(Optional) SECONDARY_KEYWORDS**: "{target_market} {keyword}"

            *Task: Deep Research for Actionable Information
            Based on the `ARTICLE_TOPIC`, `PRIMARY_KEYWORD`, and `USER_SEARCH_INTENT`, conduct in-depth research. Collate a diverse set of actionable information points suitable for substantiating claims in an SEO article.

            *Demand
            1. you must just collect information from 40,50 sources, do not collect too many sources.

            *Information Categories to Collect (Prioritize recency & direct evidence):
            1.  **Data & Statistics:** Recent, verifiable numbers (cite sources).
            2.  **Expert Quotes:** Attributed statements from credible individuals/publications (cite sources).
            3.  **User Sentiment (from Twitter, Reddit, Review Sites, Forums):**
                * Direct positive/negative user quotes.
                * Summarized common themes/pain points.
            4.  **Arguments & Viewpoints:** Pros & Cons, key arguments for/against.
            5.  **Examples & Case Studies:** Brief, illustrative real-world instances.
            6.  **FAQs:** Common questions related to the topic.
            7.  **Unique Insights/Trends:** Novel perspectives or emerging information.

            *Key Information Sources:
            Google (news, academic, reputable blogs, official reports), Twitter/X, Reddit, Professional Review Websites (e.g., G2, Capterra for software; industry-specific sites), YouTube (reviews, expert interviews), Quora.

            *Output Requirements:
            1.  **Format:** Structured, itemized list using markdown, categorized by "Information Categories" above.
            2.  **Content:** Provide direct facts and verbatim quotes. Be concise. NO article prose.
            3.  **Relevance:** All information must be highly relevant to the inputs.
            4.  **Attribution:** Crucially, cite sources (URL or Name/Publication) for all data and quotes.
            5.  **Purpose:** Deliver raw, actionable information for RAG. DO NOT write any article content.
            """)
        ]
        #修改数据库中的loading_text，显示正在生成research_data
        workflow.loading_text = "正在生成深度研究报告..."
        db.session.commit()

        #调用llm_1生成research_data
        research_data = ""
        for token in llm_1.stream(messages):
            print(token.content, end="")
            research_data += token.content

        #将research_data保存到数据库中
        workflow.research_data = research_data
        db.session.commit()
    except Exception as e:
        error_message = f"节点执行失败 - 用户:{email}, 工作流id:{session_id}, 错误阶段：在节点2中生成深度研究报告阶段发生错误，错误详情：{e}"
        logging.error(error_message)
        return {'status': 'failed', 'message': error_message}
#-----------------------------------------------------------
    try:
        #生成文章标题
        llm_2 = ChatOpenAI(model=model_2, api_key=api_key,base_url=base_url)
            #1. 初始化tavily搜索工具
        search_tool = TavilySearch(
                    max_results=6,  # 限制结果数量为6个
                    include_generated_answer=False,  # 不需要生成的回答
                    include_raw_content=False,  # 不需要原始内容
                    include_images=False,  # 不需要图片
        )
        #2. 执行搜索查询
        #修改数据库中的loading_text，显示正在搜索类似文章标题
        workflow.loading_text = "正在搜索类似文章标题..."
        db.session.commit()
        #调用tavily搜索工具
        search_query = f"{chosen_topic} {keyword} {target_market}"
        search_response = search_tool.invoke({"query": search_query})

        #3. 处理tavily返回结果
        ##3.1 提取搜索结果（去除query等辅助信息，只保留搜索的结果）
        if isinstance(search_response, dict): #当搜索结果为空时，tavily会返回字符串
            search_results = search_response['results']
            print(f"search_results: {search_results}")
        else:
            search_results = ""
        ##3.2 提取搜索标题
        search_titles = []
        for result in search_results:
            search_titles.append(result['title'])
        search_titles_text = "\n".join(search_titles)
        print(search_titles_text)

        #4. 提炼research_data为research_insights
        #修改数据库中的loading_text，显示正在提炼研究洞察
        workflow.loading_text = "正在提炼研究洞察..."
        db.session.commit()
        #调用llm_2提炼research_data为research_insights
        model_step4 = ChatOpenAI(
            model=model_2, 
            api_key=api_key,
            base_url=base_url,
            reasoning_effort="none"
            )
        prompt_extraction = f"""The following text is research_data. Please extract the 'Data and Statistics', 'Expert Quotes', 'Unique Insights/Trends' sections for a point by point summary output (try to keep the original text and avoid making major changes):

        {research_data}
        """
        research_insights = ""
        for token in model_step4.stream(prompt_extraction):
            print(token.content, end="")
            research_insights += token.content
        
        #5. 调用大模型进行标题生成
        #修改数据库中的loading_text，显示正在生成文章标题
        workflow.loading_text = "正在生成文章标题..."
        db.session.commit()
        #调用llm_2生成文章标题
        model_step5 = ChatOpenAI(model=model_2, api_key=api_key,base_url=base_url)
        messages = [
            SystemMessage("You are an AI product expert, Senior SEO writer, Google SEO expert, and an enthusiastic member of the AI product community, skilled in writing professional, in-depth, and uniquely insightful SEO articles."),
            HumanMessage(f""""
                        ## Inputs:
                        * **Article Topic:** [{chosen_topic}]
                        * **User Search Intent:** [Analyze the top 10 SERP results of Google]
                        * **Target Market:** [{target_market}]
                        * **Keyword:** [{keyword}]
                        * **Article Title language** `[{article_language}]`
                        * **Background Information:** `[{background_information}]`
                        * **Title Generation Demands:** `[{title_generation_demands}]`
                        * **SERP Analysis Results:** 
                        ```
                        {search_titles_text}
                        ```{research_insights}

                                ## Task:
                                Your goal is to generate 5 compelling and SEO-friendly article titles based on the provided inputs. Follow these steps:

                                1.  **Analyze Search Results:**
                                * Review the provided SERP titles carefully
                                * Identify patterns, common formats, and approaches used by top-ranking articles
                                * Note any keywords or phrases that appear frequently
                                * Understand the dominant angle or perspective taken on the topic

                                2.  **Analyze Article Types & Structures:**
                                * Identify common article formats and structures used in the search results (e.g., "How-to," "Best X," "Comparison," "Ultimate Guide," "Why X Matters")
                                * Determine which title structures appear most frequently in top results

                                3.  **Strategic Title Development:**
                                * Incorporate the target keyword naturally in most titles
                                * Ensure alignment with the identified user search intent
                                * Create titles that stand out from existing content while addressing similar needs
                                * Apply proven SEO title patterns but with unique angles
                                * Ensure all titles are under 70 characters as specified
                                * Make titles attractive, compelling, and click-worthy

                                4.  **Generate Titles:**
                                * Create 5 distinct, clear, engaging, and SEO-optimized title options
                                * Aim for variety in structure and approach (question-based, benefit-driven, list-based, etc.)
                                * Ensure each title offers a unique value proposition

                                        ## Output Format:
                                Present exactly 5 generated titles ONLY, one per line, with NO headings, explanations, or additional text.
                                DO NOT include any numbering, bullets, or formatting.
                                DO NOT include introductory text like "Here are 5 titles..." or concluding text.
                                DO NOT include any formatting markers like # or *.
                                Each title must be under 70 characters.
                                if user choose Write a "List" blog post, you can randomly offer the numbers of products to be listed in the article, such as 5, 6, 7, 8, 9, 10.
                                if there is date in the article title, make sure it is the current year.(check the current date), for example, 2025, 2026, 2027, 2028, 2029, 2030.

                                Example of correct output format:
                                10 Best SEO Writing Tools to Elevate Your Content Strategy
                                Top SEO Writing Tools to Optimize Your Content in 2025
                                The Ultimate List of SEO Writing Tools for Better Rankings
                                10 Must-Have Tools for SEO Writing Success
                                Best Tools for SEO Writing You Need to Know in 2025
                                Essential SEO Writing Tools for Smarter Content Creation
                            """)
        ]
        article_titles = ""
        for token in model_step5.stream(messages):
            print(token.content, end="")
            article_titles += token.content
        # 使用正则表达式匹配一个或多个空行作为分隔符,输出主题列表数组
        arr_article_titles = [title.strip() for title in re.split(r'\n+', article_titles) if title.strip()]
        #修改loading_text，显示加载中
        workflow.loading_text = "加载中"
        return {'research_data':research_data,'gen_article_titles':arr_article_titles}
    except Exception as e:
        error_message = f"节点执行失败 - 用户:{email}, 工作流id:{session_id}, 错误阶段：在节点2中生成文章标题阶段发生错误，错误详情：{e}"
        logging.error(error_message)
        return {'status': 'failed', 'message': error_message}