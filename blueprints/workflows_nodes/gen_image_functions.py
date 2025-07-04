from openai import OpenAI
from langchain_openai import ChatOpenAI
import os
import re
import json
import requests
from dotenv import load_dotenv
load_dotenv()
from flask import jsonify

load_dotenv()

#清洗json字符串函数
def extract_json_from_llm_output(llm_text: str) -> str | None:
    """
    从LLM可能返回的、被Markdown代码块包裹的文本中提取纯JSON字符串。
    """
    # 1. 寻找被 ```json ... ``` 包裹的代码块
    # re.DOTALL 标志让 . 可以匹配包括换行在内的任意字符
    match = re.search(r"```json\s*(\{.*\})\s*```", llm_text, re.DOTALL)
    
    if match:
        # 如果找到，返回第一个捕获组的内容，即花括号内的所有内容
        return match.group(1)
    
    # 2. 如果没有找到Markdown块，作为备用方案，尝试直接寻找第一个 '{' 和最后一个 '}'
    #    这可以处理LLM有时只返回纯JSON，但前后可能带有一些解释性文字的情况
    start_brace = llm_text.find('{')
    end_brace = llm_text.rfind('}')
    
    if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
        return llm_text[start_brace:end_brace+1]
        
    # 如果两种方法都找不到，则返回None
    return None

#llm结果 to dict 函数
def llm_to_dict(str):
    import json
    #正则表达式清洗
    json_str = extract_json_from_llm_output(str)
    #格式转化为dict
    res = json.loads(json_str)
    return res

#dict to 任务列表 函数
def gen_task(obj):
    tasks_to_generate = []
    if obj.get('main_image'):
        tasks_to_generate.append({
            'type': 'main',
            'prompt': obj['main_image']['image_prompt']
        })

    if obj.get('sub_images'):
        for sub_image_info in obj['sub_images']:
            tasks_to_generate.append({
                'type': 'sub',
                'location': sub_image_info['insert_after_h2_heading'],
                'prompt': sub_image_info['image_prompt']
            })

    return tasks_to_generate

# image1模型函数，输入prompt，输出生成的图片的url
def gen_image(prompt, model="gpt-image-1",api_key=os.getenv("GROK_API_KEY"),base_url=os.getenv("BLT_BASE_URL")):
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    try:
        # 生成图像
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1536x1024"
        )

        # 获取图片 URL
        if result.data and len(result.data) > 0:
            image_url = result.data[0].url
            print(f"Image URL: {image_url}")
            return image_url
        else:
            print("No image data in response")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print(f"Error type: {type(e)}")
        return None

#任务列表 to urls_map 函数
def gen_task_with_urls(task):
    #并发调用
    from concurrent.futures import ThreadPoolExecutor

    #如果一个对象有prompt属性，在该函数输入对象，会给对象加url属性并返回整个对象
    def process_image_task(task):
        image_url = gen_image(task['prompt'])
        task['url'] = image_url
        return task

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(process_image_task, task))

    image_urls_map = {}
    for res in results:
        if res['type'] == 'main':
            image_urls_map['main_image'] = res['url']
        elif res['type'] == 'sub':
            image_urls_map.setdefault('sub_images', {})[res['location']] = res['url']
    return image_urls_map

#拼装md文档: md文档 to 带url的md文档 函数
def assemble_markdown(original_md, urls_map):
    md_lines = original_md.split('\n')
    final_md_content = original_md

    # 1. 插入主图 (如果存在)
    if 'main_image' in urls_map:
        main_image_url = urls_map['main_image']
        main_image_md = f"\n![封面图片]({main_image_url})\n"
        
        # 找到第一个H1标题的位置并插入图片
        h1_found = False
        for i, line in enumerate(md_lines):
            if line.strip().startswith('# '):
                # 在H1标题行的下一行插入
                md_lines.insert(i + 1, main_image_md)
                h1_found = True
                break
        if h1_found:
            final_md_content = "\n".join(md_lines)

    # 2. 插入副图 (如果存在)
    if 'sub_images' in urls_map:
        for heading, url in urls_map['sub_images'].items():
            # 使用字符串替换，在H2标题下方插入图片
            # heading 变量的值是 "## The Rise of Electric Scooters"
            insertion_text = f"\n![插图]({url})\n"
            final_md_content = final_md_content.replace(
                heading, 
                heading + insertion_text
            )
            
    return final_md_content

#md -> HTML 函数
def md_to_HTML(md):
    from markdown_it import MarkdownIt
    md_parser = MarkdownIt()
    final_html = md_parser.render(md)
    return final_html