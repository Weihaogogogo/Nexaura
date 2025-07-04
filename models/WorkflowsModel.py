from exts import db
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGTEXT

class WorkflowsModel(db.Model):
    __tablename__ = 'workflows'
    session_id = db.Column(db.Integer, primary_key=True, autoincrement=True) #每个工作流的唯一ID
    email = db.Column(db.String(50), nullable=False) #用户账号，外键，与UserModel关联
    current_node_index = db.Column(db.Integer, nullable=False, default=1) #当前工作流的节点序号，例如1代表第一个节点，2代表第二个节点
    status = db.Column(db.Enum('in_progress', 'completed', 'failed'), default='in_progress', nullable=False) #当前工作流在当前节点的状态
    failed_message = db.Column(LONGTEXT) #方便在异步进程中记录用户失败的原因
    created_time = db.Column(db.DateTime, default=datetime.now, nullable=False) #实例化一条数据时就记录当时的时间，后面更新数据时不更新这个字段
    updated_time = db.Column(db.DateTime, default=datetime.now, nullable=False) #实例化一条数据时就记录当时的时间，后面每次更新都需要更新这个字段
    keyword = db.Column(db.String(50),nullable=False) #关键词
    target_market = db.Column(db.String(50),nullable=False) #目标市场，例如us
    article_language = db.Column(db.String(50),nullable=False) #文章语言，例如English
    gen_search_intent = db.Column(db.JSON) #后端生成的搜索意图，是一个数组
    search_intent = db.Column(LONGTEXT) #用户选择/输入的搜索意图，是一个字符串
    gen_topic_ideas = db.Column(db.JSON) #后端生成的主题创意，是一个数组
    chosen_topic = db.Column(db.String(500)) #用户选择/输入的主题创意
    gen_research_data = db.Column(LONGTEXT) #后端生成功能的深度研究报告
    background_information = db.Column(LONGTEXT) #背景信息
    title_generation_demands = db.Column(LONGTEXT) #标题生成要求
    gen_article_titles = db.Column(db.JSON) #后端生成的文章标题列表，是一个数组
    article_title = db.Column(db.String(100)) #用户选择/输入的文章标题
    additional_knowledge_points = db.Column(LONGTEXT) #用户上传的附加知识点
    outline_demand = db.Column(LONGTEXT) #大纲要求
    gen_article_outline = db.Column(LONGTEXT) #后端生成的文章大纲
    article_outline = db.Column(LONGTEXT) #经过用户优化后的文章大纲
    narrative_perspective = db.Column(db.String(100)) #视角选择，1代表第一人称视角；2代表第二人称视角
    gen_article_content = db.Column(LONGTEXT) #后端生成的文章内容草稿
    article_content = db.Column(LONGTEXT) #文章内容草稿
    secondary_keywords = db.Column(db.String(100)) #第二关键词
    gen_optimized_article_content = db.Column(LONGTEXT) #后端生成的优化后的文章内容
    gen_final_article_content = db.Column(LONGTEXT) #生成的最终的MD格式的文章结果（含图片标签）
    seo_title = db.Column(LONGTEXT) #seo标题，70字符内，如果article_title符合就等于article_title，否则大模型重新输出一个
    article_description = db.Column(LONGTEXT) #seo描述，是对文章的总结，用于在卡片列表中展示（或者也可以在页面中呈现，让用户快速了解文章写了什么）
    url_example = db.Column(LONGTEXT) #url示例，是seo标题转小写并用“-”拼接
    main_image_option = db.Column(db.Boolean, default=False) #是否生成博客封面图
    sub_images_option = db.Column(db.Boolean, default=False) #是否生成文章内H2标题图片
    gen_final_article_html = db.Column(LONGTEXT) #生成的最终的HTML格式的文章结果（含图片标签）
    loading_text = db.Column(LONGTEXT) #加载文本，用于在异步进程中记录用户加载的进度,方便在前端展示
    final_article_content = db.Column(LONGTEXT) #最终的文章结果（含图片标签）
    final_article_html = db.Column(LONGTEXT) #最终的HTML格式的文章结果（含图片标签）
    #添加与用户表的关联
    user = db.relationship('UserModel', backref='workflows', 
                         foreign_keys=[email], 
                         primaryjoin='WorkflowsModel.email == UserModel.email')