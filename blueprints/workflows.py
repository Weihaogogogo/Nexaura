#工作流核心模块（工作流步骤、执行逻辑）
from flask import Blueprint, request, jsonify, g
from exts import db
from models.WorkflowsModel import WorkflowsModel
from utils.jwt_utils import jwt_required
#参数完整性校验模块
from blueprints.workflows_nodes.form_validation import params_required
#创建工作流实例模块
from blueprints.workflows_nodes.create_newflow import create_newflow
#工作流任务执行模块
from blueprints.workflows_nodes.task_execution import workflow_task
from blueprints.workflows_nodes.gen_image_functions import md_to_HTML


bp = Blueprint('workflows', __name__,url_prefix='/workflows')

#用于前端轮询，获取工作流状态
@bp.route('/status/<session_id>',methods=['GET'])
@jwt_required  # 🔥 使用JWT认证
def get_workflow_status(session_id):
    email = g.current_user_email  # 🔥 从JWT获取，不是session
    # 同时验证session_id和email
    current_workflow = WorkflowsModel.query.filter_by(
        session_id=session_id,
        email=email
    ).first()

    if not current_workflow:
        return jsonify({'code': 404, 'message': '工作流不存在或无权访问'}), 404
    
    else: #current_workflow验证成功，可以获取status来返回
        
        if current_workflow.status == 'in_progress':
            return jsonify({'code':202,'message':'工作流正在进行中，请耐心等待...','data':{'current_node_index':current_workflow.current_node_index,'loading_text':current_workflow.loading_text,'status':current_workflow.status}}),202
        elif current_workflow.status == 'failed':
            failed_message = current_workflow.failed_message
            return jsonify({'code':400, 'message':failed_message})
        elif current_workflow.status == 'pending':
            return jsonify({'code':400, 'message':'工作流未启动，请检查celery是否故障'}),400
        else: # status == 'completed'
        #响应数据库workflows表中所有字段数据到前端(除了email外的所有字段的和值）
            response_data = {
                column.name: getattr(current_workflow, column.name)
                for column in current_workflow.__table__.columns
                if column.name != 'email'
            }
            # 格式化时间字段
            if response_data.get('created_time'):
                response_data['created_time'] = current_workflow.created_time.strftime('%Y-%m-%d %H:%M:%S')
            if response_data.get('updated_time'):
                response_data['updated_time'] = current_workflow.updated_time.strftime('%Y-%m-%d %H:%M:%S')
            return jsonify({'code':200, 'message':'节点调用成功', 'data':response_data}),200

#工作流结果获取模块
@bp.route('/result/<session_id>',methods=['GET'])
@jwt_required  # 🔥 使用JWT认证
def get_workflow_result(session_id):
    email = g.current_user_email  # 🔥 从JWT获取，不是session
    current_workflow = WorkflowsModel.query.filter_by(
        session_id=session_id,
        email=email
    ).first()

    if not current_workflow:
        return jsonify({'code': 404, 'message': '工作流不存在或无权访问'}), 404
    
    else:
        #响应数据库workflows表中所有字段数据到前端(除了email外的所有字段的和值）
        response_data = {
            column.name: getattr(current_workflow, column.name)
            for column in current_workflow.__table__.columns
            if column.name != 'email'
        }
        # 格式化时间字段
        if response_data.get('created_time'):
            response_data['created_time'] = current_workflow.created_time.strftime('%Y-%m-%d %H:%M:%S')
        if response_data.get('updated_time'):
            response_data['updated_time'] = current_workflow.updated_time.strftime('%Y-%m-%d %H:%M:%S')
        return jsonify({'code':200, 'message':'工作流结果获取成功', 'data':response_data}),200

#修改文章接口
@bp.route('/modify_article/<session_id>',methods=['POST'])
@jwt_required  # 🔥 使用JWT认证
def modify_article(session_id):
    email = g.current_user_email  # 🔥 从JWT获取，不是session
    current_workflow = WorkflowsModel.query.filter_by(
        session_id=session_id,
        email=email
    ).first()
    if not current_workflow:
        return jsonify({'code': 404, 'message': '工作流不存在或无权访问'}), 404
    
    else:
        #获取前端传入的修改后的文章
        modified_article = request.get_json().get('modified_article')
        #将修改后的文章更新到数据库中
        current_workflow.final_article_content = modified_article
        current_workflow.final_article_html = md_to_HTML(modified_article)
        db.session.commit()
        return jsonify({'code':200, 'message':'文章修改成功'}),200

#获取已完成文章列表接口
@bp.route('/completed_articles', methods=['GET'])
@jwt_required  # 🔥 使用JWT认证
def get_completed_articles():
    """
    获取当前用户所有已完成的文章（final_article_content不为null）
    支持分页和排序
    """
    email = g.current_user_email  # 🔥 从JWT获取用户邮箱
    
    # 获取查询参数
    page = request.args.get('page', 1, type=int)  # 页码，默认第1页
    per_page = request.args.get('per_page', 10, type=int)  # 每页数量，默认10条
    sort_by = request.args.get('sort_by', 'updated_time')  # 排序字段，默认按更新时间
    sort_order = request.args.get('sort_order', 'desc')  # 排序方式，默认降序
    
    # 验证每页数量范围
    if per_page > 50:
        per_page = 50
    
    try:
        # 查询条件：当前用户 + final_article_content不为null
        query = WorkflowsModel.query.filter_by(email=email).filter(
            WorkflowsModel.final_article_content.isnot(None),
            WorkflowsModel.final_article_content != ''
        )
        
        # 排序设置
        if hasattr(WorkflowsModel, sort_by):
            if sort_order.lower() == 'asc':
                query = query.order_by(getattr(WorkflowsModel, sort_by).asc())
            else:
                query = query.order_by(getattr(WorkflowsModel, sort_by).desc())
        else:
            # 默认排序
            query = query.order_by(WorkflowsModel.updated_time.desc())
        
        # 分页查询
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # 构建响应数据
        articles = []
        for workflow in pagination.items:
            # 只返回文章相关的关键信息，避免返回过多数据
            article_data = {
                'session_id': workflow.session_id,
                'article_title': workflow.article_title,
                'seo_title': workflow.seo_title,
                'article_description': workflow.article_description,
                'url_example': workflow.url_example,
                'keyword': workflow.keyword,
                'target_market': workflow.target_market,
                'article_language': workflow.article_language,
                'created_time': workflow.created_time.strftime('%Y-%m-%d %H:%M:%S') if workflow.created_time else None,
                'updated_time': workflow.updated_time.strftime('%Y-%m-%d %H:%M:%S') if workflow.updated_time else None,
                'status': workflow.status,
                'final_article_content': workflow.final_article_content,
                'final_article_html': workflow.final_article_html
            }
            articles.append(article_data)
        
        # 分页信息
        pagination_info = {
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page,
            'per_page': pagination.per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev,
            'next_page': pagination.next_num if pagination.has_next else None,
            'prev_page': pagination.prev_num if pagination.has_prev else None
        }
        
        return jsonify({
            'code': 200,
            'message': f'获取已完成文章成功，共{pagination.total}篇',
            'data': {
                'articles': articles,
                'pagination': pagination_info
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取已完成文章失败: {str(e)}'
        }), 500

#获取单篇已完成文章详情接口
@bp.route('/completed_articles/<int:session_id>', methods=['GET'])
@jwt_required  # 🔥 使用JWT认证
def get_completed_article_detail(session_id):
    """
    获取指定session_id的已完成文章详情
    """
    email = g.current_user_email  # 🔥 从JWT获取用户邮箱
    
    try:
        # 查询指定的工作流
        workflow = WorkflowsModel.query.filter_by(
            session_id=session_id,
            email=email
        ).filter(
            WorkflowsModel.final_article_content.isnot(None),
            WorkflowsModel.final_article_content != ''
        ).first()
        
        if not workflow:
            return jsonify({
                'code': 404,
                'message': '文章不存在或无权访问'
            }), 404
        
        # 返回完整的文章数据（除了email字段）
        article_data = {
            column.name: getattr(workflow, column.name)
            for column in workflow.__table__.columns
            if column.name != 'email'
        }
        
        # 格式化时间字段
        if article_data.get('created_time'):
            article_data['created_time'] = workflow.created_time.strftime('%Y-%m-%d %H:%M:%S')
        if article_data.get('updated_time'):
            article_data['updated_time'] = workflow.updated_time.strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'code': 200,
            'message': '获取文章详情成功',
            'data': article_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取文章详情失败: {str(e)}'
        }), 500

#工作流核心模块，用于调用工作流节点函数
@bp.route('/',methods=['POST'])
@jwt_required  # 🔥 使用JWT认证
def workflows():
    data = request.get_json()
    #1. 获取数据：
    ##从JWT中获取email
    email = g.current_user_email  # 🔥 从JWT获取，不是session
    ##获取session_id
    session_id = data.get('session_id',None)
    ##获取new_workflow字段
    new_workflow = data.get('new_workflow',None)
    ##获取用户输入的工作流数据：
    node_input = data.get('node_input',None)
    ##将数据打包成字典
    params = {
        'email':email,
        'session_id':session_id,
        'new_workflow':new_workflow,
        'node_input':node_input
    }

    #2. 使用params_required模块，判断必备参数完整性,如果参数不完整，则直接返回错误
    if type(params_required(params)) == jsonify:
        return params_required(params)
    else:
        #参数完整，可以继续执行
        pass

    #3. 判断是否第一次请求（会携带new_workflow字段）
    if new_workflow:
        #创建工作流实例，并返回session_id
        session_id = create_newflow(params)
        #如果创建工作流实例失败，则直接返回错误
        if isinstance(session_id, tuple):
            return session_id  # 直接返回tuple (response, status_code)
        elif isinstance(session_id, dict) and session_id.get('status') == 'failed':
            return jsonify({'code': 500, 'message': session_id.get('message', '创建工作流失败')}), 500
        else: #创建工作流实例成功，更新params中的session_id
            params['session_id'] = session_id
    else:
        #检查工作流是否已经在执行中，防止重复提交
        current_workflow = WorkflowsModel.query.filter_by(
            session_id=session_id,
            email=email
        ).first()
        
        if not current_workflow:
            return jsonify({'code': 404, 'message': '工作流不存在或无权访问'}), 404
            
        if current_workflow.status == 'in_progress':
            return jsonify({'code': 409, 'message': '工作流正在执行中，请勿重复提交'}), 409

    #4. 调用工作流任务执行模块(异步任务)
    try:
        output = workflow_task.delay(params)
        return jsonify({'code':202, 'message':'已开始调用工作流节点','data':{'session_id': session_id}}),202
    except Exception as e:
        return jsonify({'code': 500, 'message': f'任务提交失败: {str(e)}'}), 500
