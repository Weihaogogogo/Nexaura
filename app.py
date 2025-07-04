from flask import Flask, session, g
import config
from exts import db, mail, redis_client, init_redis, celery,cors
from flask_migrate import Migrate
from sqlalchemy import text
#导入蓝图模块
from blueprints.auth import bp as auth_bp
from blueprints.workflows import bp as workflows_bp
from blueprints.list import bp as list_bp
#导入模型
from models.UserModel import UserModel
#导入代理支持
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime

def create_app():
    #1.加载配置
    app = Flask(__name__)
    
    # 根据环境变量选择配置类
    import os
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(config.ProductionConfig)
    else:
        app.config.from_object(config.DevelopmentConfig)

    # 添加代理支持，让Flask正确识别HTTPS
    app.wsgi_app = ProxyFix(
        app.wsgi_app, 
        x_for=1, 
        x_proto=1, 
        x_host=1, 
        x_prefix=1
    )

    #2.初始化扩展
    db.init_app(app)
    mail.init_app(app)
    cors.init_app(app) #初始化CORS以支持跨域调试
    init_redis(app)
    migrate = Migrate(app, db)

    #3.配置并绑定Celery到Flask应用
    # 将Flask的配置同步给Celery
    if env == 'production':
        celery.config_from_object(config.ProductionConfig, namespace='CELERY')
    else:
        celery.config_from_object(config.DevelopmentConfig, namespace='CELERY')

    #创建一个特殊的Celery Task基类，它会自动设置app上下文
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask

    #4. 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(workflows_bp)
    app.register_blueprint(list_bp)

    #钩子函数 - 科普
    ## @app.before_request 请求处理前执行
    ## @app.after_request 请求处理后，响应发送前执行
    ## @app.context_processor 模版渲染前执行，返回的变量可以在模板中直接使用，前后端分离项目不用
    ## @app.errorhandler 错误发生时执行
    @app.before_request
    def before_request():
        # JWT模式下用户信息由装饰器处理，这里可以简化
        # 如果需要全局用户信息，可以从 g.current_user_email 获取
        pass

    #健康检查端点，用于Docker健康检查
    @app.route('/health')
    def health_check():
        """健康检查端点 - 服务器心跳"""
        try:
            # 检查数据库连接 (SQLAlchemy 2.0+ 新写法)
            with db.engine.connect() as connection:
                result = connection.execute(text('SELECT 1'))
                result.fetchone()
            
            # 检查Redis连接
            from exts import redis_client
            redis_client.ping()
            
            return {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'services': {
                    'database': 'ok',
                    'redis': 'ok',
                    'app': 'ok'
                }
            }, 200
        except Exception as e:
            return {
                'status': 'unhealthy', 
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }, 500
    
    return app




app = create_app()

if __name__ == '__main__':
    import os
    # 根据环境变量决定是否开启debug模式
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    app.run(debug=debug_mode, host=host, port=port)