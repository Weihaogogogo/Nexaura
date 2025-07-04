#节点1: 分析搜索意图
import os
import re
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_tavily import TavilySearch, TavilyExtract
from flask import jsonify
from models.WorkflowsModel import WorkflowsModel
from exts import db

load_dotenv()

def get_search_intent_and_topic_ideas(node_input, email, session_id, model="grok-3-deepsearch",api_key=os.getenv("GROK_API_KEY"),base_url=os.getenv("BLT_BASE_URL")):
    try:
        keyword = node_input.get('keyword')
        target_market = node_input.get('target_market')
        article_language = node_input.get('article_language')
        workflow = WorkflowsModel.query.filter_by(email=email, session_id=session_id).first()
        #调研用户意图 - 初始化模型,流式调用模型返回完整结果
        model = ChatOpenAI(model=model, api_key=api_key,base_url=base_url)
        messages = [
            SystemMessage("You are an AI product expert, Senior SEO writer, Google SEO expert, an enthusiastic member of the AI product community. You are very good at writing professional, in-depth, and uniquely insightful SEO articles."),
            HumanMessage(f""""
                        *Task：
                        1. Now, based on the keyword "{keyword}" , analyze the user search intent from the Google SERP results related to the product. Determine what problems they want to solve. 
                        2. For the search intent obtained in the previous step, cross-verify it with the SERP results of Google search related to the product from the provided link to ensure that the search intent reflects the genuine search intent of users in the American market.
                        *Demand：
                        3. I need the latest user search intent
                        4. Once you identify the search intent for the keyword , output the search intent point by point. 
                        5. Only offer me top 6 user search intent for "{target_market}" market
                        6. I strongly ask you to output the search intent report in "{article_language}"
                            for example: if the aricle_language = English, then output the search intent report in English
                                        if the aricle_language = Spanish, then output the search intent report in Spanish
                            """)
        ]
        search_intent_result = ""
        #修改数据库中的loading_text，显示正在生成用户搜索意图
        workflow.loading_text = "正在生成用户搜索意图..."
        db.session.commit()
        #调用模型生成搜索意图
        for token in model.stream(messages):
            print(token.content, end="")
            search_intent_result += token.content

        #提取要点 - 初始化模型，流式调用模型获取总结提取后的6个用户搜索意图
        model = ChatOpenAI(
            model="gemini-2.5-flash-preview-05-20", 
            api_key=os.getenv("GROK_API_KEY"),
            base_url=os.getenv("BLT_BASE_URL"),
            reasoning_effort="none"
            )
        prompt_extraction = f"""
    Your task is to analyze the following text, enclosed in triple backticks, and extract exactly 6 primary user search intents.

    You must adhere to the following rules for your output:
    1.  Provide exactly 6 search intents.
    2.  Format the output as a numbered list (1., 2., 3., etc.).
    3.  Each intent must be on a new line.
    4.  Your response must contain ONLY the numbered list. Do NOT include any introductory phrases like "Here are the search intents:", explanations, or any concluding remarks.

    **Output Format Example1:**
    1. Get the latest NBA news and updates
    2. Find the schedule of upcoming NBA games
    3. Check the current standings of NBA teams
    4. Access player and team statistics
    5. Watch NBA games or highlights
    6. Learn about the NBA (history, rules, etc.)

    **Output Format Example2:**
    1. Understand what the keto diet is and how it works
    2. Find a list of foods to eat and to avoid
    3. Get a beginner's meal plan and recipes
    4. Learn about the potential benefits and health risks
    5. Read success stories and see before-and-after results
    6. Find keto-friendly products or supplements to buy

    **Output Format Example3:**
    1. Find top tourist attractions and landmarks
    2. Discover unique local experiences and hidden gems
    3. Get sample itineraries for a trip (e.g., 3-day, 5-day)
    4. Look for recommendations on food and restaurants
    5. Find information on booking tickets or tours
    6. Learn about transportation options like the subway system

    Now, analyze the following text and generate the output.
    ```
    {search_intent_result}
    ```
        """
        search_intent = ""
        #修改数据库中的loading_text，显示正在提取用户搜索意图
        workflow.loading_text = "正在提取用户搜索意图..."
        db.session.commit()
        #调用模型提取用户搜索意图
        for token in model.stream(prompt_extraction):
            print(token.content, end="")
            search_intent += token.content
        #-----------------------
            #初始化一个搜索工具
        search_tool_2 = TavilySearch(
                    max_results=7,  # 获取前7个结果
                    include_generated_answer=False,
                    include_raw_content=False,
                    include_images=False,
                )
        #调用搜索工具:

        search_query_2 = f"{keyword}\n{search_intent}\n{target_market}"

        ##tavilySearch的query字符长度限制为400，需要对query进行校验，如果大于400则对search_intent进行截断
        while len(search_query_2) > 400:
            lines = search_query_2.split("\n") #切分每一行成为数组
            lines.pop(-2) #删除倒数第二个元素，因为倒数第一个时target_market，倒数第二个则为search_intent的最后一行
            search_query_2 = '\n'.join(lines)
        #修改数据库中的loading_text，显示正在搜索相关内容
        workflow.loading_text = "正在搜索相关内容..."
        db.session.commit()
        #调用搜索工具
        search_results_2 = search_tool_2.invoke({"query": search_query_2})

        #处理tavily返回结果:
        search_insights_2 = []
        for result in search_results_2['results']:  # 直接从字典中获取results列表
            insight = f"- Title: {result.get('title', 'N/A')}"
            if result.get('url'):
                insight += f" (URL: {result.get('url')})"
            if result.get('content'):
                insight += f"\n  Snippet: {result.get('content')[:250]}..."
            search_insights_2.append(insight)
        search_insights_text_2 = "\n".join(search_insights_2)
        #初始化大模型，流式调用生成主题创意
        model_2 = ChatOpenAI(model="gemini-2.5-flash-preview-05-20", api_key=api_key,base_url=base_url)
        prompt_2 = f"""*Inputs:* 
        * **Keyword:** `[{keyword}]`
        * **User Search Intent:** `[{search_intent}]`
        * **Article Topic Ideas language** `[{article_language}]`
        * **Relevant Search Insights (from Tavily):**
        ```
        {search_insights_text_2}
        ```

        *Task：*
        Based on the provided **Keyword**, **User Search Intent**, and **Relevant Search Insights**, generate 6 to 8 distinct and relevant article topic ideas.
        Analyze the relationship between the keyword, intent, and the current top-ranking content (from search insights) to ensure the topics directly address what a user searching for this keyword likely wants to know or achieve, and offer a unique or comprehensive angle.
        Prioritize topics that are commonly associated with the keyword/intent and have strong potential to attract organic traffic.

                *Requirements & Formatting:*
                * For each topic, determine the most appropriate "article type" (e.g., "What is", "How to", "Best", "Comparison", "List", "Guide", "Why", "Review").
                * Present each topic using the exact format below:
                * Write a "[Article Type]" blog post on "[Article Topic Title]" ([Search Intent Type])
                * I strongly demand you to output the article topics in Article Topic Ideas language "{article_language}"
                
                *Example Output (if Keyword was "AI prompt engineering" and Intent was Informational):*
            Write a 'Listicle' blog post on 'Top 10 SEO Writing Tools for 2025' commercial
            Write a 'Comparison' blog post on 'SEO Writing Tools: Features, Pricing, and Performance' commercial 
            Write a 'How' blog post on 'How to Use SEO Writing Tools to Improve Content Rankings' Information
            Write a 'Tips' blog post on 'Tips for Choosing the Best SEO Writing Tool for Your Needs' Information
            Write a 'Review' blog post on 'In-Depth Review of the Top AI SEO Writing Tools in 2025' commercial 
            Write a 'Why' blog post on 'Why SEO Writing Tools Are Essential for Content Creators in 2025' Information
            Write a 'Steps' blog post on 'Steps to Optimize Your Content Using SEO Writing Tools' Information
            Write a 'Ranking' blog post on 'Ranking the Best Free SEO Writing Tools for 2025' commercial 

                *Instructions for AI:*
        Analyze all inputs carefully. Use the **Relevant Search Insights** to understand what content already exists and to identify potential gaps or opportunities for new topic ideas.
        Ensure the generated topics are specific, compelling, and directly satisfy the user's likely need based on the provided keyword and search intent, while also considering the competitive landscape shown in the search insights.
        Select article types that logically fit the topic and intent.

        Keep the topic ideas for output (do not change the content inside) and discard other content. Output one empty line for each topic idea."""
        topic_idea_result = ""
        #修改数据库中的loading_text，显示正在生成主题创意
        workflow.loading_text = "正在生成主题创意..."
        db.session.commit()
        #调用模型生成主题创意
        for token in model_2.stream(prompt_2):
            print(token.content, end="")
            topic_idea_result += token.content
        # 使用正则表达式匹配一个或多个空行作为分隔符,输出主题列表数组
        arr_topic_idea = [topic.strip() for topic in re.split(r'\n+', topic_idea_result) if topic.strip()]
        #修改loading_text，显示加载中
        workflow.loading_text = "加载中"
        return {'gen_search_intent':search_intent, 'gen_topic_ideas':arr_topic_idea}
    except Exception as e:
        error_message = f"节点执行失败 - 用户:{email}, 工作流id:{session_id}, 错误阶段：在节点1中生成用户搜索意图和主题创意阶段发生错误，错误详情：{e}"
        logging.error(error_message)
        return {'status': 'failed', 'message': error_message}
