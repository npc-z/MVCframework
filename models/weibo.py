from models import Model
from models.user import User
from models.comment import Comment


class Weibo(Model):
    """
    微博类
    """
    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', None)

    @classmethod
    def add(cls, form, user_id):
        w = Weibo(form)
        w.user_id = user_id
        w.save()

    @classmethod
    def update(cls, form):
        weibo_id = int(form['id'])
        w = Weibo.find_by(id=weibo_id)
        w.content = form['content']
        w.save()

    def comments(self):
        cs = Comment.find_all(weibo_id=self.id)
        return cs

    def username(self):
        user_id = int(self.user_id)
        u = User.find_by(id=user_id)
        return u.username
