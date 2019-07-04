import json

from models.user_role import (
    Encoder,
    my_decode,
)

from utils import log


def save(data, path):
    """
    本函数把一个 dict 或者 list 写入文件
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    # indent 是缩进
    # ensure_ascii=False 用于保存中文
    s = json.dumps(data, indent=2, ensure_ascii=False, cls=Encoder)
    with open(path, 'w+', encoding='utf-8') as f:
        # log('save', path, s, data)
        f.write(s)


def load(path):
    """
    本函数从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        # log('load', s)
        return json.loads(s, object_hook=my_decode)


class Model(object):
    """
    Model 是所有 model 的基类
    """

    def __init__(self, form):
        self.id = form.get('id', None)

    @classmethod
    def db_path(cls):
        """
        model 表路径
        """
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        m.save()
        return m

    @classmethod
    def delete(cls, id):
        ms = cls.all()
        # 删除对应 id 的 model
        for i, m in enumerate(ms):
            if m.id == id:
                del ms[i]
                break

        # 保存
        d = [m.__dict__ for m in ms]
        path = cls.db_path()
        save(d, path)

    @classmethod
    def all(cls):
        """
        all 方法使用 load 函数得到所有的 models
        """
        path = cls.db_path()
        models = load(path)
        log('models in all', models)
        ms = [cls(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        log('find_by kwargs', kwargs)

        for m in cls.all():
            exist = True
            for k, v in kwargs.items():
                if not hasattr(m, k) or not getattr(m, k) == v:
                    exist = False
            if exist:
                return m

    @classmethod
    def find_all(cls, **kwargs):
        log('find_all kwargs', kwargs)
        models = []

        for m in cls.all():
            exist = True
            for k, v in kwargs.items():
                log('for loop in find all', m, k, v, hasattr(m, k), getattr(m, k), getattr(m, k) == v)
                if not hasattr(m, k) or not getattr(m, k) == v:
                    exist = False
            if exist:
                models.append(m)

        return models

    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        models = self.all()
        log('models', models)

        if self.id is None:
            # 加上 id
            if len(models) > 0:
                # log('不是第一个元素', models[-1].id)
                self.id = models[-1].id + 1
            else:
                # log('第一个元素')
                self.id = 0
            models.append(self)
        else:
            # 有 id 说明已经是存在于数据文件中的数据
            # 那么就找到这条数据并替换
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self

        # 保存
        d = [m.__dict__ for m in models]
        path = self.db_path()
        save(d, path)

    def __repr__(self):
        """
        格式化打印输出对象
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)
