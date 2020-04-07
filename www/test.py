#-*- coding:utf8-*-
# import asyncio
# import www.orm
# from www.models import User, Blog, Comment
# import time
#
#
# async def test(loop):
#     #连接池异步连接
#     await www.orm.create_pool(loop,user='root', password='664991558', db='awesome')
#     #u = User(name='jinxn', email='test@123.com', passwd='123', image='about:blank')
#     summary = 'python框架搭建 Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
#     u=Blog(user_id='12',user_name='guo',user_image='ss',name='Python New Study', content='123456767',summary=summary, created_at=time.time() - 3600)
#     #异步保存
#     await u.save()
#
# async def find(loop):
#     await www.orm.create_pool(loop,user='root', password='664991558', db='awesome')
#     rs = await Blog.findAll()
#     print('查找测试： %s' % rs)
#
# # 获取EventLoop:
# loop = asyncio.get_event_loop()
# # 执行coroutine
# loop.run_until_complete(asyncio.wait([test(loop),find(loop)]))
# loop.run_forever()


#2018-9-3
# leetcode  -1 -两数之和

# 给定一个整数数组和一个目标值，找出数组中和为目标值的两个数。
#
# 你可以假设每个输入只对应一种答案，且同样的元素不能被重复利用。
#
# 示例:
#
# 给定 nums = [2, 7, 11, 15], target = 9
#
# 因为 nums[0] + nums[1] = 2 + 7 = 9
# 所以返回 [0, 1]

# def twoSum(nums,target):
#     retar=[]
#     for i in range(1,len(nums)+1):
#
#         l=i-1
#         for j in range(i+1,len(nums)+1):
#             r=j-1
#             if(nums[i-1]+nums[j-1]==int(target)):
#                 retar.append([l,r])
#                 break
#
#     return retar
#
# nums=[5,2,3,9,7,3,65,7,6]
# t=twoSum(nums,9)
# print(t)
#
# def isLenth(s):
#     tmp = '0'
#     value = '0'
#     if s is None or len(s)==0:
#         return tmp
#     d={}
#     start=0
#     for i in range(len(s)):
#         if s[i] in d and d[s[i]]>=start:
#             tmp=i-start+1
#             d[s[i]]=i
#             tmp=max()



import time
from selenium import webdriver

browser=webdriver.Chrome()
browser.get('https://www.baidu.com')
browser.execute_script('window.open()')
print(browser.window_handles)
browser.switch_to_window(browser.window_handles[1])
browser.get('https://www.taobao.com')
time.sleep(1)
browser.switch_to_window(browser.window_handles[0])
browser.get('https://python.org')


