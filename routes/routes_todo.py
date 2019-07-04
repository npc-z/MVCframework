from models.todo import Todo
from routes import (
    redirect,
    current_user,
    html_response,
    login_required,
)
from utils import log


def same_user_required(route_function):
    """
    用户只能删除自己的 todo 事项
    """
    def f(request):
        log('same_user_required')
        u = current_user(request)
        if 'id' in request.query:
            todo_id = request.query['id']
        else:
            todo_id = request.form()['id']
        t = Todo.find_by(id=int(todo_id))

        if t.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/todo/index')

    return f


@login_required
def index(request):
    """
    todo 首页的路由函数
    """
    u = current_user(request)
    todos = Todo.find_all(user_id=u.id)

    return html_response('todo_index.html', todos=todos)


@login_required
def add(request):
    """
    用于增加新 todo 的路由函数
    """
    u = current_user(request)
    form = request.form()
    Todo.add(form, u.id)

    return redirect('/todo/index')


@same_user_required
@login_required
def delete(request):
    """
    删除 todo
    """
    todo_id = int(request.query['id'])
    Todo.delete(todo_id)
    return redirect('/todo/index')


@same_user_required
@login_required
def edit(request):
    """
    编辑 todo
    """
    todo_id = int(request.query['id'])
    t = Todo.find_by(id=todo_id)
    return html_response('todo_edit.html', todo=t)


@same_user_required
@login_required
def update(request):
    """
    更新 todo
    """
    form = request.form()
    Todo.update(form)

    return redirect('/todo/index')


def route_dict():
    """
    路由字典
    """
    d = {
        '/todo/index': index,
        '/todo/add': add,
        '/todo/delete': delete,
        '/todo/edit': edit,
        '/todo/update': update,
    }
    return d
