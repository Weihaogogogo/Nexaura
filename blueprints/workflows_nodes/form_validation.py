#必备参数映射表，用于判断用户输入的必备参数是否完整（不含非必要参数）
from flask import jsonify
from models.WorkflowsModel import WorkflowsModel

def params_required(params):
    email = params.get('email')
    session_id = params.get('session_id')
    new_workflow = params.get('new_workflow')
    node_input = params.get('node_input')

    params_required = {
        "1":["keyword","target_market","article_language"],
        "2":["chosen_topic"],
        "3":["article_title"],
        "4":["article_outline","narrative_perspective","main_image_option","sub_images_option"],
    }
    
    #完整性校验
    #1. 校验email是否完整
    if not email:
        return jsonify({'code':400, 'message':'缺少email'}),400
    
    #2. 如果是第一次请求，校验node_input是否完整
    if new_workflow:
        #第一次请求，校验node_input是否完整
        if not node_input:
            return jsonify({'code':400, 'message':'node_input中缺少节点1的必要参数，因此用户额度没有变化，工作流实例尚未创建。'}),400
        else:
            #校验node_input中的参数是否完整
            for param in params_required["1"]:
                if not node_input.get(param):
                    return jsonify({'code':400, 'message':'node_input中缺少节点1的必要参数，因此用户额度没有变化，工作流实例尚未创建。'}),400
            return True
    #3. 非第一次请求，校验session_id是否存在数据库中,以及对应的节点输入参数是否完整
    else:
        if not session_id:
            return jsonify({'code':400, 'message':'缺少session_id'}),400
        else:
            #校验session_id是否存在数据库中
            workflow = WorkflowsModel.query.filter_by(email=email,session_id=session_id).first()
            if not workflow:
                return jsonify({'code':400, 'message':'session_id不存在或者无权访问'}),400
            else:
                #校验对应的节点输入参数是否完整(需要验证status的值来决定对应params_required的key)
                #如果工作流节点状态为completed，则需要验证输入参数在下一个节点中是否完整，如果完整则可以继续调用，否则返回错误
                if workflow.status == 'completed':
                    #如果工作流已全部完成，则不能被调用
                    if workflow.current_node_index >= 4:
                        return jsonify({'code':400, 'message':'工作流已完成，请勿重复调用'}),400
                    #如果工作流未全部完成，则校验对应的节点输入参数是否完整
                    for param in params_required[str(workflow.current_node_index+1)]:
                        if not node_input.get(param):
                            return jsonify({'code':400, 'message':f'在对应的节点{workflow.current_node_index+1}中node_input参数不完整，请检查node_input中是否缺少{param}参数'}),400
                #如果工作流节点状态为in_progress，则不能被调用
                elif workflow.status == 'in_progress':
                    return jsonify({'code':400, 'message':'工作流正在进行中，请勿重复调用'}),400
                #如果工作流节点状态为failed，则需要验证输入参数在原节点中是否完整，如果完整则可以继续调用，否则返回错误
                else:
                    for param in params_required[str(workflow.current_node_index)]:
                        if not node_input.get(param):
                            return jsonify({'code':400, 'message':f'在对应的节点{workflow.current_node_index}中node_input参数不完整，请检查node_input中是否缺少{param}参数'}),400
                    return True




