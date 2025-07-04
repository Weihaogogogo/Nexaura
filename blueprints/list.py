from flask import Blueprint, jsonify, g
from utils.jwt_utils import jwt_required
from models.WorkflowsModel import WorkflowsModel

bp = Blueprint('list', __name__, url_prefix='/')

@bp.route('/workflows/list', methods=['GET'])
@jwt_required  # 使用JWT认证
def workflows_list():
    email = g.current_user_email  # 从JWT获取用户邮箱
    
    # 查询该用户的所有工作流记录，按创建时间倒序排列
    workflows = WorkflowsModel.query.filter_by(email=email).order_by(WorkflowsModel.created_time.desc()).all()
    
    # 按status分类
    completed_workflows = []
    in_progress_workflows = []
    failed_workflows = []
    
    # 构建返回数据
    for workflow in workflows:
        workflow_info = {
            'session_id': workflow.session_id,
            'keyword': workflow.keyword,
            'target_market': workflow.target_market,
            'article_language': workflow.article_language,
            'current_node_index': workflow.current_node_index,
            'status': workflow.status,
            'created_time': workflow.created_time.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_time': workflow.updated_time.strftime('%Y-%m-%d %H:%M:%S') if workflow.updated_time else None
        }
        
        # 根据status分类
        if workflow.status == 'completed':
            completed_workflows.append(workflow_info)
        elif workflow.status == 'in_progress':
            in_progress_workflows.append(workflow_info)
        elif workflow.status == 'failed':
            failed_workflows.append(workflow_info)
    
    return jsonify({
        'code': 200,
        'message': '获取工作流列表成功',
        'data': {
            'total': len(workflows),
            'completed': completed_workflows,
            'in_progress': in_progress_workflows,
            'failed': failed_workflows
        }
    })
    