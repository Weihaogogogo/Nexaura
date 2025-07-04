import os
from datetime import timedelta

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "qrjenvidndpmfgdksncislxjvndf") #用于加密session
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT 配置
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-here-make-it-strong")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))  # 1小时
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 2592000))  # 30天

    #redis配置（用于存储验证码）
    REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    #验证码过期时间（秒）
    CAPTCHA_EXPIRE_TIME = int(os.getenv("CAPTCHA_EXPIRE_TIME", 600)) #10分钟
    # Celery 基础配置
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", 'redis://localhost:6379/0')
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ENABLE_UTC = True
    
    # 重试配置 - 防止无限重试
    CELERY_TASK_ALWAYS_EAGER = False
    CELERY_TASK_EAGER_PROPAGATES = True
    CELERY_TASK_REJECT_ON_WORKER_LOST = True
    CELERY_WORKER_DISABLE_RATE_LIMITS = True
    

#开发环境的配置
class DevelopmentConfig(BaseConfig):
    # 本地开发使用现有配置，Docker部署时使用环境变量
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        "mysql+pymysql://root:235568419@127.0.0.1:3306/db_seo_article?charset=utf8mb4"
    )
    
    #邮箱配置
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.163.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 465))
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "True").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "13006885304@163.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "DJXBAPmKJ4KZPbVN")
    MAIL_DEFAULT_SENDER = ("Nexaura", os.getenv("MAIL_USERNAME", "13006885304@163.com"))

    #CORS配置
    cors_origins_str = os.getenv("CORS_ORIGINS", "https://localhost:3000,http://localhost:3000,https://localhost,http://localhost")
    CORS_ORIGINS = [origin.strip() for origin in cors_origins_str.split(",")]
    CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]  # 允许的请求方法
    CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]  # 允许的请求头
    CORS_SUPPORTS_CREDENTIALS = True

    # Session配置
    SESSION_COOKIE_NAME = 'session'  # cookie名称
    SESSION_COOKIE_DOMAIN = None  # cookie域名，None表示当前域名
    SESSION_COOKIE_PATH = '/'  # cookie路径
    SESSION_COOKIE_HTTPONLY = True  # 防止JavaScript访问cookie
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False").lower() == "true"  # 开发环境设为False，生产环境建议设为True
    SESSION_COOKIE_SAMESITE = 'None'  # 支持跨域
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)  # session过期时间

# 测试环境的配置，暂时用不到，所以先备注掉
# class TestingConfig(BaseConfig):
#     SQLALCHEMY_DATABASE_URI = "mysql+pymysql://[测试服务器MySQL用户名]:[测试服务器MySQL密码]@[测试服务器MySQL域名]:[测试服务器MySQL端口号]/pythonbbs?charset=utf8mb4"


# 生产环境配置
class ProductionConfig(BaseConfig):
    # 基础配置
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        "mysql+pymysql://seo_user:password@mysql:3306/db_seo_article?charset=utf8mb4"
    )
    
    # 生产环境HTTPS安全配置
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_SECURE = True
    
    # CORS配置 - 从环境变量读取生产环境域名
    cors_origins_str = os.getenv("CORS_ORIGINS", "https://nexauraseo.com")
    CORS_ORIGINS = [origin.strip() for origin in cors_origins_str.split(",")]
    CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]
    CORS_SUPPORTS_CREDENTIALS = True

    # 生产环境的邮箱配置
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 465))
    MAIL_USE_SSL = str(os.getenv("MAIL_USE_SSL", "true")).lower() == "true"
    MAIL_USE_TLS = str(os.getenv("MAIL_USE_TLS", "false")).lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")