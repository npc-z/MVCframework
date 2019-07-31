from models.base_model import SQLModel
from models.user import User
from models.comment import Comment
from utils import log


class Weibo(SQLModel):
    """
    微博类
    """
    sql_create = '''
    CREATE TABLE `weibo` (
        `id`       INT NOT NULL AUTO_INCREMENT,
        `content`  varchar(255) NOT NULL,
        `user_id`  INT NOT NULL,
        PRIMARY KEY (`id`)
    );
    '''

    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', -1)

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = int(user_id)
        Weibo.new(form)

    @classmethod
    def update(cls, weibo_id, **kwargs):
        weibo_id = int(weibo_id)
        log('weibo, update, kwargs,', kwargs)
        kwargs.pop('id')
        super().update(weibo_id, **kwargs)

    def comments(self):
        cs = Comment.all(weibo_id=self.id)
        return cs

    def username(self):
        user_id = int(self.user_id)
        u = User.one(id=user_id)
        return u.username
