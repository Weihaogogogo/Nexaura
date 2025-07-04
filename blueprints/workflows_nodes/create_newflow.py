#创建工作流实例模块
from flask import jsonify
from models.UserModel import UserModel
from models.WorkflowsModel import WorkflowsModel
from exts import db
import logging

def create_newflow(params):
    try:
        email = params.get('email')
        node_input = params.get('node_input')
        new_workflow = params.get('new_workflow')

        if new_workflow:
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                return jsonify({'code':400, 'message':'该用户未注册，请检查email是否正确'}),400
            if user.available_uses < 1:
                return jsonify({'code':400, 'message':'该用户额度不足'}),400
            user.available_uses -= 1
            db.session.commit()
            current_workflow = WorkflowsModel(email=email, current_node_index=0, status='completed', keyword=node_input.get('keyword'), target_market=node_input.get('target_market'), article_language=node_input.get('article_language'))
            db.session.add(current_workflow)
            db.session.commit()
            session_id = current_workflow.session_id
            return session_id
    except Exception as e:
        error_message = f"create_newflow为用户创建新的工作流执行时发生错误 - 用户:{email}, 工作流id:{session_id if 'session_id' in locals() else '未知'}, 错误详情：{e}"
        logging.error(error_message)
        return {'status': 'failed', 'message': error_message}