#celery 异步任务队列
from flask import jsonify
from models.WorkflowsModel import WorkflowsModel
from exts import db, celery
from datetime import datetime
import json
import logging
from blueprints.workflows_nodes.node_1 import get_search_intent_and_topic_ideas
from blueprints.workflows_nodes.node_2 import generate_deep_research_report_and_article_titles
from blueprints.workflows_nodes.node_3 import generate_article_outline
from blueprints.workflows_nodes.node_4 import generate_article_and_optimize_article_and_gen_image


workflow_nodes = [get_search_intent_and_topic_ideas, generate_deep_research_report_and_article_titles, generate_article_outline, generate_article_and_optimize_article_and_gen_image]

@celery.task(bind=True, autoretry_for=(), max_retries=0, default_retry_delay=0)
def workflow_task(self, params):
    try:
        email = params.get('email')
        session_id = params.get('session_id')
        node_input = params.get('node_input')
        workflow = WorkflowsModel.query.filter_by(email=email, session_id=session_id).first()
        status = workflow.status
        current_node_index = workflow.current_node_index

        #用于保存节点输入字段到数据库的映射
        node_input_field_mapping = {
        "1":['keyword','target_market','article_language'],
        "2":["chosen_topic","background_information","title_generation_demands"],
        "3":['article_title','secondary_keywords','outline_demand','additional_knowledge_points'],
        "4":['article_outline','narrative_perspective','main_image_option','sub_images_option']
            }

        if status == 'completed':
            #数据库更新：更新status为'in_progress'，current_node_index加1
            workflow.status = 'in_progress'
            workflow.current_node_index = current_node_index + 1
            #将节点输入字段保存到数据库
            field_arr = node_input_field_mapping[str(workflow.current_node_index)]
            for field in field_arr:
                setattr(workflow, field, node_input.get(field))
            db.session.commit()

            #调用下一个节点的函数
            next_node_function = workflow_nodes[int(workflow.current_node_index-1)]
            output = next_node_function(node_input,email,session_id)

            #如果节点函数返回包含status='failed'的字典，则视为错误
            if isinstance(output, dict) and output.get('status') == 'failed':
                workflow.status = 'failed'
                workflow.failed_message = output.get('message', '未知错误')
                workflow.updated_time = datetime.now()
                db.session.commit()
                return {'status': 'failed', 'message': workflow.failed_message}
            
            # 兼容旧的tuple格式错误返回
            if isinstance(output, tuple):
                workflow.status = 'failed'
                workflow.failed_message = output[0]['message']
                workflow.updated_time = datetime.now()
                db.session.commit()
                return {'status': 'failed', 'message': workflow.failed_message}

            #假设当前节点函数返回为字段字典，即成功返回结果，里面是需要保存到数据库中的所有输出字段的键值对，遍历后保存到数据库中
            for key, value in output.items():
                setattr(workflow,key,value)
            db.session.commit()

            #更新status为完成
            workflow.status = 'completed'
            workflow.updated_time = datetime.now()
            db.session.commit()
            return {'status': 'completed', 'message': 'Node completed successfully'}
        
        else:   #status为failed的情况
            workflow.status = 'in_progress'
            #将节点输入字段保存到数据库
            field_arr = node_input_field_mapping[str(workflow.current_node_index)]
            for field in field_arr:

                setattr(workflow, field, node_input.get(field))
            db.session.commit()

            #调用当前节点的函数
            current_node_function = workflow_nodes[int(workflow.current_node_index-1)]
            output = current_node_function(node_input,email,session_id)
            
            #如果节点函数返回包含status='failed'的字典，则视为错误
            if isinstance(output, dict) and output.get('status') == 'failed':
                workflow.status = 'failed'
                workflow.failed_message = output.get('message', '未知错误')
                workflow.updated_time = datetime.now()
                db.session.commit()
                return {'status': 'failed', 'message': workflow.failed_message}
            
            # 兼容旧的tuple格式错误返回
            if isinstance(output, tuple):
                workflow.status = 'failed'
                workflow.failed_message = output[0]['message']
                workflow.updated_time = datetime.now()
                db.session.commit()
                return {'status': 'failed', 'message': workflow.failed_message}

            #假设当前节点函数返回为字段字典，里面是需要保存到数据库中的所有输出字段的键值对，遍历后保存到数据库中
            for key, value in output.items():
                setattr(workflow,key,value)
            db.session.commit()

            #更新status为完成
            workflow.status = 'completed'
            workflow.updated_time = datetime.now()
            db.session.commit()
            return {'status': 'completed', 'message': 'Node completed successfully'}
    except Exception as e:
        error_message = f"task_execution执行失败 - 用户:{email}, 工作流id:{session_id}, 错误详情：{e}"
        logging.error(error_message)
        return {'status': 'failed', 'message': error_message}