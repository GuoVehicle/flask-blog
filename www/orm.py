# -*-coding:utf8 -*-
__author__='Vehicle Guo'

import asyncio, logging
import aiomysql

def log(sql, args=()):
    logging.info('SQL: %s' % sql)

#根据异步驱动程序aiomysql创建连接池 保存在__pool
async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )

#异步执行查询方法
async def select(sql, args, size=None):
    log(sql, args)
    global __pool
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            logging.info('sql888888888:%s%s'%(sql.replace('?', '%s'),args))
            await cur.execute(sql.replace('?', '%s'), args or ())
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
        logging.info('rows returned: %s' % len(rs))
        return rs

#异步执行sql 返回影响条数
async def execute(sql, args, autocommit=True):
    log(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected
#生成占位符
def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)

#保存某个model的属性值并转化为field类
class Field(object):

    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)

class StringField(Field):

    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)

class BooleanField(Field):

    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)

class IntegerField(Field):

    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)

class FloatField(Field):

    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)

class TextField(Field):

    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)

#type()方法具有修改类的功能
#元类Metaclass 通过传入的不同的model类  修改成相应的映射模板
#所有的类都只能动态定义，因为只有使用者才能根据表的结构定义出对应的类来
#传入该model如user类 通过元类修改该类实例 形成一个统一风格的类
#该类的规范是为了更好的让从model派生出的实例user去执行增删改查的操作类
#其他任何的model实例不管表多表少 都可以从这里生成新的实例  动态生成 这样就完成了数据库表和model类的映射
#代码复用性高 简单的orm框架
class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        #修改类时排除修改model类本身
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        #表名 如果传入时元素__table__为空 则默认为类名
        tableName = attrs.get('__table__', None) or name
        #打印日志
        logging.info('found model: %s (table: %s)' % (name, tableName))
        #装载model实例元素的字典
        mappings = dict()
        #装载表里除主键以外的字段名称 list
        fields = []
        #找到主键
        primaryKey = None
        #循环model实例的所有元素 以及他们key
        for k, v in attrs.items():
            #假如找到Field类型的属性  填充进mapping
            if isinstance(v, Field):
                logging.info('  found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    # 找到主键:
                    if primaryKey:
                        raise BaseException('Duplicate primary key for field: %s' % k)
                    primaryKey = k
                else:
                    #除主键外的其他字段
                    fields.append(k)
        if not primaryKey:
            raise BaseException('Primary key not found.')
        #删除model实例里原有的相关元素 以免运行出错  （实例的属性会遮盖类的同名属性）
        for k in mappings.keys():
            attrs.pop(k)
        #通过map 将实例的字段变为字符类型装在list
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))

        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey # 主键属性名
        attrs['__fields__'] = fields # 除主键外的属性名
        #.join分割字段名
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        #create_args_string方法生成与字段数量相同的？占位符  参数化
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)

class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        #判断如id value为空
        if value is None:
            field = self.__mappings__[key]
            #Default缺省属性为执行方法 假如有则执行为该字段生成value
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value
    #classmethod是用来指定一个类的方法为类方法，没有此参数指定的类的方法为实例方法
    #重构类的时候不必要修改构造函数，只需要额外添加你要处理的函数， @classmethod作用
    @classmethod
    async def findAll(cls, where=None, args=None, **kw):
        ' find objects by where clause. '
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
            print('find all sql:{}',sql)
        rs = await select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    #多表查询
    @classmethod
    async def finddefineAll(cls, selectField, where=None, args=None, **kw):
        ' find finddefineAll by select and where. '
        sql = ['select %s from `%s`' % (selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
            print('find finddefineAll sql:{}', sql)
        rs = await select(' '.join(sql), args)
        return [cls(**r) for r in rs]


    @classmethod
    async def findNumber(cls, selectField, where=None, args=None):
        ' find number by select and where. '
        sql = ['select %s _num_ from `%s`' % (selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']




    @classmethod
    async def find(cls, pk):
        ' find object by primary key. '
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), pk, 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)

    async def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = await execute(self.__update__, args)
        if rows != 1:
            logging.warn('failed to update by primary key: affected rows: %s' % rows)

    async def remove(self):
        args = [self.getValue(self.__primary_key__)]
        rows = await execute(self.__delete__, args)
        if rows != 1:
            logging.warn('failed to remove by primary key: affected rows: %s' % rows)
