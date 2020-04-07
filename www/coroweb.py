
# -*- coding: utf-8 -*-

__author__ = 'Vehicle Guo'

import asyncio, os, inspect, logging, functools
from urllib import parse
from aiohttp import web
from apis import APIError
from models import User

#' @get装饰器，给处理函数绑定URL和HTTP method-GET的属性 '
def get(path):
    '''
    Define decorator @get('/path')
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator
#' @post装饰器，给处理函数绑定URL和HTTP method-POST的属性
def post(path):
    '''
    Define decorator @post('/path')
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator



#将函数所有 没默认值的 命名关键字参数名 作为一个tuple返回 '
def get_required_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            args.append(name)
    return tuple(args)

#将函数所有的 命名关键字参数名 作为一个tuple返回
def get_named_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)

#' 检查函数是否有命名关键字参数，返回布尔值
def has_named_kw_args(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True

#' 检查函数是否有关键字参数集，返回布尔值 '
def has_var_kw_arg(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True

#' 检查函数是否有request参数，返回布尔值。' \
#'若有request参数，检查该参数是否为该函数的最后一个参数，否则抛出异常 '
def has_request_arg(fn):
    sig = inspect.signature(fn) # 含有 参数名，参数 的信息
    params = sig.parameters
    found = False
    for name, param in params.items():
        if name == 'request':
            found = True
            continue
        # 如果找到‘request’参数后，还出现位置参数，就会抛出异常
        if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError('request parameter must be the last named parameter in function: %s%s' % (fn.__name__, str(sig)))
    return found

#从URL函数中分析其需要接收的参数，从request中获取必要的参数，
# 调用URL函数，然后把结果转换为web.Response对象
class RequestHandler(object):
    #请求处理器，用来封装处理函数
    def __init__(self, app, fn):
        self._app = app
        self._func = fn
        self._has_request_arg = has_request_arg(fn)
        self._has_var_kw_arg = has_var_kw_arg(fn)
        self._has_named_kw_args = has_named_kw_args(fn)
        self._named_kw_args = get_named_kw_args(fn)
        self._required_kw_args = get_required_kw_args(fn)
    # 分析请求
    async def __call__(self, request):
        kw = None
        if self._has_var_kw_arg or self._has_named_kw_args or self._required_kw_args:
            # 当传入的处理函数具有 关键字参数集 或 命名关键字参数 或 request参数
            if request.method == 'POST':
                # POST请求预处理
                if not request.content_type:
                    # 无正文类型信息时返回
                    return web.HTTPBadRequest('Missing Content-Type.')
                ct = request.content_type.lower()
                if ct.startswith('application/json'):
                    # 处理JSON类型的数据，传入参数字典中
                    params = await request.json()
                    if not isinstance(params, dict):
                        return web.HTTPBadRequest('JSON body must be object.')
                    kw = params
                elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
                    # 处理表单类型的数据，传入参数字典中
                    params = await request.post()
                    kw = dict(**params)
                else:
                    # 暂不支持处理其他正文类型的数据
                    return web.HTTPBadRequest('Unsupported Content-Type: %s' % request.content_type)
            if request.method == 'GET':
                # GET请求预处理
                qs = request.query_string
                # 获取URL中的请求参数，如 name=Justone, id=007
                if qs:
                    # 将请求参数传入参数字典中
                    kw = dict()
                    for k, v in parse.parse_qs(qs, True).items():
                        kw[k] = v[0]
        if kw is None:
            # 请求无请求参数时
            kw = dict(**request.match_info)
        else:
            # 参数字典收集请求参数
            if not self._has_var_kw_arg and self._named_kw_args:
                # remove all unamed kw:
                copy = dict()
                for name in self._named_kw_args:
                    if name in kw:
                        copy[name] = kw[name]
                kw = copy
            # check named arg:
            for k, v in request.match_info.items():
                if k in kw:
                    logging.warning('Duplicate arg name in named arg and kw args: %s' % k)
                kw[k] = v
        if self._has_request_arg:
            kw['request'] = request
        # check required kw:
        if self._required_kw_args:
            # 收集无默认值的关键字参数
            for name in self._required_kw_args:
                if not name in kw:
                    # 当存在关键字参数未被赋值时返回，例如 一般的账号注册时，没填入密码就提交注册申请时，提示密码未输入
                    return web.HTTPBadRequest('Missing argument: %s' % name)
        logging.info('call with args: %s' % str(kw))
        try:
            r = await self._func(**kw)
            # 最后调用处理函数，并传入请求参数，进行请求处理
            return r
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)

#' 添加静态资源路径 '
def add_static(app):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')#获得包含'static'的绝对路径
    # os.path.dirname(os.path.abspath(__file__)) 返回脚本所在目录的绝对路径
    app.router.add_static('/static/', path)# 添加静态资源路径
    logging.info('add static %s => %s' % ('/static/', path))

#将处理函数注册到web服务程序的路由当中
def add_route(app, fn):
    method = getattr(fn, '__method__', None)# 获取 fn 的 __method__ 属性的值，无则为None
    path = getattr(fn, '__route__', None)# 获取 fn 的 __route__ 属性的值，无则为None
    if path is None or method is None:
        raise ValueError('@get or @post not defined in %s.' % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        # 当处理函数不是协程时，封装为协程函数
        fn = asyncio.coroutine(fn)
    logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method, path, RequestHandler(app, fn))

#自动把handler模块符合条件的函数注册
def add_routes(app, module_name):
    logging.info('add_routes...{}'.format(module_name))
    n = module_name.rfind('.')
    if n == (-1):
        # 没有匹配项时
        mod = __import__(module_name, globals(), locals())
        logging.info('mod...{}'.format(mod))
        # import一个模块，获取模块名 __name__
    else:
        # 添加模块属性 name，并赋值给mod
        name = module_name[n+1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    for attr in dir(mod):
        # dir(mod) 获取模块所有属性
        if attr.startswith('_'):
            # 略过所有私有属性
            continue
        fn = getattr(mod, attr)
        logging.info('fn...{}'.format(fn))
        # 获取属性的值，可以是一个method
        if callable(fn):
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                # 对已经修饰过的URL处理函数注册到web服务的路由中
                add_route(app, fn)