from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS
import redis
from config import BaseConfig
from celery import Celery

db = SQLAlchemy()
mail = Mail()
cors = CORS()
redis_client = None

def init_redis(app):
    global redis_client
    # 优先使用REDIS_URL环境变量(Docker环境)，否则使用独立配置项
    import os
    redis_url = os.getenv('REDIS_URL')
    if redis_url:
        redis_client = redis.from_url(redis_url, decode_responses=True)
    else:
        redis_client = redis.Redis(
            host=app.config['REDIS_HOST'],
            port=app.config['REDIS_PORT'],
            password=app.config['REDIS_PASSWORD'],
            db=app.config['REDIS_DB'],
            decode_responses=True
        )

# 创建Celery实例并配置防止重复执行的设置
import os
broker_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
celery = Celery(__name__,
                broker=broker_url,
                backend=broker_url)

# 配置Celery以防止任务重复执行和无限循环
celery.conf.update(
    # 任务确认设置 - 延迟确认直到任务完成
    task_acks_late=True,
    
    # Worker预取设置 - 减少预取数量防止任务堆积
    worker_prefetch_multiplier=1,
    
    # 任务时间限制设置
    task_time_limit=30 * 60,  # 30分钟硬限制
    task_soft_time_limit=25 * 60,  # 25分钟软限制
    
    # Worker丢失时拒绝任务
    task_reject_on_worker_lost=True,
    
    # 结果后端设置
    result_expires=60 * 60,  # 结果保存1小时
    result_backend_transport_options={
        'master_name': 'mymaster',
        'retry_on_timeout': True,
        'socket_keepalive': True,
        'socket_keepalive_options': {},
        'connection_pool_kwargs': {
            'max_connections': 20,
            'retry_on_timeout': True,
        }
    },
    
    # 序列化设置
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    
    # 错误处理
    task_ignore_result=False,
    
    # 防止任务重复
    worker_disable_rate_limits=True,
    
    # 连接设置
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_connection_max_retries=3,
)