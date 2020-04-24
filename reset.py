import pymysql

import secret
import config
from models.base_model import SQLModel
from models.comment import Comment
from models.session import Session
from models.todo import Todo
from models.user_role import UserRole
from models.user import User
# from models.weibo import Weibo
# from models.comment import Comment
from models.weibo import Weibo
from utils import log


def recreate_table(cursor):
    cursor.execute(Todo.sql_create)
    cursor.execute(User.sql_create)
    cursor.execute(Session.sql_create)
    cursor.execute(Weibo.sql_create)
    cursor.execute(Comment.sql_create)


def recreate_database():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=secret.mysql_password,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                'DROP DATABASE IF EXISTS `{}`'.format(
                    config.db_name
                )
            )
            cursor.execute(
                'CREATE DATABASE `{}` DEFAULT CHARACTER SET utf8mb4'.format(
                    config.db_name
                )
            )
            cursor.execute('USE `{}`'.format(config.db_name))

            recreate_table(cursor)

        connection.commit()
    finally:
        connection.close()


def test_comment():
    # add
    form = dict(
        content='hello',
        weibo_id=5,
    )
    c = Comment(form)
    c.add(1)

    # update
    form = dict(
        id=1,
        content='well done',
    )
    id = int(form['id'])
    Comment.update(1, **form)

    # user
    user = c.user()
    log('test comment user(), us, ', user)


def test_weibo():
    # add
    form = dict(
        content='hello',
    )
    user_id = 1
    Weibo.add(form, user_id)

    # update
    form = dict(
        id=1,
        content='well done',
        user_id=1,
    )
    weibo_id = 1
    Weibo.update(weibo_id, **form)

    # comments
    w = Weibo.one(id=1)
    form = dict(
        content='hello',
        weibo_id=1,
    )
    c = Comment(form)
    c.add(1)
    form = dict(
        content='hello233',
        weibo_id=1,
    )
    c = Comment(form)
    c.add(1)

    cs = w.comments()
    log('test comments cs', cs)


def test_user():
    # add
    form = dict(
        username='hello',
        password='123',
        role=UserRole.normal,
    )
    u = User.new(form)
    log('test user add u, ', u)


def test_data():
    # SQLModel.init_db()

    # Test.new({})

    form = dict(
        username='abc',
        password='123',
        role=UserRole.normal,
    )
    form1 = dict(
        username='xyz',
        password='123',
        role=UserRole.normal,
    )

    q = dict(
        username='abc',
        role='normal',
    )
    u, result = User.register(form)
    # Session.add(u.id)
    # u, result = User.register(form1)
    # user = User.one(**q)
    # log('test, one, user', user)
    # Session.add(u.id)

    q = dict(
        user_id=1,
    )
    # session = Session.one(**q)
    # log('test, one, session', session)
    q = dict(
        role='normal',
    )
    # User.all(**q)
    # User.all()
    # Session.all()

    # form = dict(
    #     content='test weibo',
    # )
    # w = Weibo.add(form, u.id)
    # form = dict(
    #     content='test comment',
    #     weibo_id=w.id,
    # )
    # Weibo.comment_add(form, u.id)
    test_weibo()
    test_comment()

    SQLModel.connection.close()


if __name__ == '__main__':
    recreate_database()
    SQLModel.init_db()
    test_user()
    test_data()
