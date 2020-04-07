# -*- coding: utf-8 -*-

__author__ = 'Vehicle Guo'

' url handlers '



import re, time, json, logging, hashlib, base64, asyncio
import markdown2
from orm import select,execute
from aiohttp import web

from coroweb import get, post
from apis import APIValueError,APIPermissionError, APIResourceNotFoundError,APIError,Page

from models import User, Comment, Blog, next_id,Sort
from config import configs

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')





#
# 后端API包括：
#
#     获取日志：GET /api/blogs
#
#     创建日志：POST /api/blogs
#
#     修改日志：POST /api/blogs/:blog_id
#
#     删除日志：POST /api/blogs/:blog_id/delete
#
#     获取评论：GET /api/comments
#
#     创建评论：POST /api/blogs/:blog_id/comments
#
#     删除评论：POST /api/comments/:comment_id/delete
#
#     创建新用户：POST /api/users
#
#     获取用户：GET /api/users
#
# 管理页面包括：
#
#     评论列表页：GET /manage/comments
#
#     日志列表页：GET /manage/blogs
#
#     创建日志页：GET /manage/blogs/create
#
#     修改日志页：GET /manage/blogs/
#
#     用户列表页：GET /manage/users
#
# 用户浏览页面包括：
#
#     注册页：GET /register
#
#     登录页：GET /signin
#
#     注销页：GET /signout
#
#     首页：GET /
#
#     日志详情页：GET /blog/:blog_id

#首页
@get('/')
async def index(request,*, page = '1',sortid=''):
    sorts_sql = 'id,class_name,(select count(1) from blogs where sort_id=sorts.id) as nums '
    sorts = await Sort.finddefineAll(sorts_sql, orderBy='created_at desc')
    return {
        '__template__': 'blogs.html',
        '__user__':request.__user__,
        'page_index': get_page_index(page),
        'sorts':sorts,
        'sortid':sortid
    }

#注册页
@get('/register')
def register():
    return {
        '__template__': 'register.html'
    }

#登陆页
@get('/signin')
def login():
    return {
        '__template__':'signin.html'
    }

#退出
@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r

#日志详情页
@get('/blog/{id}')
async def get_blog(id,request):
    blog_sql='id,user_id,user_name,user_image,name,summary,content,created_at,sort_id,(select class_name  from sorts where id=blogs.sort_id)as class_name,(select count(1) from comments where blog_id = blogs.id) as nums '
    blog_where = 'id=?'
    #返回的是list集合 因此取第一个
    blog=await Blog.finddefineAll(blog_sql,blog_where,id)
    logging.info('555555555%s'%blog)
    # blog=await Blog.find(id)
    comments=await Comment.findAll('blog_id=?',id,orderBy='created_at desc')
    for c in comments:
        c.html_content = text2html(c.content)
    if blog[0]!=None:
        logging.info('555555555%s' % blog[0].content)
        blog[0].html_content = markdown2.markdown(blog[0].content)
    sorts_sql = 'id,class_name,(select count(1) from blogs where sort_id=sorts.id) as nums '
    sorts = await Sort.finddefineAll(sorts_sql, orderBy='created_at desc')
    return {
        '__template__':'blog.html',
        'blog':blog[0],
        'comments':comments,
        '__user__': request.__user__,
        'sorts':sorts
    }
#个人信息页
@get('/user/{id}')
async def get_user(id,request):
    if request.__user__:
        if not ((request.__user__.id == id) or request.__user__.admin):
            return web.HTTPFound('/signin')
    else:
        return web.HTTPFound('/signin')
    user=await User.find(id)
    user.created_at=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user.created_at))
    return {
        '__template__':'manage_user_edit.html',
        'user':user,
        '__user__': request.__user__
    }
#修改密码页
@get('/pwd/{id}')
async def get_pwd(id,request):
    if request.__user__:
        if request.__user__.id != id:
            return web.HTTPFound('/signin')
    else:
        return web.HTTPFound('/signin')
    user=await User.find(id)
    user.created_at=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user.created_at))
    return {
        '__template__':'manage_pwd_edit.html',
        'user':user,
        '__user__': request.__user__
    }


#显示分类管理页
@get('/manage/sorts')
def manage_sorts(*, page='1',request):
    return {
        '__template__': 'manage_sorts.html',
        'page_index': get_page_index(page),
        '__user__':request.__user__
    }
#分类页分页方法
@get('/api/sorts')
async def api_sorts(*, page='1'):
    page_index = get_page_index(page)
    num = await Sort.findNumber('count(id)')
    logging.info('num ::%s'%(num))
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, sorts=())
    sorts = await Sort.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    logging.info('sort  sort ::%s' % (sorts))
    return dict(page=p, sorts=sorts)
#创建分类页
@get('/manage/sorts/create')
def manage_create_sort(request):
    return {
        '__template__': 'manage_sort_edit.html',
        'id': '',
        'action': '/api/sorts',
        '__user__': request.__user__
}
#修改分类页
@get('/manage/sorts/edit')
def manage_edit_sort(*,request,id):
    return {
        '__template__':'manage_sort_edit.html',
        'id':id,
        'action':'/api/sorts/%s ' % id,
        '__user__': request.__user__
    }

#如为修改分类 回显数据方法
@get('/api/sorts/{id}')
async def api_get_sort(id,request):
    sort=await Sort.find(id)
    return dict(sort)



#显示日志管理页
@get('/manage/blogs')
def manage_blogs(*, page='1',name='',request):
    logging.info('8787878:%s' % name)
    return {
        '__template__': 'manage_blogs.html',
        'page_index': get_page_index(page),
        '__user__':request.__user__,
        'names':name
    }


# #日志分页方法(未加查询原方法)
# @get('/api/blogs')
# async def api_blogs(*, page='1'):
#     page_index = get_page_index(page)
#     num = await Blog.findNumber('count(id)')
#     p = Page(num, page_index)
#     if num == 0:
#         return dict(page=p, blogs=())
#     blogs = await Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
#     return dict(page=p, blogs=blogs)

#日志分页方法 2018-9-6 by gdk
@get('/api/blogs')
async def api_blogs(*, page='1',name='',sortid='',page_size=''):
    logging.info('2323233232323:%s'%name)
    page_index = get_page_index(page)
    wheresql=None
    blog_where=None
    select_sql='id,user_id,user_name,user_image,name,summary,content,created_at,sort_id,(select class_name  from sorts where id=blogs.sort_id)as class_name,(select count(1)  from comments where blog_id=blogs.id)as count'
    if  name or name.strip():
        blog_where="name like '%%"+name+"%%'"
        wheresql=" blogs.name like '%%"+name+"%%'"
    if sortid or sortid.strip():
        blog_where = "sort_id ='" + sortid + "'"
        wheresql = " blogs.sort_id='" + sortid + "'"
    num = await Blog.findNumber('count(id)', where=wheresql)
    p = Page(num, page_index)
    if page_size or page_size.strip():
        page_size = get_page_index(page_size)
        p = Page(num, page_index,page_size)
    if num == 0:
        return dict(page=p, blogs=())
    blogs=await Blog.finddefineAll(select_sql,where=blog_where,orderBy='created_at desc',limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)

#创建日志页
@get('/manage/blogs/create')
async def manage_create_blog(request):
    check_admin(request)
    sorts=await Sort.findAll(orderBy='created_at desc')
    return {
        '__template__': 'manage_blog_edit.html',
        'id': '',
        'action': '/api/blogs',
        '__user__': request.__user__,
        'sorts':  sorts
}

#修改日志页
@get('/manage/blogs/edit')
async def manage_edit_blog(*,request,id):
    check_admin(request)
    sorts = await Sort.findAll(orderBy='created_at desc')
    return {
        '__template__':'manage_blog_edit.html',
        'id':id,
        'action':'/api/blogs/%s ' % id,
        '__user__': request.__user__,
        'sorts': sorts
    }

#如为修改日志 回显数据方法
@get('/api/blogs/{id}')
async def api_get_blog(id,request):
    sorts = await Sort.findAll(orderBy='created_at desc')
    blog=await Blog.find(id)
    return dict(blog)



#评论管理页
@get('/manage/')
def manage():
    return 'redirect:/manage/comments'

#评论管理页
@get('/manage/comments')
def manage_comments(*,request, page='1'):
    return {
        '__template__': 'manage_comments.html',
        'page_index': get_page_index(page),
        '__user__': request.__user__
    }
#评论列表分页方法
@get('/api/comments')
async def api_comments(*, page='1'):
    page_index = get_page_index(page)
    num = await Comment.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, comments=())
    comments = await Comment.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, comments=comments)

#用户页面
@get('/manage/users')
def manage_users(*,request, page='1'):
    return {
        '__template__': 'manage_users.html',
        'page_index': get_page_index(page),
        '__user__': request.__user__
}

#用户列表分页方法
@get('/api/users')
async def api_get_users(*, page='1'):
    page_index = get_page_index(page)
    num = await User.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, users=())
    users = await User.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    for u in users:
        u.passwd = '******'
    return dict(page=p, users=users)




#注册方法
@post('/api/users')
async def api_register_user(*,email,name,password):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not password or not _RE_SHA1.match(password):
        raise APIValueError('password')
    users=await User.findAll('email=?',email)
    if len(users)>0:
        raise APIError('register:failed','email','Email is already in use.')
    uid= next_id()
    sha1_password='%s:%s'%(uid,password)
    user=User(id=uid,name=name.strip(),email=email,passwd=hashlib.sha1(sha1_password.encode('utf-8')).hexdigest(),image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()

    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

#登陆方法
@post('/api/authenticate')
async def authenticate(*,email,passwd):
    if not email:
        raise APIValueError('email','invaild email')
    if not passwd:
        raise APIValueError('passwd','invaild passwd')
    users=await User.findAll('email=?',email)
    if len(users)==0:
        raise APIValueError('email','invaild email exist')
    user=users[0]
    sha1=hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    logging.info('%s %s' % (user.passwd, sha1.hexdigest()))
    if user.passwd!=sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')
    r=web.Response()
    #"用户id" + "过期时间" + SHA1("用户id" + "用户口令" + "过期时间" + "SecretKey")
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

#详情页评论方法
@post('/api/blogs/{id}/comments')
async def api_create_comment(id,request,*,content):
    user=request.__user__
    if user is None:
        raise APIPermissionError('PLEASE signin frist')
    if not content or not content.strip():
        raise APIValueError('content')
    blog=await Blog.find(id)
    if blog is None:
        return APIResourceNotFoundError('Blog')
    comment=Comment(blog_id=blog.id,user_id=user.id,user_name=user.name,user_image=user.image,content=content.strip())
    await comment.save()
    return comment

#日志新增 保存方法
@post('/api/blogs')
async def api_create_blog(request,*,name,summary,content,sort_id):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty')
    if not sort_id or not sort_id.strip():
        raise APIValueError('sort_id', 'sort_id cannot be empty')
    blog=Blog(sort_id=sort_id, user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, name=name.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog


#日志修改详情页 保存方法
@post('/api/blogs/{id}')
async def api_update_blog(id,request,*,name,summary,content,sort_id):
    check_admin(request)
    blog=await Blog.find(id)
    if not name or not name.strip():
        raise APIValueError('name','name cannot be empty')
    if not summary or not summary.strip():
        raise APIValueError('summary','summary cannot be empty')
    if not content or not content.strip():
        raise APIValueError('content','content cannot be empty')
    if not sort_id or not sort_id.strip():
        raise APIValueError('sort_id', 'sort_id cannot be empty')
    blog.sort_id=sort_id
    blog.name=name
    blog.content=content
    blog.summary=summary
    await blog.update()
    return blog

#日志删除方法
@post('/api/blogs/{id}/delete')
async def api_delete_blog(*,id,request):
    check_admin(request)
    blog=await Blog.find(id)
    await blog.remove()
    return dict(id=id)


#分类新增 保存方法
@post('/api/sorts')
async def api_create_sort(request,*,class_name):
    check_admin(request)
    if not class_name or not class_name.strip():
        raise APIValueError('class_name', 'describe cannot be empty')
    sort=Sort(updated_user_id= request.__user__.id,updated_user_name=request.__user__.name, user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, class_name=class_name.strip())
    await sort.save()
    return sort

#分类修改详情页 保存方法
@post('/api/sorts/{id}')
async def api_update_sort(id,request,*,class_name):
    check_admin(request)
    sort=await Sort.find(id)
    if not class_name or not class_name.strip():
        raise APIValueError('class_name','class_name cannot be empty')
    sort.class_name=class_name
    sort.updated_user_id=request.__user__.id
    sort.updated_user_name=request.__user__.name
    sort.updated_at=time.time()
    await sort.update()
    return sort

#分类删除方法
@post('/api/sorts/{id}/delete')
async def api_delete_sort(*,id,request):
    check_admin(request)
    sort=await Sort.find(id)
    await sort.remove()
    return dict(id=id)


#评论删除方法
@post('/api/comments/{id}/delete')
async def api_delete_comments(id,request):
    check_admin(request)
    c=await Comment.find(id)
    if c is None:
        raise APIResourceNotFoundError('Comment')
    await c.remove()
    return dict(id=id)

#用户信息-管理员权限-更改方法
@post('/api/users/{id}/edit')
async def api_update_users(id,request):
    check_admin(request)
    user=await User.find(id)
    if user is None:
        raise APIResourceNotFoundError('User')
    user.admin=(not user.admin)
    await user.update()
    return dict(id=id)

#用户删除方法
@post('/api/users/{id}/delete')
async def api_delete_users(id,request):
    check_admin(request)
    user=await User.find(id)
    if user is None:
        raise APIResourceNotFoundError('User')
    await user.remove()
    return dict(id=id)

#用户信息名称更新方法s
@post('/api/users/{id}/update')
async def api_updates_users(id,*,request,name):
    if request.__user__.id!=id and not request.__user__.admin:
        raise APIResourceNotFoundError('User')
    user=await User.find(id)
    if user is None:
        raise APIResourceNotFoundError('User')
    user.name = name
    await user.update()
    return dict(id=id)

#用户密码更改 -密码构成（id:email:passwd）单项加密
@post('/api/users/pwd/{id}/update')
async def api_update_pwd_users(id,*,request,passwd,passwd2):
    logging.info('%s %s'%(passwd,passwd2))
    if request.__user__.id!=id:
        raise APIResourceNotFoundError('User')
    user=await User.find(id)
    if user is None:
        raise APIResourceNotFoundError('User')
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    logging.info('%s %s' % (user.passwd, sha1.hexdigest()))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password...')
    sha1_password = '%s:%s' % (id, passwd2)
    user.passwd= hashlib.sha1(sha1_password.encode('utf-8')).hexdigest()
    await user.update()
    return dict(id=id)


#判断是否管理员
def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()


#初始化分页起始值
def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p

#SHA1("用户id" + "用户口令" + "过期时间" + "SecretKey")
# 计算加密cookie:
def user2cookie(user, max_age):
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

# 解密cookie:
async def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None

#格式化文本内容
def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)









# @get('/api/users')
# async def api_get_users(*, page='1'):
#     num = await User.findNumber('count(id)')
#     if num == 0:
#         return dict(page=p, users=())
#     users = await User.findAll(orderBy='created_at desc')
#     for u in users:
#         u.passwd = '******'
#     return dict(users=users)