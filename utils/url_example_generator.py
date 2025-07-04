import re
def format_title_to_slug(title):
    """
    将标题字符串转换为小写并用连字符连接
    
    Args:
        title (str): 原始标题字符串
    
    Returns:
        str: 格式化后的字符串（小写+连字符连接）
    """
    if not title:
        return ""
    
    # 转换为小写
    title = title.lower()
    
    # 移除特殊字符，只保留字母、数字和空格
    title = re.sub(r'[^\w\s-]', '', title)
    
    # 将多个空格替换为单个空格
    title = re.sub(r'\s+', ' ', title)
    
    # 去除首尾空格
    title = title.strip()
    
    # 用连字符替换空格
    title = title.replace(' ', '-')
    
    # 移除多余的连字符
    title = re.sub(r'-+', '-', title)
    
    # 去除首尾连字符
    title = title.strip('-')
    
    return title
