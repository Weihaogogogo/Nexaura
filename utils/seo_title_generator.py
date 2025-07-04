import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def optimize_seo_title(article_title, api_key=os.getenv("GROK_API_KEY"), base_url=os.getenv("BLT_BASE_URL")):
    """
    优化文章标题为SEO友好的标题
    
    Args:
        article_title (str): 原始文章标题
        api_key (str): API密钥
        base_url (str): API基础URL
    
    Returns:
        str: 优化后的SEO友好标题（70字符以内）
    """
    
    # 输入验证
    if not article_title or not article_title.strip():
        return "无效标题"
    
    article_title = article_title.strip()
    
    # 如果标题长度不超过70个字符，直接返回
    if len(article_title) <= 70:
        return article_title
    
    # 如果超过70个字符，使用LLM优化
    try:
        model = ChatOpenAI(
            model="gemini-2.5-flash-preview-05-20", 
            api_key=api_key,
            base_url=base_url,
            request_timeout=60,
            max_retries=3
        )
        
        prompt = f"""
# Role: You are an expert SEO copywriter and digital marketing specialist with 10+ years of experience in creating high-converting, search-engine-optimized titles.

# Task: Transform the given article title into an SEO-friendly version that is compelling, keyword-rich, and optimized for search engines while staying within strict character limits.

# Critical Requirements:
1. **CHARACTER LIMIT**: Output must be EXACTLY 70 characters or fewer (including spaces and punctuation)
2. **SEO OPTIMIZATION**: Include relevant keywords that users would search for
3. **COMPELLING**: Make it click-worthy and engaging
4. **CLEAR**: Maintain the core meaning and value proposition
5. **ACTION-ORIENTED**: Use power words when appropriate
6. **NO FLUFF**: Remove unnecessary words, articles, and filler content

# SEO Best Practices to Follow:
- Place primary keywords at the beginning when possible
- Use numbers, years, or specific data points
- Include power words (Ultimate, Complete, Essential, Proven, etc.)
- Avoid keyword stuffing
- Make it scannable and easy to read
- Focus on user intent and search behavior

# Few-Shot Examples:

## Example 1:
**Input**: "The Complete Comprehensive Guide to Understanding and Implementing Advanced Search Engine Optimization Strategies for Small Business Owners in 2025"
**Character Count**: 147 characters
**Output**: "Complete SEO Guide for Small Business Owners 2025"
**Character Count**: 50 characters
**Reasoning**: Kept core keywords (SEO, Small Business, 2025), removed redundant words, maintained value proposition

## Example 2:
**Input**: "How to Choose the Perfect Smartphone: A Detailed Comparison Between iPhone and Android Devices with Pros and Cons Analysis"
**Character Count**: 127 characters
**Output**: "iPhone vs Android 2025: Complete Smartphone Buying Guide"
**Character Count**: 56 characters
**Reasoning**: Added year for relevance, kept comparison aspect, made it more searchable

## Example 3:
**Input**: "Top 10 Most Effective Digital Marketing Strategies That Every Modern Business Should Know and Implement Right Now"
**Character Count**: 118 characters
**Output**: "10 Essential Digital Marketing Strategies for Modern Business"
**Character Count**: 59 characters
**Reasoning**: Kept number, power word "Essential", removed time pressure, focused on core value

## Example 4:
**Input**: "The Ultimate Step-by-Step Beginner's Guide to Learning Python Programming Language from Scratch in 2025"
**Character Count**: 108 characters
**Output**: "Python Programming Guide 2025: Beginner to Expert"
**Character Count**: 48 characters
**Reasoning**: Simplified structure, kept year, implied progression, highly searchable

## Example 5:
**Input**: "Best Practices for Creating High-Converting Landing Pages That Generate More Leads and Increase Sales Revenue"
**Character Count**: 114 characters
**Output**: "High-Converting Landing Pages: Best Practices for More Leads"
**Character Count**: 61 characters
**Reasoning**: Kept main benefit, action-oriented, focused on outcome

# Your Task:
Original Title: "{article_title}"
Character Count: {len(article_title)} characters

Please provide:
1. **Optimized Title**: [Your optimized title here]
2. **Character Count**: [Exact count]
3. **Key Changes**: [Brief explanation of main optimizations made]

**CRITICAL**: Your optimized title MUST be 70 characters or fewer. Count carefully!

Optimized Title:
"""
        
        response = model.invoke(prompt)
        result = response.content.strip()
        
        # 解析响应，提取优化后的标题
        optimized_title = extract_optimized_title(result, article_title)
        
        # 验证字符长度
        if len(optimized_title) > 70:
            # 如果仍然超长，使用备用方案
            return generate_fallback_title(article_title)
        
        return optimized_title
        
    except Exception as e:
        print(f"Error optimizing title with AI: {str(e)}")
        return generate_fallback_title(article_title)

def extract_optimized_title(ai_response, original_title):
    """
    从AI响应中提取优化后的标题
    
    Args:
        ai_response (str): AI的完整响应
        original_title (str): 原始标题（备用）
    
    Returns:
        str: 提取的优化标题
    """
    try:
        lines = ai_response.split('\n')
        
        # 查找包含"Optimized Title"的行
        for line in lines:
            if 'optimized title' in line.lower() or 'title:' in line.lower():
                # 提取冒号后的内容
                if ':' in line:
                    title = line.split(':', 1)[1].strip()
                    # 清理可能的格式标记
                    title = title.replace('**', '').replace('*', '').replace('"', '').replace("'", "")
                    if title and len(title) <= 70:
                        return title
        
        # 如果没找到标准格式，尝试提取第一行非空内容
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('**'):
                title = line.replace('**', '').replace('*', '').replace('"', '').replace("'", "")
                if len(title) <= 70:
                    return title
        
        # 如果都失败了，返回备用方案
        return generate_fallback_title(original_title)
        
    except Exception:
        return generate_fallback_title(original_title)

def generate_fallback_title(original_title):
    """
    备用标题生成方案（基于规则的简化）
    
    Args:
        original_title (str): 原始标题
    
    Returns:
        str: 简化后的标题（70字符以内）
    """
    try:
        # 移除常见的冗余词汇
        stop_words = [
            'the complete', 'comprehensive', 'ultimate', 'detailed', 'step-by-step',
            'beginner\'s', 'advanced', 'professional', 'expert', 'complete guide to',
            'how to', 'ways to', 'methods for', 'strategies for', 'tips for',
            'that you need to know', 'you should know', 'everyone should',
            'in this article', 'this guide', 'right now', 'today'
        ]
        
        title = original_title.lower()
        
        # 移除停用词
        for stop_word in stop_words:
            title = title.replace(stop_word, '')
        
        # 清理多余空格
        title = ' '.join(title.split())
        
        # 首字母大写
        title = title.title()
        
        # 如果仍然太长，截取前67个字符并添加省略号
        if len(title) > 70:
            title = title[:67] + '...'
        
        return title if title else original_title[:70]
        
    except Exception:
        # 最后的备用方案：直接截取
        return original_title[:70]

def batch_optimize_titles(titles_list, api_key=os.getenv("GROK_API_KEY"), base_url=os.getenv("BLT_BASE_URL")):
    """
    批量优化标题
    
    Args:
        titles_list (list): 标题列表
        api_key (str): API密钥
        base_url (str): API基础URL
    
    Returns:
        list: 优化后的标题列表
    """
    optimized_titles = []
    for i, title in enumerate(titles_list):
        print(f"正在优化第 {i+1}/{len(titles_list)} 个标题...")
        optimized = optimize_seo_title(title, api_key, base_url)
        optimized_titles.append(optimized)
        print(f"原标题 ({len(title)}字符): {title}")
        print(f"优化后 ({len(optimized)}字符): {optimized}")
        print("-" * 50)
    
    return optimized_titles
