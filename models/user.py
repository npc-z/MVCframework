from models import Model
from models.base_model import SQLModel
from models.user_role import UserRole

import hashlib


# class User(Model):
#     """
#     """
#
#     def __init__(self, form):
#         super().__init__(form)
#         self.username = form.get('username', '')
#         self.password = form.get('password', '')
#         self.role = form.get('role', UserRole.normal)
#
#     @staticmethod
#     def guest():
#         form = dict(
#             role=UserRole.guest,
#             username='【游客】',
#         )
#         u = User(form)
#         return u
#
#     def is_guest(self):
#         return self.role == UserRole.guest
#
#     @staticmethod
#     def salted_password(password, salt='$!@><?>HUI&DWQa`'):
#         """$!@><?>HUI&DWQa`"""
#         salted = password + salt
#         hash = hashlib.sha256(salted.encode()).hexdigest()
#         return hash
#
#     @classmethod
#     def login(cls, form):
#         salted = cls.salted_password(form['password'])
#         u = User.find_by(username=form['username'], password=salted)
#         if u is not None:
#             result = '登录成功'
#             return u, result
#         else:
#             result = '用户名或者密码错误'
#             return User.guest(), result
#
#     @classmethod
#     def register(cls, form):
#         valid = len(form['username']) > 2 and len(form['password']) > 2
#         if valid:
#             form['password'] = cls.salted_password(form['password'])
#             u = User.new(form)
#             # result = '注册成功<br> <pre>{}</pre>'.format(User.all())
#             result = '注册成功, 请登录'
#             return u, result
#         else:
#             result = '用户名或者密码长度必须大于2'
#             return User.guest(), result


class User(SQLModel):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """

    sql_create = '''
    CREATE TABLE `user` (
        `id`        INT NOT NULL AUTO_INCREMENT,
        `username`  VARCHAR(255) NOT NULL,
        `password`  VARCHAR(255) NOT NULL,
        `role`      ENUM('guest', 'normal') NOT NULL,
        PRIMARY KEY (`id`)
    );
    '''

    def __init__(self, form):
        super().__init__(form)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.role = form.get('role', UserRole.normal)

    @staticmethod
    def guest():

        form = dict(
            role=UserRole.guest,
            username='【游客】',
        )
        u = User(form)
        return u

    def is_guest(self):
        return self.role == UserRole.guest

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        """$!@><?>HUI&DWQa`"""
        salted = password + salt
        hash = hashlib.sha256(salted.encode()).hexdigest()
        return hash

    @classmethod
    def login(cls, form):
        salted = cls.salted_password(form['password'])
        # 作业 2
        # u = User.one_for_username_and_password(username=form['username'], password=salted)
        q = dict(
            username=form['username'],
            password=salted,
        )
        u = User.one(**q)
        if u is not None:
            result = '登录成功'
            return u, result
        else:
            result = '用户名或者密码错误'
            return User.guest(), result

    @classmethod
    def register(cls, form):
        valid = len(form['username']) > 2 and len(form['password']) > 2
        if valid:
            form['password'] = cls.salted_password(form['password'])
            u = User.new(form)
            result = '注册成功'
            return u, result
        else:
            result = '用户名或者密码长度必须大于2'
            return User.guest(), result
