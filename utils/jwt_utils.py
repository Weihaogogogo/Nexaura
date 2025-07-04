import jwt
import datetime
from flask import current_app, request, jsonify, g
from functools import wraps

def generate_jwt_token(user_email, token_type='access'):
    """生成 JWT token"""
    if token_type == 'access':
        expires_delta = datetime.timedelta(seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    else:  # refresh
        expires_delta = datetime.timedelta(seconds=current_app.config['JWT_REFRESH_TOKEN_EXPIRES'])
    
    payload = {
        'sub': user_email,  # subject
        'iat': datetime.datetime.utcnow(),  # issued at
        'exp': datetime.datetime.utcnow() + expires_delta,  # expiration
        'type': token_type
    }
    
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def decode_jwt_token(token):
    """解码 JWT token"""
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}

def jwt_required(f):
    """JWT 认证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'code': 401, 'message': 'Authorization header missing'}), 401
        
        try:
            # Extract Bearer token
            token = auth_header.split(' ')[1] if auth_header.startswith('Bearer ') else auth_header
        except IndexError:
            return jsonify({'code': 401, 'message': 'Invalid authorization header format'}), 401
        
        payload = decode_jwt_token(token)
        
        if 'error' in payload:
            return jsonify({'code': 401, 'message': payload['error']}), 401
        
        if payload.get('type') != 'access':
            return jsonify({'code': 401, 'message': 'Invalid token type'}), 401
        
        # Store user info in g object
        g.current_user_email = payload['sub']
        return f(*args, **kwargs)
    
    return decorated_function 