#表单验证的方法，在auth.py中使用(在auth中并不会完全依赖这里的注册类来验证，部分验证在auth中进行)
import wtforms
from wtforms.validators import DataRequired, Length, Email, EqualTo
from models.UserModel import UserModel

#表单 - 注册验证类
class RegisterForm(wtforms.Form):
    #验证格式是否正确
    email = wtforms.StringField(validators=[wtforms.validators.Email(message='邮箱格式错误')])
    code = wtforms.StringField(validators=[wtforms.validators.Length(min=6, max=6, message='验证码长度错误')])
    username = wtforms.StringField(validators=[wtforms.validators.Length(min=3, max=20, message='用户名格式错误')])
    password = wtforms.StringField(validators=[wtforms.validators.Length(min=6, max=20, message='密码格式错误')])
    password_confirm = wtforms.StringField(validators=[wtforms.validators.EqualTo('password', message='两次密码不一致')])
    #验证是否已注册/数据是否正确
    ##1. 验证邮箱是否被注册
    def validate_email(self, field):
        user = UserModel.query.filter_by(email=field.data).first()
        if user:
            raise wtforms.ValidationError('该邮箱已被注册')
    ##2. 校验验证码是否正确
    def validate_code(self, field):
        email = self.email.data
        code = field.data
        from exts import redis_client
        redis_key = f"verification_code:{email}"
        stored_code = redis_client.get(redis_key)
        if not stored_code:
            raise wtforms.ValidationError('验证码未发送或已过期')
        if stored_code != code:
            raise wtforms.ValidationError('验证码错误')


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[wtforms.validators.Email(message='邮箱格式错误')])
    password = wtforms.StringField(validators=[wtforms.validators.Length(min=6, max=20, message='密码格式错误')])