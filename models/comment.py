from models.base_model import SQLModel
from models.user import User


class Comment(SQLModel):
    """
    评论类
    """
    sql_create = '''
    CREATE TABLE `comment` (
        `id`       INT NOT NULL AUTO_INCREMENT,
        `content`  varchar(255) NOT NULL,
        `user_id`  INT NOT NULL,
        `weibo_id` INT NOT NULL,
        PRIMARY KEY (`id`)
    );
    '''

    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = int(form.get('user_id', -1))
        self.weibo_id = int(form.get('weibo_id', -1))

    def user(self):
        u = User.one(id=self.user_id)
        return u

    def add(self, user_id):
        self.weibo_id = int(self.weibo_id)
        self.user_id = user_id
        self.new(self.__dict__)

    @classmethod
    def update(cls, comment_id, **kwargs):
        kwargs.pop('id')
        super().update(comment_id, **kwargs)
