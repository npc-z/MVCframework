# MVC 框架

## 简介

用 python 基于 socket 实现的 MVC web 框架


## 基本功能

- 基于 Socket 通信实现 web 服务器, 完成对客户端 HTTP 请求解析
- 使用 MVC 架构, 数据与视图解耦 , 实现前后端分离 , 完整路由分发
- 实现用户登录, 注册, 用户密码 加盐加密
- 包含 session 控制, 路由权限验证
- ~~自制 ORM, 完成增删改查~~
- 基于 MySQL 的新底层 ORM, 完成增删改查
- 内含 待办清单 应用, 用户可添加/修改/删除待办项
- 内含 简易weibo 应用, 用户可发布/删除感想, 其他用户添加/删除评论

## 远行项目
- Python 版本 `Python 3.6`
- 安装依赖 `pip install -r requirements.txt`
- 在 `config.py` 中配置数据库名
- 在 `secret.py` 中配置书库连接密码
- 执行 `python reset.py` 创建数据库
- 执行 `python server.py` 启动服务器



## 简单演示

### 登录注册

- 注册/登录

![avatar](https://github.com/Zeng-Tao/MVCframework/raw/master/GIF/login-register.gif )

### 简易 weibo

- 发表 weibo
- 发表评论
- weibo 主可删除自己 weibo 下的所有评论

![avatar](https://github.com/Zeng-Tao/MVCframework/raw/master/GIF/weibo.gif )

### todo 应用

- 添加/删除/修改

![avatar](https://github.com/Zeng-Tao/MVCframework/raw/master/GIF/todo.gif )