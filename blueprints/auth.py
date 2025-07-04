#认证模块（用户注册、登录、登出）
from flask import Blueprint, request, jsonify, current_app, session, g
from exts import mail,db
from flask_mail import Message
import random
from blueprints.forms import RegisterForm, LoginForm #导入表单验证类
from werkzeug.security import generate_password_hash, check_password_hash
from utils.jwt_utils import generate_jwt_token, decode_jwt_token, jwt_required
import time

bp = Blueprint('auth', __name__,url_prefix='/auth')

#生成随机数字验证码
def generate_verification_code(length=6):
    """生成指定长度的纯数字验证码"""
    return ''.join(random.choices('0123456789', k=length))

#用户注册
#1. 发送验证码邮件
@bp.route('/mail/captcha',methods=['GET'])
def mail_captcha():
    from exts import redis_client #在函数内部导入redis_client，避免redis_client未初始化的问题
    email = request.args.get('email')
    if not email:
        return jsonify({'code': 400, 'message': '注册邮箱不能为空'})
    
    #检测发送频率
    rate_key = f"send_rate:{email}"
    #如果redis中存在该Key，说明距离上次发送小于60秒，则禁止发送
    if redis_client.exists(rate_key):
        return jsonify({'code': 400, 'message': '请等待60秒后再发送验证码'})
    
    #获取随机6位数字的验证码
    code = generate_verification_code()
    #存储验证码到redis，设置过期时间10分钟
    redis_key = f"verification_code:{email}"
    redis_client.setex(redis_key, 600, code)
    #记录发送频率rate_key，设置过期时间为60秒
    redis_client.setex(rate_key, 60, "")
    
    message = Message(subject="欢迎使用Nexaura，在10分钟内创建高质量的SEO博客！",recipients=[email],body=f"您好！您本次操作的验证码是：{code}，请在10分钟内使用。")
    mail.send(message)
    print(redis_client.get(redis_key))
    return "邮件发送成功"
    
#2. 验证注册
@bp.route('/register', methods=['POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate():
        #创建新用户
        from models.UserModel import UserModel
        new_user = UserModel(username=form.username.data, email=form.email.data, password=generate_password_hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()
        message = Message(subject="欢迎使用Nexaura，在10分钟内创建高质量的SEO博客！",recipients=[form.email.data],body=f"您好,{form.username.data}！您已成功注册Nexaura，您的注册邮箱为{form.email.data}，将作为Nexaura的登录帐号。接下来请尽情体验Nexaura AI生成SEO博客的乐趣吧！")
        mail.send(message)
        session['email'] = form.email.data
        return jsonify({'code': 200, 'message': '注册成功'})
    else:
        return jsonify({'code': 400, 'message': form.errors}),400


#用户登录
@bp.route('/login',methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        email = form['email'].data
        password = form['password'].data
        from models.UserModel import UserModel
        from models.WorkflowsModel import WorkflowsModel
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            return jsonify({'code': 400, 'message': '用户不存在'})
        if not check_password_hash(user.password, password):
            return jsonify({'code': 400, 'message': '密码错误'})
        
        # 🔥 关键变化：生成 JWT tokens 而不是设置 session
        access_token = generate_jwt_token(email, 'access')
        refresh_token = generate_jwt_token(email, 'refresh')
        
        # 统计用户已使用的次数
        used_quota = WorkflowsModel.query.filter_by(email=email).count()
        
        return jsonify({
            'code': 200, 
            'message': '登录成功',
            'token': access_token,  # 🔥 前端会保存这个token
            'refresh_token': refresh_token,
            'data': {
                'email': user.email,
                'username': user.username,
                'available_uses': user.available_uses,
                'used_quota': used_quota,
                'join_time': user.join_time.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    else:
        return jsonify({'code': 400, 'message': form.errors}),400

# 🔥 新增：token刷新端点
@bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return jsonify({'code': 401, 'message': 'Authorization header missing'}), 401
    
    try:
        token = auth_header.split(' ')[1] if auth_header.startswith('Bearer ') else auth_header
    except IndexError:
        return jsonify({'code': 401, 'message': 'Invalid authorization header'}), 401
    
    payload = decode_jwt_token(token)
    
    if 'error' in payload:
        return jsonify({'code': 401, 'message': payload['error']}), 401
    
    if payload.get('type') != 'refresh':
        return jsonify({'code': 401, 'message': 'Invalid token type'}), 401
    
    # Generate new access token
    new_access_token = generate_jwt_token(payload['sub'], 'access')
    
    return jsonify({
        'code': 200,
        'message': 'Token refreshed successfully',
        'token': new_access_token
    })

#退出登录
@bp.route('/logout')
def logout():
    return jsonify({'code': 200, 'message': '退出登录成功'})

#前端页面在登录态时，验证登录态是否有效
@bp.route('/me', methods=['GET'])
@jwt_required  # 🔥 使用JWT装饰器而不是session检查
def get_current_user():
    email = g.current_user_email  # 🔥 从JWT payload获取，不是session
    
    from models.UserModel import UserModel
    from models.WorkflowsModel import WorkflowsModel
    user = UserModel.query.filter_by(email=email).first()
    if not user:
        return jsonify({'code': 401, 'message': '用户不存在'}), 401
    
    # 统计用户已使用的次数
    used_quota = WorkflowsModel.query.filter_by(email=email).count()
    
    # 返回用户基本信息（不包含敏感信息）
    return jsonify({
        'code': 200,
        'data': {
            'email': user.email,
            'username': user.username,
            'available_uses': user.available_uses,
            'used_quota': used_quota,  # 添加已使用次数
            'join_time': user.join_time.strftime('%Y-%m-%d %H:%M:%S')
        }
    })