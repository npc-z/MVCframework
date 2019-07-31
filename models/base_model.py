import pymysql

import config
import secret
from utils import log


class SQLModel(object):
    connection = None

    @classmethod
    def init_db(cls):
        cls.connection = pymysql.connect(
            host='localhost',
            user='root',
            password=secret.mysql_password,
            db=config.db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def __init__(self, form):
        # 因为 id 是数据库给的，所以最开始初始化的时候必须是 None
        self.id = form.get('id', None)

    @classmethod
    def table_name(cls):
        return '`{}`'.format(cls.__name__.lower())

    @classmethod
    def new(cls, form):
        # cls(form) 相当于 User(form)
        m = cls(form)
        id = cls.insert(m.__dict__)
        m.id = id
        return m

    @classmethod
    def insert(cls, form):
        # {
        #     'username': 'gua',
        #     'password': 123,
        # }
        form.pop('id')
        # INSERT INTO `User` (
        #   `username`, `password`, `email`
        # ) VALUES (
        #   %s, %s, %s
        # )
        sql_keys = ', '.join(['`{}`'.format(k) for k in form.keys()])
        sql_values = ', '.join(['%s'] * len(form))
        sql_insert = 'INSERT INTO {} ({}) VALUES ({})'.format(
            cls.table_name(),
            sql_keys,
            sql_values,
        )
        log('ORM insert <{}>'.format(sql_insert))

        values = tuple(form.values())

        # try:
        #   cursor = cls.connection.cursor()
        #   cursor.execute(sql_insert, values)
        #   _id = cursor.lastrowid
        # finally:
        #   cursor.close()
        with cls.connection.cursor() as cursor:
            cursor.execute(sql_insert, values)
            _id = cursor.lastrowid
        cls.connection.commit()

        return _id

    @classmethod
    def delete(cls, id):
        sql_delete = 'DELETE FROM {} WHERE `id`=%s'.format(cls.table_name())
        log('ORM delete <{}>'.format(sql_delete.replace('\n', ' ')))

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_delete, (id,))
        cls.connection.commit()

    @classmethod
    def update(cls, id, **kwargs):
        # UPDATE
        # 	`User`
        # SET
        # 	`username`=%s, `password`=%s
        # WHERE `id`=%s;
        sql_set = ', '.join(
            ['`{}`=%s'.format(k) for k in kwargs.keys()]
        )
        sql_update = 'UPDATE {} SET {} WHERE `id`=%s'.format(
            cls.table_name(),
            sql_set,
        )
        log('ORM update <{}>'.format(sql_update.replace('\n', ' ')))

        values = list(kwargs.values())
        values.append(id)
        values = tuple(values)

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_update, values)
        cls.connection.commit()

    @classmethod
    def one(cls, **kwargs):
        query = ' and '.join(
            ['`{}`=%s'.format(k) for k in kwargs.keys()]
        )
        values = tuple(kwargs.values())
        sql = 'SELECT * FROM {} WHERE {}'.format(
            cls.table_name(),
            query,
        )
        log('ORM one values, ', values)
        log('ORM one', sql)

        with cls.connection.cursor() as cursor:
            cursor.execute(sql, values)
            result = cursor.fetchone()

        if result is None:
            return None
        else:
            m = cls(result)
        return m

    @classmethod
    def all(cls, **kwargs):
        table_name = cls.table_name()
        values = tuple(kwargs.values())
        sql = 'SELECT * FROM {}'.format(table_name)
        if len(kwargs) != 0:
            query = ' and '.join(
                ['`{}`=%s'.format(k) for k in kwargs.keys()]
            )

            # log('ORM all values, ', values)

            sql = 'SELECT * FROM {} WHERE {}'.format(
                table_name,
                query,
            )
        log('ORM all', sql)

        with cls.connection.cursor() as cursor:
            cursor.execute(sql, values)
            result = cursor.fetchall()

        ms = [cls(m) for m in result]
        log('ORM all, ms', ms)
        return ms

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        不明白就看书或者 搜
        """
        name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(name, s)

    def json(self):
        return self.__dict__
