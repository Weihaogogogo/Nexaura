from exts import db
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #id，自增长主键，在使用时并未用到
    username = db.Column(db.String(50), nullable=False) #用户名
    password = db.Column(db.String(200), nullable=False) #密码，用于用户登录
    email = db.Column(db.String(100), unique=True, nullable=False) #账号，用户登录的唯一身份凭证
    available_uses = db.Column(db.Integer, default=0, nullable=False) #剩余调用额度
    join_time = db.Column(db.DateTime, default=datetime.now, nullable=False) #用户注册时间

