#节点6: 生成文章内容

import os
import re
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_tavily import TavilySearch, TavilyExtract
import time
import datetime
from blueprints.workflows_nodes.narrative_perspective import perspective
from flask import jsonify
from models.WorkflowsModel import WorkflowsModel
from exts import db
from blueprints.workflows_nodes.gen_image_functions import gen_image, gen_task_with_urls, assemble_markdown, md_to_HTML, extract_json_from_llm_output, llm_to_dict, gen_task
from utils.article_description import generate_article_summary

load_dotenv()

def generate_article_and_optimize_article_and_gen_image(node_input, email, session_id, model="claude-3-7-sonnet-20250219",api_key=os.getenv("GROK_API_KEY"),base_url=os.getenv("BLT_BASE_URL")):
    try:
        #node_input中有的数据，直接获取
        article_outline = node_input.get('article_outline')
        narrative_perspective = node_input.get('narrative_perspective')
        main_image_option = node_input.get('main_image_option')
        sub_images_option = node_input.get('sub_images_option')
        #node_input中没有的数据，需要从数据库中获取
        workflow = WorkflowsModel.query.filter_by(email=email, session_id=session_id).first()
        article_language = workflow.article_language
        keyword = workflow.keyword
        target_market = workflow.target_market
        article_title = workflow.article_title
        additional_knowledge_points = workflow.additional_knowledge_points
        secondary_keywords = workflow.secondary_keywords
        #--------------------------------generate article--------------------------------
        #0. 设置用户视角, narrative_perspective == '1'时为第一人称，否则是第二人称
        current_perspective = perspective()
        current_perspective.set_perspective(narrative_perspective)
        perspective_instruction = current_perspective.instruction
        perspective_examples = current_perspective.example

        print(f'人称视角： 第{narrative_perspective}人称')

        #1. tavily搜索工具
        #1.1 初始化搜索工具
        search_tool_1 = TavilySearch(
            max_results=15,  # 限制结果数量为5个，避免提取过多内容
            include_generated_answer=False,
            include_raw_content=False,
            include_images=False,
        )
        search_query_1 = f"{article_title}\n{keyword}\n{target_market}"
        #1.2 调用搜索工具
        #修改数据库中的loading_text，显示正在搜索相关内容
        workflow.loading_text = "正在搜索相关内容..."
        db.session.commit()
        search_response_1 = search_tool_1.invoke({"query": search_query_1})
        if isinstance(search_response_1, dict): #当搜索结果为空时，tavily会返回字符串
            search_results_1 = search_response_1['results']
            print(f"search_results_1: {search_results_1}")
        else:
            search_results_1 = ""
        #1.4 提取搜索标题成数组，以及url成数组
        search_insights_1 = []
        urls_to_extract_1 = []
        for result in search_results_1:
            search_insights_1.append(result['title'])
            urls_to_extract_1.append(result['url'])
        search_insights_text_1 = '\n'.join(search_insights_1)

        #2. 使用tavily提取工具
        #2.1 初始化解析工具
        extract_tool_1 = TavilyExtract(
            extract_depth="advanced",
            include_images=False,
        )
        #2.2 调用解析工具
        if not search_results_1 == "":
            #修改数据库中的loading_text，显示正在提取相关内容
            workflow.loading_text = "正在提取相关内容..."
            db.session.commit()
            extraction_results_1 = extract_tool_1.invoke({"urls": urls_to_extract_1})
            #2.3 提取页面内容为数组
            extracted_contents_1 = []
            for result in extraction_results_1["results"]:
                extracted_contents_1.append(f"--- Content from {result.get('url', 'Unknown URL')} ---\n{result['raw_content'][:6000]}...")
            #2.4 合并提取内容为新变量
            extracted_text_1 = "\n\n".join(extracted_contents_1)

        #3. 调用大模型
        llm_generate = ChatOpenAI(model=model, api_key=api_key, base_url=base_url)
        messages = [
            SystemMessage("You are an Expert SEO Article Writer with a specialization in writing deeply insightful, and SEO-optimized articles that demonstrably align with Google's E-E-A-T guidelines."),
            HumanMessage(f""""
                        ## Inputs:
                            1. **Article Title:** [{article_title}]
                            2. **Target Market:** [{target_market}]
                            3. **Article Outline:** [{article_outline}]
                            4. **Additional Knowledge Points/Unique Angles:** []
                            5. **Primary Keyword(s):** [{keyword}]
                            6. **Article language** `[{article_language}]`
                            7. **Research Findings:** 
                            ```
                            Search Insights:
                            {search_insights_text_1}

                            Extracted Content:
                            {extracted_text_1}
                            ```

                            ## Article Specifications:
                                    Adhere closely to these requirements:

                            * **E-E-A-T Driven Content:**
                                * **Experience:** Demonstrate practical knowledge and first-hand understanding of the topic
                                * **Expertise:** Show deep technical knowledge and industry insights
                                * **Authoritativeness:** Cite authoritative sources from the Research Findings
                                * **Trustworthiness:** Ensure factual accuracy and transparent information presentation

                                    * **Content Quality & Depth:**
                                        * **Clarity and Conciseness:** Write in clear, direct language. Avoid jargon where possible or explain it simply. Every sentence should add value.
                                * **Actionable Insights:** Include practical advice and applicable takeaways
                                * **Latest Information:** Incorporate recent developments, statistics, and trends from the Research Findings
                                * **Do not use fancy words, try to express the content clearly and concisely

                                    * **Key Takeaways:** Place a bulleted list of 3-5 main takeaways (each with a relevant Emoji 💡, ✅, 🎯, 🚀, etc.) at the very beginning of the article content, immediately after the H1 title.

                            * **Target Word Count:** 2000-2500 words
                            * **Target Audience:** Easily understood by a high school graduate
                            * **Tone:** Professional with appropriate humor
                            {perspective_instruction}

                                    * **Narrative Perspective Guidelines:**
                            {perspective_examples}

                                    * **Formatting:**
                                * Strictly follow the provided article outline
                                * Use appropriate heading hierarchy (H1, H2, H3, etc.)
                                * Include bullet points, numbered lists, and short paragraphs for readability
                                *  **Heading Separation Rules:**
                                    - Insert exactly ONE blank line before every heading (H1-H6)
                                    - Insert exactly ONE blank line after every heading (H1-H6)
                                    - This applies to ALL heading level transitions (H1→H2, H2→H3, H3→H2, etc.)

                                    2. **Content Block Separation:**
                                    - ONE blank line between headings and any following content
                                    - ONE blank line between separate paragraphs
                                    - ONE blank line before and after: lists, code blocks, tables, blockquotes, horizontal rules

                                    3. **Strict Compliance:**
                                    - NO exceptions to these rules
                                    - Every heading must be isolated by blank lines
                                    - Every content block must be properly separated
                                    - Failure to follow these rules is unacceptable

                                    4. **Validation Requirement:**
                                    - Your output must pass standard markdown parsers
                                    - All formatting must render correctly in markdown viewer

                            * **Comparison Table:** Include a comprehensive comparison table near the end of the article (before Conclusion/FAQs) that compares all discussed tools/concepts with columns for key parameters, advantages, and disadvantages.

                            ## Content Enhancement Instructions:

                            1. **User Intent Alignment:** Address the likely search intent behind the relevant keywords
                            2. **Product/Tool Sections:** Explain core purpose, key features, and benefits specifically for the Target Market
                            3. **Keyword Integration:** Naturally incorporate Primary Keyword(s) throughout the article, especially in strategic positions
                            4. **External Linking:** Insert 5-10 contextual external links to authoritative sources from the Research Findings
                            5. **Unique Angle Development:** Create a compelling narrative that makes the article stand out from competitors
                            6. **Evidence-Based Writing:** Support claims with data, expert opinions, and real user experiences from the Research Findings
                            7. **Balanced Perspective:** Present multiple viewpoints where appropriate, especially for controversial topics
                            8. **Product/Tool Sections:** Explain core purpose, key features, and benefits specifically for the Target Market, be sure to include detailed information in every paragraph of the outline. 
                            9. **Paragraph Structure:** pay attention to dividing it into paragraphs with a clear structure, and avoid cramming 400-500 words into a single paragraph.


                                    ## Task:
                            Generate a comprehensive, professional, and uniquely insightful SEO article that leverages the Research Findings to create content with superior E-E-A-T value. The article must be a definitive resource on the topic for the target audience.

                                    ## Output Format:
                            For the FAQs section, the answer generated for each question should not exceed 120 words.
                            For the Conclusion section, the answer generated for each question should not exceed 200 words.
                            Provide the final article content as well-formatted text in Markdown format.

                            """)
        ]
        article = ""
        #修改数据库中的loading_text，显示正在生成文章草稿
        workflow.loading_text = "正在生成文章草稿..."
        db.session.commit()
        for token in llm_generate.stream(messages):
            print(token.content, end="")
            article += token.content
        
        #提取markdown内容
        llm_extract = ChatOpenAI(
            model="gemini-2.5-flash-preview-05-20", 
            api_key=os.getenv("GROK_API_KEY"),
            base_url=os.getenv("BLT_BASE_URL"),
            reasoning_effort="none"
            )
        prompt_extract = f'''
                        The following is the content of the article. Please delete the parts that are not markdown section, only keep the markdown section and output it (remember not to make any changes to the retained content, keep the original text):
                        ***article: {article}
                        Remember: When outputting, do not use any other words except for the markdown section.
                        '''
        article_content = ""
        for token in llm_extract.stream(prompt_extract):
            print(token.content, end="")
            article_content += token.content
            print(f'aritcle原文：{article}')
            print(f'article提取：{article_content}')
    except Exception as e:
        error_message = f"节点执行失败 - 用户:{email}, 工作流id:{session_id}, 错误阶段：在节点4中生成文章草稿阶段发生错误，错误详情：{e}"
        logging.error(error_message)
        return {'status': 'failed', 'message': error_message}

    #--------------------------------optimize article--------------------------------
    try:
        #获取当前日期
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        #1. tavily搜索工具
        #1.1 初始化搜索工具
        search_tool_2 = TavilySearch(
            max_results=10, 
            include_generated_answer=False,
            include_raw_content=False,
            include_images=False,
        )
        search_query_2 = f"{keyword} latest trends research"
        #1.2 调用搜索工具
        search_response_2 = search_tool_2.invoke({"query": search_query_2})
        #1.3 提取搜素结果（只保留results）
        if isinstance(search_response_2, dict): #当搜索结果为空时，tavily会返回字符串
            search_results_2 = search_response_2['results']
            print(f"search_results_2: {search_results_2}")
        else:
            search_results_2 = ""
        #1.4 提取搜索标题成数组，以及url成数组
        urls_to_extract_2 = []
        for result in search_results_2:
            urls_to_extract_2.append(result['url'])
        #2. 使用tavily提取工具
        #2.1 初始化解析工具
        extract_tool_2 = TavilyExtract(
            extract_depth="advanced",
            include_images=False,
        )
        #2.2 调用解析工具
        if not search_results_2 == "":
            extraction_results_2 = extract_tool_2.invoke({"urls": urls_to_extract_2})
            #2.3 提取页面内容为数组
            extracted_contents_2 = []
            for result in extraction_results_2["results"]:
                extracted_contents_2.append(f"--- Content from {result.get('url', 'Unknown URL')} ---\n{result['raw_content'][:6000]}...")
            #2.4 合并提取内容为新变量
            extracted_text_2 = "\n\n".join(extracted_contents_2)
        #3. 调用大模型
        llm_optimize = ChatOpenAI(model=model, api_key=api_key, base_url=base_url)
        messages = [
            SystemMessage("You are an AI product expert, Senior SEO writer, Google SEO expert, an enthusiastic member of the AI product community. You are very good at writing professional, in-depth, and uniquely insightful SEO articles, also deeply expertise in Google's E-E-A-T principles and modern content optimization."),
            HumanMessage(f""""
                        **# Core Demand**
                            1.This is a direct task, not a request for advice
                            2.You must only polish the input article and are strictly prohibited from making extensive modifications to the original text.
                            3.You must not change the outline of the input article
                            4.If the article mentions a product, be sure to include detailed information in every paragraph of the outline. At the same time, pay attention to dividing it into paragraphs with a clear structure, and avoid cramming 400-500 words into a single paragraph.
                            5.When you output content in languages other than English, ensure that the article is not a rigid translation from English into {article_language}. Instead, optimize the content for localization based on {article_language}, and strive to write in a style that closely mimics that of experienced SEO content writers from the respective country.
                            6.If your article references content from other pages and you know the URL of the source, be sure to add the source URL to the anchor text of the relevant content.
                            7.Strictly follow the Heading Separation Rules and Content Block Separation Rules:
                                7.1 **Heading Separation Rules:**
                                - Insert exactly ONE blank line before every heading (H1-H6)
                                - Insert exactly ONE blank line after every heading (H1-H6)
                                - This applies to ALL heading level transitions (H1→H2, H2→H3, H3→H2, etc.)

                                7.2 **Content Block Separation:**
                                - ONE blank line between headings and any following content
                                - ONE blank line between separate paragraphs
                                - ONE blank line before and after: lists, code blocks, tables, blockquotes, horizontal rules

                                7.3 **Strict Compliance:**
                                - NO exceptions to these rules
                                - Every heading must be isolated by blank lines
                                - Every content block must be properly separated
                                - Failure to follow these rules is unacceptable

                                7.4 **Validation Requirement:**
                                - Your output must pass standard markdown parsers
                                - All formatting must render correctly in markdown viewer

                            **# TASK**
                            Your task is to optimize the input article draft based on the EEAT algorithm. The goal is to supplement it with more recent arguments, user reviews, and reference materials, while also improving the keyword density of the article. 
                            Ensure the overall readability of the text remains smooth and naturally integrate the LSI (Latent Semantic Indexing) keywords related to {keyword} throughout the article. Additionally, avoid using fancy vocabulary; instead, strive to use simple words to make the article appear more human-written. 
                            Your primary task is to optimize the FAQs at the bottom of the article, and your secondary task is to supplement the entire text with arguments, data, user reviews, and expert evaluations.

                            ## ARTICLE TO OPTIMIZE:
                            {article_content}

                            ## KEY INFORMATION:
                            - Primary Keyword: {keyword}
                            - Secondary Keywords: {secondary_keywords}
                            - Current Date: {current_date}
                            - Additional Knowledge: {additional_knowledge_points}
                            - Article language `[{article_language}]`

                            ## LATEST WEB RESEARCH (from Tavily's real-time search):
                            ```
                            {extracted_text_2}
                            ```
                            **# OUTPUT REQUIREMENTS**
                            - **## Word Count Requirements
                            - The article should contain between 2,500 and 5,000 words
                            - The exact length should be determined by the depth and breadth of the topic
                            - Adjust word count based on the complexity of the subject matter
                            - For the FAQs section, the answer generated for each question should not exceed 120 words
                            - For the Conclusion section, the answer generated for each question should not exceed 200 words

                            ## Content Depth vs. Word Count Relationship
                            - More complex topics requiring detailed explanations warrant longer articles
                            - Consider how many items, products, or points need to be covered
                            - Allow sufficient space to properly explain each section without fluff

                            ## Examples for Proper Scaling
                            - A list article reviewing 5 products in detail (overview, pros, cons, user reviews) will naturally be shorter than one covering 10 products
                            - A beginner's guide may require more explanatory content than an expert-focused piece
                            - Technical topics may require more space for proper explanation of concepts

                            ## Quality Priority Principle
                            - Always prioritize the quality and value of the content over strict word count
                            - Do not pad the article with unnecessary content just to reach a target word count
                            - Do not cut important information just to stay under a maximum word count
                            - Focus on comprehensive coverage that fully addresses the reader's search intent

                            ## SEO Best Practices
                            - Ensure all key information is included regardless of length constraints
                            - Maintain proper depth for each section to provide genuine value to readers
                            - Quality content that thoroughly addresses the topic will perform better in search rankings than articles written solely to hit word count targets

                            - Audience: High school graduate level (simple language, explained terms)
                            - Tone: Professional with natural humor
                            - Voice: First-person narration
                            - Format: Ready-to-publish with proper markdown formatting
                            - Use appropriate emojis to enhance key points (✅, 🔑, 📊, 💡, etc.)
                            - Format tables properly with markdown table syntax
                            - Include properly formatted lists (ordered and unordered)

                            **# OPTIMIZATION STRATEGY**

                            **1. E-E-A-T Enhancement (Focus on Experience & Authority)**

                            * **Experience Enhancement:**
                            * Replace generic claims with specific scenarios you've personally encountered
                            * Include detailed problem-solution stories with concrete outcomes
                            * Share genuine insights that demonstrate hands-on knowledge
                            * Add "lessons learned" elements that feel authentic and valuable

                            * **Authority Building:**
                            * Develop comprehensive coverage of all relevant subtopics
                            * Incorporate balanced analysis of different perspectives
                            * Reference industry standards and consensus viewpoints
                            * Ensure content answers the most common user questions thoroughly

                            * **Supporting Elements:**
                            * Verify technical accuracy of all claims and explanations
                            * Simplify complex concepts without losing meaning
                            * Include relevant data points and citations from authoritative sources
                            * Ensure headings accurately reflect section content without exaggeration

                            **2. Human Writing Style**

                            * Vary sentence structure and length naturally (mix short and long)
                            * Include occasional rhetorical questions and conversational transitions
                            * Use natural language patterns with occasional imperfections
                            * Add personal touches, analogies, and relatable examples
                            * Include occasional humor that feels spontaneous rather than forced
                            * Format quoted content with proper attribution using blockquotes

                            **3. SEO Implementation**

                            * Integrate primary keyword naturally within the text, especially in strategic locations
                            * Distribute LSI keywords (related semantic keywords) throughout the content
                            * Example: For "tablet" as primary keyword, include model-specific terms like "Lenovo Y700" or "Lenovo P12" naturally within relevant sections
                            * Focus on satisfying user search intent comprehensively
                            * Prioritize reader value over keyword density
                            * Organize information logically with proper headings and subheadings

                            **4. Content Quality**

                            * Eliminate redundancy and filler content
                            * Ensure information is current and accurate
                            * Present complex information in easily digestible formats
                            * Distribute content across paragraphs for improved readability
                            * Include unique insights that differentiate from generic content

                            ## Word Count Requirements
                            - The article should contain between 2,500 and 5,000 words
                            - The exact length should be determined by the depth and breadth of the topic
                            - Adjust word count based on the complexity of the subject matter

                            ## Content Depth vs. Word Count Relationship
                            - More complex topics requiring detailed explanations warrant longer articles
                            - Consider how many items, products, or points need to be covered
                            - Allow sufficient space to properly explain each section without fluff

                            ## Examples for Proper Scaling
                            - A list article reviewing 5 products in detail (overview, pros, cons, user reviews) will naturally be shorter than one covering 10 products
                            - A beginner's guide may require more explanatory content than an expert-focused piece
                            - Technical topics may require more space for proper explanation of concepts

                            ## Quality Priority Principle
                            - Always prioritize the quality and value of the content over strict word count
                            - Do not pad the article with unnecessary content just to reach a target word count
                            - Do not cut important information just to stay under a maximum word count
                            - Focus on comprehensive coverage that fully addresses the reader's search intent

                            ## SEO Best Practices
                            - Ensure all key information is included regardless of length constraints
                            - Maintain proper depth for each section to provide genuine value to readers
                            - Quality content that thoroughly addresses the topic will perform better in search rankings than articles written solely to hit word count targets

                            **# FINAL DELIVERY**
                            Provide a complete, ready-to-publish article that seamlessly incorporates all optimization elements while maintaining the original structure. The final output should be pure article content with no editorial marks, comments, or metadata.
                            """)
        ]
        optimized_article_content = ""
        #修改数据库中的loading_text，显示正在优化文章
        workflow.loading_text = "正在优化文章..."
        db.session.commit()
        for token in llm_optimize.stream(messages):
            print(token.content, end="")
            optimized_article_content += token.content
        
        #提取markdown内容
        model_extract = ChatOpenAI(
            model="gemini-2.5-flash-preview-05-20", 
            api_key=os.getenv("GROK_API_KEY"),
            base_url=os.getenv("BLT_BASE_URL"),
            reasoning_effort="none"
            )
        prompt_extract = f'''
                        The following is the content of the article. Please delete the parts that are not markdown section, only keep the markdown section and output it (remember not to make any changes to the retained content, keep the original text):
                        ***article: {optimized_article_content}
                        Remember: When outputting, do not use any other words except for the markdown section.
                        '''
        optimized_article_content_markdown = ""
        for token in model_extract.stream(prompt_extract):
            print(token.content, end="")
            optimized_article_content_markdown += token.content
    except Exception as e:
        error_message = f"节点执行失败 - 用户:{email}, 工作流id:{session_id}, 错误阶段：在节点4中优化文章阶段发生错误，错误详情：{e}"
        logging.error(error_message)
        return {'status': 'failed', 'message': error_message}

    #--------------------------------generate image--------------------------------
    try:
        gen_optimized_article_content = optimized_article_content_markdown

        if main_image_option:
            main_image_option = 'true'
        else:
            main_image_option = 'false'

        if sub_images_option:
            sub_images_option = 'true'
        else:
            sub_images_option = 'false'
        
        #如果没有生图要求则直接返回，不要浪费token
        if not main_image_option and not sub_images_option:
            return {'gen_article_content':article_content,'gen_optimized_article_content':optimized_article_content_markdown,'gen_final_article_content':optimized_article_content_markdown,'gen_final_article_html':md_to_HTML(optimized_article_content_markdown),'final_article_content':optimized_article_content_markdown,'final_article_html':md_to_HTML(optimized_article_content_markdown)}
        
        #1. 通过llm生成图片插入锚点和文生图prompt
        model = ChatOpenAI(model=model, api_key=api_key, base_url=base_url)
        prompt = f'''
    ## ROLE
    You are an expert Visual Content Strategist and a world-class Prompt Engineer for AI text-to-image models. **You are responsible for creating prompts that are not only creative and relevant but also guaranteed to be safe and pass automated content safety filters.**

    ## TASK
    Your task is to analyze the provided Markdown article and devise a visual strategy based on the user-defined options below. You will generate prompts for a main cover image and/or supporting inline images, but only if the corresponding option is set to `true`.

    ## OPTIONS
    * Generate Main Image: `[{main_image_option}]`
    * Generate Sub-Images: `[{sub_images_option}]`

    ## WORKFLOW & RULES
    1.  **SAFETY-FIRST PROMPT CREATION**: **This is the most important rule.** All generated `image_prompt`s must be **family-safe and suitable for a general audience.**
        * **Strictly avoid** any words, concepts, or descriptions related to violence, conflict, harm, adult themes, hate speech, or other politically and socially sensitive topics.
        * **CRITICAL**: Avoid ambiguous words or metaphors that could be misinterpreted by a safety system. **Favor direct, descriptive, and neutral language.** For example, instead of "a killer new product," use "an amazing new product." Instead of "launching an attack on the market," use "launching a new marketing campaign."
        * **Self-Correction Step**: After generating a prompt, mentally review it. If there is any chance it could be flagged by a safety system, you MUST rephrase it to be more benign and explicit.

    2.  **Full Article Analysis**: Thoroughly read and understand the entire article provided below the `---` separator to grasp its core message, tone, and key sections.

    3.  **Main Cover Image (Conditional)**:
        * **If the "Generate Main Image" option above is `true`**, create one **safe-to-generate** prompt for the main "cover image".
        * This image is intended to be placed directly below the article's main H1 title.
        * The prompt must synthesize the central theme of the entire article into a single, captivating, and high-level visual concept.

    4.  **Supporting Inline Images (Conditional)**:
        * **If the "Generate Sub-Images" option above is `true`**, identify the **two (2)** most suitable H2 headings (e.g., `## A Specific Topic`) in the article to place an illustrative image directly beneath.
        * For **each** of the two chosen H2 headings, create a specific, **safe-to-generate** `image_prompt` that visually represents the key information discussed within that particular section.
        * The prompt should be in English and include style details.

    5.  **CRITICAL ASPECT RATIO RULE**: **It is a strict and mandatory requirement that every `image_prompt` you generate MUST end with the exact text `--ar 16:9`. This is to ensure a horizontal display. There are no exceptions to this rule.**

    6.  **Format the Output**: Compile all your results into a single, valid JSON object, strictly following the output structure defined by the options.

    ## OUTPUT CONSTRAINTS
    * Your **entire response** must be a single, valid JSON object and nothing else. Do not include any explanations, comments, or text outside of the JSON object.
    * The structure of the final JSON object is conditional:
        * **Only include the `main_image` key** if the "Generate Main Image" option is `true`.
        * **Only include the `sub_images` key** if the "Generate Sub-Images" option is `true`.
        * If both options are `false`, return an empty JSON object `{{}}`.
    * **Do NOT use `--ar 9:16` or any other aspect ratio.** The only allowed aspect ratio string is `--ar 16:9`.

    ## EXAMPLE OUTPUT FORMATS

    ### Example 1: If both options are `true`
    ```json
    {{
    "main_image": {{
        "image_prompt": "A futuristic and optimistic city skyline at dusk, with glowing lines representing data flows between smart buildings, autonomous vehicles on the streets below, and drone-like air taxis in the sky. The style is sleek, modern, and slightly stylized. --ar 16:9"
    }},
    "sub_images": [
        {{
        "insert_after_h2_heading": "## The Rise of Electric Scooters",
        "image_prompt": "A photorealistic action shot of a diverse group of young professionals cheerfully riding electric scooters on a dedicated bike lane in a sunny, green urban park. The focus is on convenience and eco-friendly transport. --ar 16:9"
        }},
        {{
        "insert_after_h2_heading": "## Autonomous Flying Taxis: The Future?",
        "image_prompt": "A conceptual, high-tech image of a sleek, autonomous flying taxi pod smoothly landing on a skyscraper's rooftop helipad. The background shows a sprawling cityscape. The style is clean, minimalist, and forward-looking. --ar 16:9"
        }}
    ]
    }}
    ```

    ### Example 2: If only "Generate Main Image" is `true`
    ```json
    {{
    "main_image": {{
        "image_prompt": "A futuristic and optimistic city skyline at dusk, with glowing lines representing data flows between smart buildings, autonomous vehicles on the streets below, and drone-like air taxis in the sky. The style is sleek, modern, and slightly stylized. --ar 16:9"
    }}
    }}
    ```

    ### Example 3: If only "Generate Sub-Images" is `true`
    ```json
    {{
    "sub_images": [
        {{
        "insert_after_h2_heading": "## The Rise of Electric Scooters",
        "image_prompt": "A photorealistic action shot of a diverse group of young professionals cheerfully riding electric scooters on a dedicated bike lane in a sunny, green urban park. The focus is on convenience and eco-friendly transport. --ar 16:9"
        }},
        {{
        "insert_after_h2_heading": "## Autonomous Flying Taxis: The Future?",
        "image_prompt": "A conceptual, high-tech image of a sleek, autonomous flying taxi pod smoothly landing on a skyscraper's rooftop helipad. The background shows a sprawling cityscape. The style is clean, minimalist, and forward-looking. --ar 16:9"
        }}
    ]
    }}
    ```

    ### Example 4: If both options are `false`
    ```json
    {{}}
    ```

    ---
    ## ARTICLE CONTENT
    {gen_optimized_article_content}
    ```
    '''
        json_result = ""
        #修改数据库中的loading_text，显示正在生成图片
        workflow.loading_text = "正在寻找最佳的图片生成方案..."
        db.session.commit()
        for token in model.stream(prompt):
            print(token.content, end="")
            json_result += token.content

        #2. 清洗json字符串
        json_str = extract_json_from_llm_output(json_result)

        #3. json字符串 -> dict类型 转换
        json_dict = llm_to_dict(json_str)

        #4. dict -> 任务列表
        task = gen_task(json_dict)

        #5. 任务列表 -> urls_map （调用image1文生图模型，耗时大概3mins）
        #修改数据库中的loading_text，显示正在生成图片
        workflow.loading_text = "正在生成图片..."
        db.session.commit()
        urls_map = gen_task_with_urls(task)

        #6. md文档，urls_map -> 带urls的md文档
        final_md_content = assemble_markdown(gen_optimized_article_content,urls_map)

        #7. md文档 -> HTML
        final_HTML = md_to_HTML(final_md_content)

        #修改loading_text，显示正在生成文章摘要
        workflow.loading_text = "正在生成文章摘要..."
        db.session.commit()
        #8. 生成文章摘要
        article_summary = generate_article_summary(final_md_content)

        return {
            'gen_article_content':article_content,
            'gen_optimized_article_content':optimized_article_content_markdown,
            'gen_final_article_content':final_md_content,
            'gen_final_article_html':final_HTML,
            'final_article_content':final_md_content,
            'final_article_html':final_HTML,
            'article_description':article_summary
        }
    except Exception as e:
        error_message = f"节点执行失败 - 用户:{email}, 工作流id:{session_id}, 错误阶段：在节点4中生成图片阶段发生错误，错误详情：{e}"
        logging.error(error_message)
        return {'status': 'failed', 'message': error_message}