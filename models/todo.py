from time import time

from models import Model
from models.base_model import SQLModel
from utils import log


class Todo(SQLModel):
    """
    Todo
    """
    sql_create = '''
    CREATE TABLE `todo` (
        `id`       INT NOT NULL AUTO_INCREMENT,
        `title`  varchar(255) NOT NULL,
        `user_id`  INT NOT NULL,
        PRIMARY KEY (`id`)
    );
    '''

    def __init__(self, form):
        super().__init__(form)
        self.title = form.get('title', '')
        self.user_id = form.get('user_id', -1)

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = int(user_id)
        Todo.new(form)

    @classmethod
    def update(cls, user_id, **kwargs):
        user_id = int(user_id)
        log('weibo, update, kwargs,', kwargs)
        kwargs.pop('id')
        super().update(user_id, **kwargs)
