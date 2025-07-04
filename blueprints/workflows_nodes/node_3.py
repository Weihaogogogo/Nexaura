#节点5: 生成文章大纲

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
from utils.seo_title_generator import optimize_seo_title
from utils.url_example_generator import format_title_to_slug

load_dotenv()

def generate_article_outline(node_input, email, session_id, model="o3-mini", api_key=os.getenv("GROK_API_KEY"),base_url=os.getenv("BLT_BASE_URL")):
    try:
        #node_input中有的数据，直接获取
        article_title = node_input.get('article_title')
        secondary_keywords = node_input.get('secondary_keywords','')
        outline_demand = node_input.get('outline_demand','')
        additional_knowledge_points = node_input.get('additional_knowledge_points','')
        #node_input中没有的数据，需要从数据库中获取
        workflow = WorkflowsModel.query.filter_by(email=email, session_id=session_id).first()
        chosen_topic = workflow.chosen_topic
        article_language = workflow.article_language
        keyword = workflow.keyword
        target_market = workflow.target_market
        
        #1. 使用tavily搜索工具
        #1.1 初始化搜索工具
        search_tool = TavilySearch(
            max_results=8,  # 专注于前8个结果以获取大纲结构
            include_generated_answer=False,
            include_raw_content=False,
            include_images=False,
        )
        search_query = f"{article_title}\n{keyword}\n{target_market}" 
        #1.2 调用搜索工具
        #修改数据库中的loading_text，显示正在搜索相关内容
        workflow.loading_text = "正在搜索相关内容..."
        db.session.commit()
        search_response = search_tool.invoke({"query": search_query})
        #1.3 提取搜素结果（只保留results）
        if isinstance(search_response, dict): #当搜索结果为空时，tavily会返回字符串
            search_results = search_response['results']
            print(f"search_results: {search_results}")
        else:
            search_results = ""
        #1.4 提取搜索的url成数组
        urls_to_extract = []
        for result in search_results:
            urls_to_extract.append(result['url'])
        #2. 使用tavily提取工具
        #2.1 初始化解析工具
        extract_tool = TavilyExtract(
            extract_depth="advanced",
            include_images=False,
        )
        #2.2 调用解析工具
        if not search_results == "":
            #修改数据库中的loading_text，显示正在提取页面内容
            workflow.loading_text = "正在提取页面内容..."
            db.session.commit()
            #调用解析工具
            extraction_results = extract_tool.invoke({"urls": urls_to_extract})
            #2.3 提取页面内容为数组
            extracted_contents = []
            for result in extraction_results["results"]:
                extracted_contents.append(f"--- Content from {result.get('url', 'Unknown URL')} ---\n{result['raw_content'][:5000]}...")
            #2.4 合并提取内容为新变量
            extracted_text = "\n\n".join(extracted_contents)
        else:
            extracted_text=""

        #3. 调用大模型
        model = ChatOpenAI(model=model, api_key=api_key,base_url=base_url)
        messages = [
            SystemMessage("You are an AI product expert, Senior SEO writer, Google SEO expert, skilled in writing professional, in-depth, and uniquely insightful SEO articles. Your article outline is very concise and clear."),
            HumanMessage(f""""
                        Inputs:
                            1. Chosen Article Title: [{article_title}]
                            2. Primary Keyword: [{keyword}]
                            3. Secondary Keywords: [{secondary_keywords}]
                            4. Core Article Topic: [{chosen_topic}]
                            5. Article Outline language [{article_language}]
                            6. Additional Knowledge Points: [{additional_knowledge_points}]
                            7. Outline demand: [{outline_demand}]
                            8. SERP Content Analysis:
                                                    {extracted_text}                        
                            You need to analyze the extracted content, examining the outline and writing style of each article. Then use the outline of an article as reference material.

                                    ## Output:
                            Provide only the generated article outline in Markdown format.

                                    ## Article Outline Requirements:
                                    * Keyword Distribution in Headings:
                                        * The Primary Keyword (or a very close, natural-sounding variation) MUST be logically and strategically integrated into relevant H2 headings.
                                        * Secondary Keywords (or very close, natural-sounding variations) MUST be distributed logically and strategically within relevant H3 and H4 headings where appropriate.
                                * Avoid keyword stuffing; integration must be natural and contextually relevant.

                            * Structure Requirements:
                                        * The H1 of the outline will be the Chosen Article Title.
                                * Include "Key Takeaways" as an H2 section. only generate Key Takeaways title, do not generate the content of Key Takeaways in the outline. "Key Takeaways" must be just below the H1 title, "Key Takeaways" as an H2 section must be the first H2 section of the whole article outline
                                * Include "FAQs" as an H2 section with question titles as H3 headings.
                                * Include "Conclusion" as an H2 section.

                            *   Heading Numbering Rules:
                                1.  General Headings (Non-List Items/Sections):
                                    *   Prohibited: Do not use numerical prefixes (e.g., 1., 2., a., b.).
                                    *   Use the heading text directly.
                                    *   Example: Introduction, Understanding [Primary Keyword], Advanced Strategies for [Primary Keyword], Conclusion.
                                2.  Specific List Item/Enumerated Headings (Applicable to "Listicle-style" content or enumerated steps/features):
                                    *   Required: Must use numerical prefixes (e.g., 1., 2., 3.).
                                    *   This applies when discussing multiple distinct products, tools, features, steps, methods, or elements that form a list.
                                    *   Numerical prefixes should ONLY be applied to the H2 or H3 headings representing these individual, enumerated items.
                                    *   Example (H2 as list items):
                                        *   H2: 1. [Tool/Product/Step A]
                                        *   H2: 2. [Tool/Product/Step B]
                                    *   Example (H3 as list items under a thematic H2):
                                        *   H2: Top Strategies for [Task]
                                            *   H3: 1. Strategy One Details
                                            *   H3: 2. Strategy Two Details

                            * General Guidelines:
                                * Only use numbers in the outline when referring to specific products/tools or in listicle-style articles.
                                * The outline should be concise and not redundant.
                                * All headings must be clear, engaging, and naturally incorporate keywords.
                                * The headings number to follow the top search results, for example: top 1 search result has 7 H2 titles, 10 H3 titles, then the outline you generated should follow this heading quanatity, do not generate too much headings
                                * Every headings must be short, clear and concise, do not generate too many words in each heading
                                * Do not include too many H3 headings in a single paragraph.
                                * Under an H2 heading, there should be no more than 4 H3 headings, and under an H3 heading, there should be no more than 3 H4 headings.
                                * when introducing products in list/comparison/ranking/why/steps/review/why/steps/ranking, the product name should be H2 title, and overivew, key features, pros, cons ,reviews should be H3 title separately, do not output title like Overview & Key Features, dont mix them together.

                                    ## Task:
                            Your process should be as follows:

                            1.  Deep SERP Analysis & Insight Extraction:
                                *   Thoroughly analyze the provided SERP Content Analysis ({extracted_text}).
                                *   Identify the common H2/H3 structures, recurring themes, and content angles used by top-ranking articles.
                                *   Critically assess their strengths and weaknesses. Note how they incorporate keywords (both effectively and ineffectively).
                                *   Crucially, pinpoint content gaps, unanswered user questions, or areas where depth could be significantly improved. This is key for creating a superior outline.
                                *   Note the typical keyword density and distribution patterns in headings without aiming to replicate them unnaturally.

                            2.  Strategic Outline Generation:
                                *   Based on your SERP insights, and primarily driven by the Chosen Article Title, Primary Keyword, Secondary Keywords, Core Article Topic, and any Additional Knowledge Points or Outline Demand, construct a unique and comprehensive article outline.
                                *   Prioritize creating a structure that offers a superior user experience and more thorough information than existing top content.
                                *   Ensure a logical flow between sections, guiding the reader seamlessly through the topic.
                                *   Integrate keywords naturally and strategically as per the "Keyword Integration Strategy."
                                *   Adhere strictly to all "Structural Mandates," "Heading Numbering Rules," and "General Outline Quality Guidelines."
                                *   The final outline should be a distinct piece of work that, if developed into a full article, would have a strong potential to outperform existing content by addressing user needs more completely and with greater insight.

                            Please only output the markdown outline with no additional text or explanation.
                            """)
        ]
        article_outline = ""
        #修改数据库中的loading_text，显示正在生成文章大纲
        workflow.loading_text = "正在生成文章大纲..."
        db.session.commit()
        #调用模型生成文章大纲
        for token in model.stream(messages):
            print(token.content, end="")
            article_outline += token.content
        
        #提取markdown内容
        model_extract = ChatOpenAI(
            model="gemini-2.5-flash-preview-05-20", 
            api_key=os.getenv("GROK_API_KEY"),
            base_url=os.getenv("BLT_BASE_URL"),
            reasoning_effort="none"
            )
        prompt_extract = f'''
    Your task is to extract the pure Markdown article outline from the following text.

    Rules:
    1.  Only keep the heading lines that start with '#' (e.g., `#`, `##`, `###`).
    2.  Delete all non-Markdown parts, including any explanatory text, introductions, or conclusions.
    3.  **You MUST NOT include any Markdown code block fences, such as ` ```markdown ` or ` ``` `.**
    4.  Do not modify or add anything to the retained outline content.
    5.  Your output must begin directly with the first Markdown heading.

    ***Text to process: {article_outline}
                        '''
        article_outline_pured = ""
        for token in model_extract.stream(prompt_extract):
            print(token.content, end="")
            article_outline_pured += token.content

        #修改loading_text，显示加载中
        workflow.loading_text = "加载中"

        #4. 生成seo标题
        seo_title = optimize_seo_title(article_title)
        url_example = format_title_to_slug(seo_title)

        return {'gen_article_outline':article_outline_pured, 'seo_title':seo_title, 'url_example':url_example}
    except Exception as e:
        error_message = f"节点执行失败 - 用户:{email}, 工作流id:{session_id}, 错误阶段：在节点3中生成文章大纲阶段发生错误，错误详情：{e}"
        logging.error(error_message)
        return {'status': 'failed', 'message': error_message}